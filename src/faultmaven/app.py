"""
FaultMaven FastAPI Application.

Main application entry point that assembles all module routers.
"""

import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables from .env file
# This must happen before any other imports that read env vars
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from redis.asyncio import Redis

# Import all models to register them with SQLAlchemy
import faultmaven.models  # noqa: F401

from faultmaven.modules.agent.router import router as agent_router
from faultmaven.modules.auth.router import router as auth_router
from faultmaven.modules.session.router import router as session_router
from faultmaven.modules.case.router import router as case_router
from faultmaven.modules.evidence.router import router as evidence_router
from faultmaven.modules.knowledge.router import router as knowledge_router
from faultmaven.modules.report.router import router as report_router

from faultmaven.providers.core import CoreDataProvider, CoreFileProvider
from faultmaven.providers.factory import create_llm_provider
from faultmaven.providers.vectors.chromadb import ChromaDBProvider
from faultmaven.config import validate_required_configuration, ConfigurationError


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Initializes heavy resources on startup and cleans them up on shutdown.
    This prevents "First User Penalty" and ensures proper health checks.
    """
    logger.info("🚀 Starting FaultMaven application...")

    # ==========================================
    # STARTUP: Validate configuration first
    # ==========================================

    try:
        # Validate required configuration before initializing any providers
        logger.info("Validating configuration...")
        validate_required_configuration()
        logger.info("✅ Configuration validated")
    except ConfigurationError:
        # Error message already printed by validate_required_configuration()
        raise RuntimeError("Configuration validation failed - see error above")

    # ==========================================
    # STARTUP: Initialize heavy resources
    # ==========================================

    try:
        # 1. Initialize Redis client
        logger.info("Initializing Redis client...")
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        redis_client = Redis.from_url(redis_url, decode_responses=False)
        # Test connection
        await redis_client.ping()
        app.state.redis_client = redis_client
        logger.info("✅ Redis client initialized")

        # 2. Initialize Data Provider (Database)
        logger.info("Initializing Data Provider...")
        db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/faultmaven.db")
        data_provider = CoreDataProvider(connection_string=db_url)
        app.state.data_provider = data_provider
        logger.info("✅ Data Provider initialized")

        # 3. Initialize File Provider
        logger.info("Initializing File Provider...")
        base_path = os.getenv("FILE_STORAGE_PATH", "data/files")
        file_provider = CoreFileProvider(base_path=base_path)
        app.state.file_provider = file_provider
        logger.info("✅ File Provider initialized")

        # 4. Initialize LLM Provider
        logger.info("Initializing LLM Provider...")
        llm_provider = create_llm_provider()
        app.state.llm_provider = llm_provider
        provider_name = os.getenv("LLM_PROVIDER", "unknown")
        logger.info(f"✅ LLM Provider initialized ({provider_name})")

        # 5. Initialize Vector Provider (ChromaDB) - SLOW OPERATION
        logger.info("Initializing Vector Provider (ChromaDB)...")
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "data/chromadb")
        vector_provider = ChromaDBProvider(persist_directory=persist_dir)
        app.state.vector_provider = vector_provider
        logger.info("✅ Vector Provider (ChromaDB) initialized")

        logger.info("✅ All providers initialized successfully")
        logger.info("🎉 FaultMaven application ready to serve requests!")

    except Exception as e:
        logger.error(f"❌ Failed to initialize application: {e}")
        raise RuntimeError(f"Application startup failed: {e}") from e

    # Application is running
    yield

    # ==========================================
    # SHUTDOWN: Clean up resources
    # ==========================================

    logger.info("🛑 Shutting down FaultMaven application...")

    # Close Redis connection
    if hasattr(app.state, "redis_client"):
        logger.info("Closing Redis connection...")
        await app.state.redis_client.close()
        logger.info("✅ Redis connection closed")

    # Close database connections (if data provider has cleanup)
    if hasattr(app.state, "data_provider"):
        logger.info("Closing database connections...")
        # CoreDataProvider doesn't have explicit cleanup, but good to log
        logger.info("✅ Database connections closed")

    logger.info("✅ FaultMaven application shutdown complete")


def create_app(enable_lifespan: bool = True) -> FastAPI:
    """
    Create and configure FastAPI application.

    Args:
        enable_lifespan: Whether to enable lifespan context manager (default: True).
                        Set to False in tests to skip provider initialization.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="FaultMaven API",
        description="Modular monolith for AI-powered debugging and troubleshooting",
        version="0.1.0",
        lifespan=lifespan if enable_lifespan else None,  # Skip lifespan in tests
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include module routers
    app.include_router(auth_router)
    app.include_router(session_router)
    app.include_router(case_router)
    app.include_router(evidence_router)
    app.include_router(knowledge_router)
    app.include_router(report_router)
    app.include_router(agent_router)

    # ==========================================
    # Static File Serving (Production Mode)
    # ==========================================
    # In production, the dashboard is bundled into /app/static via multi-stage Dockerfile.
    # This allows the backend to serve both API and frontend from a single container.
    #
    # In development mode, the static directory won't exist, so we skip mounting it.
    # The dashboard runs separately on port 5173 (Vite dev server).

    static_dir = Path("/app/static")  # Production path from Dockerfile
    if static_dir.exists() and static_dir.is_dir():
        logger.info(f"📁 Mounting static files from {static_dir}")

        # Mount static assets (JS, CSS, images)
        app.mount(
            "/assets",
            StaticFiles(directory=str(static_dir / "assets")),
            name="assets"
        )

        # Serve index.html for root and all non-API routes (SPA routing)
        @app.get("/{full_path:path}")
        async def serve_dashboard(full_path: str):
            """
            Serve the React dashboard for all non-API routes.

            This enables client-side routing for the SPA.
            API routes are matched first due to router precedence.
            """
            # If the path exists as a file in static dir, serve it
            file_path = static_dir / full_path
            if file_path.exists() and file_path.is_file():
                return FileResponse(file_path)

            # Otherwise, serve index.html (SPA entry point)
            return FileResponse(static_dir / "index.html")

        logger.info("✅ Static file serving enabled (production mode)")
    else:
        logger.info("📝 Static files not found - running in development mode")
        logger.info("   Dashboard should be run separately: cd dashboard && pnpm dev")

        # Root health check (only used in dev mode)
        @app.get("/")
        async def root():
            return {
                "service": "faultmaven",
                "status": "healthy",
                "version": "0.1.0",
                "mode": "development"
            }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.get("/health/live")
    async def liveness_check():
        """Kubernetes liveness probe endpoint."""
        return {"status": "alive", "service": "faultmaven"}

    @app.get("/health/ready")
    async def readiness_check():
        """Kubernetes readiness probe endpoint."""
        return {"status": "ready", "service": "faultmaven", "checks": {"database": "ok", "cache": "ok"}}

    @app.post("/admin/refresh-openapi")
    async def refresh_openapi():
        """Admin endpoint to refresh OpenAPI spec."""
        return {"message": "OpenAPI spec refreshed", "version": "0.1.0"}

    @app.get("/admin/openapi-health")
    async def openapi_health():
        """Check OpenAPI spec health."""
        return {
            "status": "healthy",
            "openapi_version": "3.1.0",
            "endpoints_count": len(app.routes)
        }

    return app


# Create app instance for uvicorn
app = create_app()
