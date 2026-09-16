> # ⚠️ This repository is not FaultMaven
>
> **The FaultMaven engine lives at [FaultMaven/faultmaven](https://github.com/FaultMaven/faultmaven).** Go there.
>
> This repository has not been touched since December 2025 and is kept only for
> reference. Everything below it describes that snapshot, and two claims on
> this page are wrong about FaultMaven today:
>
> - **The description.** FaultMaven reads **no live telemetry** — it has no
>   agents and no credentials in your systems. It works from the logs, metrics
>   and configs *you* share. That claim was retired from every other surface.
>   The headline's "for SRE and DevOps Teams" was narrowed for the same reason:
>   FaultMaven is for engineers generally.
> - **The numbers.** The test and coverage badges are from December 2025 and
>   describe a codebase that has since been superseded.
>
> **The licence below is genuine and still applies to this snapshot.** The code
> in this repository is Apache-2.0 and that grant is irrevocable — reuse it on
> those terms. It is only worth flagging because the *engine* is licensed
> differently: [FaultMaven/faultmaven](https://github.com/FaultMaven/faultmaven)
> ships under FSL-1.1-ALv2 (fair source, converting to Apache-2.0 two years
> after each release), so do not read this badge as describing that.
>
> **Where to go instead:**
>
> | | |
> |---|---|
> | Run it yourself | [FaultMaven/faultmaven](https://github.com/FaultMaven/faultmaven#quick-start) — free, fair source |
> | Let us run it | [app.faultmaven.ai](https://app.faultmaven.ai/) — Cloud beta is open, free while it is in beta |
> | Just look | [A real investigation, unedited](https://www.faultmaven.ai/investigation) |

---

# FaultMaven

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/Tests-148%20passing-brightgreen)](https://github.com/FaultMaven/faultmaven)
[![Coverage](https://img.shields.io/badge/Coverage-47%25-yellow)](https://github.com/FaultMaven/faultmaven)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Monolith-blue)](docs/architecture/)

**AI-Powered Troubleshooting Copilot for SRE and DevOps Teams**

FaultMaven correlates your live telemetry with your runbooks, docs, and past fixes. It delivers answers grounded in your actual system—not generic guesses. Resolve incidents faster with an AI copilot that understands both your stack and your organization.

---

## 🚀 Quick Start

Deploy FaultMaven Core locally with Docker in 4 simple steps.

### Prerequisites

- **Docker & Docker Compose** installed
- **LLM API Key** (OpenAI, Anthropic, or other [supported providers](#4-multi-provider-llm-support))

### Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/FaultMaven/faultmaven.git
cd faultmaven

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY

# 3. Start the platform
docker compose up -d
```

Database migrations run automatically on startup. No manual initialization needed!

**Access Points (Development Mode):**

- **Dashboard**: <http://localhost:3000> - Knowledge base management UI
- **API**: <http://localhost:8000> - Backend REST API
- **API Docs**: <http://localhost:8000/docs> - Interactive API documentation
- **Health Check**: <http://localhost:8000/health> - Service health status

**Access Points (Production Mode):**

- **Unified Application**: <http://localhost:8090> - Single port for both API and Dashboard
- **API Docs**: <http://localhost:8090/docs> - Interactive API documentation
- **Health Check**: <http://localhost:8090/health> - Service health status

> **Remote Access**: If deploying to a remote server, replace `localhost` with your server's IP address or domain name (e.g., `http://192.168.1.100:8000`). Configure `SERVER_HOST` in your `.env` file for remote dashboard access.
>
> **All deployment options:** See [deploy/](deploy/) for Docker and local development guides
>
> **Troubleshooting:** See [deploy/troubleshooting/](deploy/troubleshooting/) for common issues and solutions

### Option 2: Local Development

For running from source code with hot-reload, see [deploy/local/](deploy/local/).

---

## Why FaultMaven?

Traditional observability tools tell you **what** broke. Generic LLMs guess **why**, but can't see your infrastructure. FaultMaven bridges this gap.

### 1. Deep Context Awareness

Generic chatbots can't access your logs, configs, or deployments. FaultMaven auto-ingests your **full stack context**—correlating errors with recent changes, configuration drift, and system state.

**Example:** A Kubernetes pod is crashlooping. ChatGPT gives generic advice. FaultMaven ingests your pod logs, deployment YAML, and recent Git commits—then tells you the ConfigMap changed 2 hours ago.

### 2. Institutional Memory

Most troubleshooting knowledge dies in Slack threads. FaultMaven's **tiered knowledge base** ensures you never solve the same problem twice:

- **Global Knowledge Base:** Pre-loaded troubleshooting patterns for common tech stacks (Kubernetes, PostgreSQL, Redis, AWS)
- **User Knowledge Base:** Your personal runbooks, post-mortems, and documentation
- **Case Knowledge Base:** Context from past investigations (auto-cleanup after case closure)

### 3. AI-Powered Investigation Framework

FaultMaven uses a sophisticated **investigation framework** with 5 integrated engines:

- ✅ **MemoryManager** - Hierarchical memory management (64% token reduction)
- ✅ **WorkingConclusionGenerator** - Continuous progress tracking
- ✅ **PhaseOrchestrator** - Intelligent phase progression with loop-back detection
- ✅ **OODAEngine** - Adaptive investigation intensity (light/medium/full)
- ⏳ **HypothesisManager** - Hypothesis lifecycle management (pending structured LLM output)

**Status**: 80% integrated, 148/148 tests passing

### 4. Multi-Provider LLM Support

FaultMaven supports **7 LLM providers** with automatic fallback:

- Fireworks AI (recommended)
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3.5)
- Google Gemini
- HuggingFace
- OpenRouter
- Local (Ollama, vLLM)

---

## Architecture

FaultMaven is built as a **modular monolith** - a single codebase organized into well-defined modules with clear boundaries.

```
┌──────────────────────────────────────────────────────────┐
│            Browser Extension / Dashboard                 │
└─────────────────────────┬────────────────────────────────┘
                          │ HTTPS
                          ▼
┌──────────────────────────────────────────────────────────┐
│              FaultMaven Monolith (8000)                   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Module Layer (7 modules)              │  │
│  ├──────┬───────┬──────┬────────┬─────────┬──────────┤  │
│  │ Auth │Session│ Case │Evidence│Knowledge│Agent│Report│  │
│  └──────┴───────┴──────┴────────┴─────────┴──────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │      Shared Infrastructure (Providers/ORM)         │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    ┌────────┐          ┌─────────┐         ┌──────────┐
    │ Redis  │          │ChromaDB │         │ SQLite/  │
    │(Cache) │          │(Vectors)│         │PostgreSQL│
    └────────┘          └─────────┘         └──────────┘
```

### Modules

FaultMaven is organized into **7 domain modules** with clear boundaries:

- **Auth** - User authentication and authorization (JWT)
- **Session** - Multi-session management with client-based resumption
- **Case** - Investigation lifecycle with AI framework integration
- **Evidence** - File upload and evidence management
- **Knowledge** - Knowledge base with semantic search (RAG)
- **Agent** - AI agent orchestration with multi-turn conversations
- **Report** - Case closure documentation and report generation

See [architecture/](docs/architecture/) for detailed architecture documentation.

---

## Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Modular Monolith** | Clean module boundaries, single deployable unit | ✅ Production |
| **Multi-LLM Support** | 7 providers with automatic fallback | ✅ Production |
| **Investigation Framework** | 5-engine AI framework (80% integrated) | ✅ Production |
| **Knowledge Base (RAG)** | Semantic search with ChromaDB | ✅ Production |
| **Session Management** | Multi-session per user with device continuity | ✅ Production |
| **Evidence Management** | File upload with metadata tracking | ✅ Production |
| **Auto-Generated API Docs** | OpenAPI specs with breaking change detection | ✅ Production |
| **Token Optimization** | 64% reduction via hierarchical memory | ✅ Production |
| **Hypothesis Management** | Automated hypothesis lifecycle | ⏳ Pending |

---

## Current Status

**Latest Update**: 2025-12-26

### Investigation Framework Integration ✅

The FaultMaven investigation framework has been successfully integrated from the original FaultMaven-Mono implementation:

- **Integration Complete**: 80% (4/5 engines integrated)
- **Test Pass Rate**: 148/148 (100%)
- **Code Coverage**: 47%
- **Token Efficiency**: 64% improvement (~1,600 vs 4,500+ tokens)

**Integrated Components**:

- ✅ **MemoryManager** - Hierarchical memory (hot/warm/cold tiers)
- ✅ **WorkingConclusionGenerator** - Continuous progress tracking
- ✅ **PhaseOrchestrator** - Intelligent phase progression
- ✅ **OODAEngine** - Adaptive investigation intensity

**Pending**:

- ⏳ **HypothesisManager** - Requires structured LLM output (inherited limitation from FaultMaven-Mono)

For detailed status, see [investigation-framework-status.md](docs/working/investigation-framework-status.md)

---

## Development

### Project Structure

```
faultmaven/                  # Single repository - true monolith
├── src/faultmaven/          # Backend application
│   ├── modules/             # 7 domain modules
│   │   ├── auth/           # Authentication
│   │   ├── session/        # Session management
│   │   ├── case/           # Investigation management
│   │   │   └── engines/    # Investigation framework
│   │   ├── evidence/       # File upload
│   │   ├── knowledge/      # Knowledge base (RAG)
│   │   ├── agent/          # AI agent orchestration
│   │   └── report/         # Report generation
│   ├── providers/          # Infrastructure abstractions
│   ├── infrastructure/     # Redis, in-memory implementations
│   ├── app.py             # FastAPI application
│   └── dependencies.py    # Dependency injection
├── dashboard/              # Web UI (React/TypeScript)
│   ├── src/               # Dashboard source code
│   ├── public/            # Static assets
│   ├── Dockerfile         # Dashboard container
│   └── package.json       # Node.js dependencies
├── tests/                  # Test suite (148 tests)
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── alembic/               # Database migrations
├── Dockerfile             # Backend container
└── docker-compose.yml     # Full stack orchestration
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=faultmaven tests/

# Current status: 148/148 tests passing (100%)
```

### Contributing

See [Development Setup](docs/development/setup.md) for:
- Local development setup
- Module development patterns
- Testing guidelines
- Code quality standards

---

## Configuration

### Environment Variables

FaultMaven uses environment variables for configuration. Create a `.env` file from the template:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Key configuration areas:**

- **LLM Providers** - OpenAI, Anthropic, Groq, Ollama (see [Multi-Provider LLM Support](#4-multi-provider-llm-support))
- **Database** - SQLite (dev) or PostgreSQL (production)
- **Session Management** - Timeout, cleanup intervals, memory limits
- **File Upload** - Size limits, allowed MIME types
- **Vector Search** - ChromaDB or Pinecone

See [.env.example](.env.example) for complete configuration options with detailed comments and examples.

---

## Deployment

For detailed deployment instructions, see:

- **[Deployment Guide](docs/operations/deployment.md)** - Production deployment with Docker, Kubernetes, or manual setup
- **[Development Setup](docs/development/setup.md)** - Local development environment setup

---

## Documentation

**📖 [Complete Documentation Index](docs/README.md)** - Central map of all documentation

**Essential Documents:**

- **[architecture/](docs/architecture/)** - System architecture and module design
- **[Development Setup](docs/development/setup.md)** - Development setup and workflows
- **[Deployment Guide](docs/operations/deployment.md)** - Production deployment guide
- **[API Documentation](docs/api/)** - Auto-generated OpenAPI specs

**Additional Resources:**

- [Testing Strategy](docs/development/testing-strategy.md) - Testing approach
- [Security Guidelines](docs/operations/security.md) - Security guidelines
- [Troubleshooting](docs/operations/troubleshooting.md) - Common issues and solutions
- [FAQ](docs/reference/faq.md) - Frequently asked questions
- [Roadmap](docs/reference/roadmap.md) - Product roadmap

See [docs/README.md](docs/README.md) for complete documentation organized by role and task.

---

## Performance

### Metrics

- **Token Efficiency**: 64% reduction (4,500+ → ~1,600 tokens via MemoryManager)
- **Response Times** (p95):
  - Chat endpoint: <2s
  - Knowledge search: <500ms
  - Session operations: <100ms
- **Scalability**: 100-500 req/s per process (horizontal scaling via load balancer)

### Test Coverage

- **Total Tests**: 148/148 passing (100%)
- **Code Coverage**: 47% (target: 80%)
- **Integration Tests**: Critical paths covered

---

## User Interfaces

FaultMaven provides two complementary interfaces:

### Web Dashboard (Included)

Built-in React/TypeScript dashboard for proactive management:

- **Knowledge Base**: Upload runbooks, manage indexed documents
- **Case History**: View, search, and export past investigations
- **Configuration**: Manage LLM providers and settings
- **Access**: [http://localhost:3000](http://localhost:3000) (when running with Docker)

Located in [dashboard/](dashboard/) directory.

### Browser Extension (Separate Repository)

The **[FaultMaven Copilot](https://github.com/FaultMaven/faultmaven-copilot)** browser extension for reactive troubleshooting:

- Overlay AI troubleshooting on AWS Console, Datadog, Grafana
- Context-aware conversations during incidents
- File upload and evidence collection
- Multi-session support

See the [Copilot repository](https://github.com/FaultMaven/faultmaven-copilot) for installation and development.

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- **What to work on** - Priority-ordered critical gaps and high-priority tasks
- **Development setup** - How to get started
- **Testing requirements** - Coverage targets and testing strategy
- **PR guidelines** - How to submit contributions

**Quick Links**:

- [CONTRIBUTING.md](CONTRIBUTING.md) - **Start here for contribution guidelines**
- [Development Setup](docs/development/setup.md) - Development environment setup
- [TECHNICAL_DEBT.md](docs/TECHNICAL_DEBT.md) - Implementation gaps and roadmap
- [architecture/](docs/architecture/) - System architecture

---

## Contact

- **Issues**: [GitHub Issues](https://github.com/FaultMaven/faultmaven/issues)
- **Discussions**: [GitHub Discussions](https://github.com/FaultMaven/faultmaven/discussions)
- **Email**: support@faultmaven.ai

---

**Architecture**: Modular Monolith (Single Repository)
**Main Application**: `src/faultmaven/app.py`
**Default Port**: 8000
**Database**: SQLite (dev), PostgreSQL (production)
**Status**: ✅ Production Ready
