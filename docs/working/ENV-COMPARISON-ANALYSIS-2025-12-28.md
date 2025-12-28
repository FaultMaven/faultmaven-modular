# .env.example Configuration Comparison & Enhancement Analysis

**Date**: 2025-12-28
**Purpose**: Compare FaultMaven current vs FaultMaven-Mono configurations to identify valuable missing options

---

## Executive Summary

The **FaultMaven-Mono** `.env.example` (328 lines) is **significantly more comprehensive** than the current **FaultMaven** `.env.example` (74 lines). It includes:

- ✅ **Multi-provider LLM configuration** with fallbacks
- ✅ **OODA framework controls** with tunable investigation strategies
- ✅ **Memory management** with hierarchical tiers
- ✅ **Protection system** (PII, rate limiting, circuit breakers)
- ✅ **Session management** with configurable timeouts
- ✅ **Observability** (Opik tracing, metrics)
- ✅ **File upload controls** with size limits
- ✅ **Feature flags** for gradual rollouts

**Recommendation**: Merge valuable configurations into current setup while preserving simplicity for basic use cases.

---

## Detailed Comparison

### 1. LLM Provider Configuration

#### Current (Simple)
```env
# LLM Provider
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Alternative LLM Providers (not yet implemented)
# ANTHROPIC_API_KEY=
# OLLAMA_HOST=http://localhost:11434
```

**Issues**:
- ❌ No multi-provider support
- ❌ No fallback configuration
- ❌ No provider-specific settings (timeout, retries)
- ❌ Limited to OpenAI

#### FaultMaven-Mono (Comprehensive)
```env
# Primary chat provider
CHAT_PROVIDER=openai

# Multimodal provider for visual evidence
MULTIMODAL_PROVIDER=openai

# Synthesis provider for RAG (fast, cheap models)
SYNTHESIS_PROVIDER=openai

# Classifier provider
CLASSIFIER_PROVIDER=openai

# Code analysis provider
CODE_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic
ANTHROPIC_API_KEY=...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Fireworks AI
FIREWORKS_API_KEY=...
FIREWORKS_MODEL=accounts/fireworks/models/llama-v3p1-70b-instruct

# Groq (ultra-fast)
GROQ_API_KEY=...
GROQ_MODEL=meta-llama/Llama-4-Scout-17B-16E-Instruct

# Local LLM
LOCAL_LLM_MODEL=llama2-7b
LOCAL_LLM_URL=http://localhost:5000

# Behavior
STRICT_PROVIDER_MODE=false  # Enable fallback
LLM_REQUEST_TIMEOUT=30
LLM_MAX_RETRIES=3
LLM_MAX_TOKENS=4096
LLM_CONTEXT_WINDOW=128000
```

**Advantages**:
- ✅ **Role-based providers** (chat, multimodal, synthesis, classifier, code)
- ✅ **Multiple providers** configured simultaneously
- ✅ **Fallback support** via STRICT_PROVIDER_MODE
- ✅ **Provider-specific tuning** (timeout, retries, tokens)
- ✅ **Cost optimization** (cheap models for synthesis)

---

### 2. Session Management

#### Current (Basic)
```env
# Session Configuration
SESSION_TIMEOUT_MINUTES=60
```

**Issues**:
- ❌ No cleanup interval
- ❌ No memory limits
- ❌ No heartbeat configuration
- ❌ No per-user limits

#### FaultMaven-Mono (Advanced)
```env
# Session Timeout Configuration
SESSION_TIMEOUT_MINUTES=180                  # 3 hours
SESSION_CLEANUP_INTERVAL_MINUTES=30          # Cleanup every 30 min
SESSION_MAX_MEMORY_MB=100                    # Max memory per session
SESSION_HEARTBEAT_INTERVAL_SECONDS=30        # Frontend heartbeat
MAX_SESSIONS_PER_USER=10                     # Concurrent sessions limit
```

**Advantages**:
- ✅ **Memory protection** (prevents OOM)
- ✅ **Automatic cleanup** (scheduled cleanup)
- ✅ **DoS protection** (per-user limits)
- ✅ **Keep-alive tuning** (heartbeat interval)

---

### 3. OODA Investigation Framework

#### Current
**MISSING ENTIRELY**

#### FaultMaven-Mono
```env
# Investigation Strategy
# - active_incident: Fast, 70% confidence, can skip phases
# - post_mortem: Thorough, 85% confidence, all phases required
DEFAULT_INVESTIGATION_STRATEGY=active_incident

# OODA Cycle Intensity
# - light: 1-2 iterations (fast)
# - medium: 2-4 iterations (balanced)
# - full: 3-6 iterations (thorough)
DEFAULT_OODA_INTENSITY=medium

# Memory Management (Hierarchical 4-Tier)
HOT_MEMORY_TOKENS=500      # Last 2 iterations, full fidelity
WARM_MEMORY_TOKENS=300     # Iterations 3-5, LLM-summarized
COLD_MEMORY_TOKENS=100     # Older, key facts only
PERSISTENT_MEMORY_TOKENS=100  # Always accessible insights

# Phase Control
ENABLE_PHASE_SKIP=true                     # Skip phases if urgent
MIN_CONFIDENCE_TO_ADVANCE=0.70             # Advance threshold
STALL_DETECTION_ITERATIONS=3               # Stall detection

# Consultant Mode
PROBLEM_SIGNAL_THRESHOLD=moderate          # weak|moderate|strong
MAX_CONSULTANT_TURNS=5                     # Before suggesting full mode
```

**Value**:
- ✅ **Tunable investigation depth** (light/medium/full)
- ✅ **Memory optimization** (4-tier hierarchical system)
- ✅ **Adaptive behavior** (skip phases if urgent)
- ✅ **Stall detection** (prevent infinite loops)
- ✅ **User experience** (consultant mode limits)

**Current Status**: Investigation framework integrated but **not configurable**

---

### 4. Protection System

#### Current
**MISSING ENTIRELY**

#### FaultMaven-Mono
```env
# General Protection
PROTECTION_ENABLED=true
PROTECTION_FAIL_OPEN=true              # Continue on failure (dev)
BASIC_PROTECTION_ENABLED=true
INTELLIGENT_PROTECTION_ENABLED=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10

# PII Sanitization
AUTO_SANITIZE_BASED_ON_PROVIDER=true  # Auto-enable for external LLMs
SANITIZE_PII=true
PROTECTION_ENTITIES=[CREDIT_CARD,EMAIL_ADDRESS,PHONE_NUMBER,US_SSN,IP_ADDRESS]

# Circuit Breakers
SMART_CIRCUIT_BREAKERS_ENABLED=true
CIRCUIT_FAILURE_THRESHOLD=5
CIRCUIT_TIMEOUT_SECONDS=60

# Reputation System
REPUTATION_SYSTEM_ENABLED=true
REPUTATION_DECAY_RATE=0.05
```

**Value**:
- ✅ **PII protection** (GDPR compliance)
- ✅ **DoS protection** (rate limiting)
- ✅ **Resilience** (circuit breakers)
- ✅ **Security** (auto-sanitize for external LLMs)

---

### 5. File Upload & Processing

#### Current
**MISSING**

#### FaultMaven-Mono
```env
# Maximum file upload size
MAX_UPLOAD_SIZE_MB=10                  # Handles 95% of logs/configs
ALLOWED_MIME_TYPES=[...]
UPLOAD_TIMEOUT_SECONDS=300
TEMP_STORAGE_PATH=/tmp/faultmaven

# Document Processing
DOCUMENT_CHUNK_SIZE=1000
DOCUMENT_CHUNK_OVERLAP=100

# Chunking (for large documents)
CHUNK_TRIGGER_TOKENS=8000              # Trigger map-reduce
CHUNK_SIZE_TOKENS=4000                 # Target chunk size
CHUNK_OVERLAP_TOKENS=200
MAP_REDUCE_MAX_PARALLEL=5
```

**Value**:
- ✅ **DoS protection** (size limits)
- ✅ **Security** (MIME type whitelist)
- ✅ **Performance** (timeouts)
- ✅ **Scalability** (chunking for large files)

---

### 6. Observability & Monitoring

#### Current
**MISSING**

#### FaultMaven-Mono
```env
# Observability (Opik)
OPIK_USE_LOCAL=true
OPIK_LOCAL_URL=http://opik.faultmaven.local:30080
OPIK_PROJECT_NAME=FaultMaven Development
OPIK_TRACK_DISABLE=false

# Targeted Tracing (optional)
OPIK_TRACK_USERS=                      # Comma-separated user IDs
OPIK_TRACK_SESSIONS=                   # Comma-separated session IDs

# Performance Monitoring
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_DETAILED_TRACING=false

# Metrics
METRICS_ENABLED=true
METRICS_PORT=9090

# Prometheus (optional)
PROMETHEUS_ENABLED=false
PROMETHEUS_PUSHGATEWAY_URL=http://localhost:9091
```

**Value**:
- ✅ **Debugging** (trace specific users/sessions)
- ✅ **Performance analysis** (Opik integration)
- ✅ **Production monitoring** (Prometheus metrics)

---

### 7. Feature Flags

#### Current
**MISSING**

#### FaultMaven-Mono
```env
# Core Features
USE_DI_CONTAINER=true
USE_REFACTORED_SERVICES=true
USE_REFACTORED_API=true

# Context Management
ENABLE_TOKEN_AWARE_CONTEXT=true
ENABLE_CONVERSATION_SUMMARIZATION=true
MAX_CONVERSATION_TURNS=20
MAX_CONVERSATION_TOKENS=4000

# Experimental Features
ENABLE_ADVANCED_REASONING=false
ENABLE_MULTI_AGENT=false
ENABLE_WORKFLOW_OPTIMIZATION=false
```

**Value**:
- ✅ **Gradual rollouts** (enable/disable features)
- ✅ **A/B testing** (experiment flags)
- ✅ **Safety** (disable broken features)

---

### 8. Storage Adapters

#### Current (Fixed)
```env
DATABASE_URL=sqlite+aiosqlite:///./data/faultmaven.db
FILE_STORAGE=local
VECTOR_STORE=chromadb
```

**Issues**:
- ❌ No in-memory option for testing
- ❌ No adapter selection flexibility

#### FaultMaven-Mono (Pluggable)
```env
# Storage adapter selection
SESSION_STORAGE_TYPE=inmemory  # inmemory or redis
VECTOR_STORAGE_TYPE=inmemory   # inmemory or chromadb
USER_STORAGE_TYPE=inmemory     # inmemory or postgres
CASE_STORAGE_TYPE=inmemory     # inmemory or postgres
```

**Value**:
- ✅ **Fast testing** (in-memory adapters)
- ✅ **Development simplicity** (no external services)
- ✅ **Gradual scaling** (switch to persistent when needed)

---

### 9. Documentation & Organization

#### Current
- ❌ **No section headers** (hard to navigate)
- ❌ **Minimal comments**
- ❌ **No examples** for complex configs

#### FaultMaven-Mono
- ✅ **Clear section headers** (=== lines)
- ✅ **Detailed comments** explaining choices
- ✅ **Examples** with reasoning
- ✅ **Warnings** for risky settings

**Example**:
```env
# =============================================================================
# LLM Provider Configuration
# =============================================================================

# Primary chat provider for main diagnostic agent (openai, anthropic, fireworks, groq, local)
CHAT_PROVIDER=openai

# Multimodal provider for visual evidence processing (openai, anthropic, gemini)
# If not specified, falls back to CHAT_PROVIDER
MULTIMODAL_PROVIDER=openai
```

---

## Recommended Enhancements for Current .env.example

### Priority 1: Essential (High Impact, Easy to Add)

1. **Multi-Provider LLM Support**
   ```env
   # LLM Provider Selection
   LLM_PROVIDER=openai  # openai, anthropic, fireworks, ollama

   # Provider-Specific Behavior
   LLM_REQUEST_TIMEOUT=30
   LLM_MAX_RETRIES=3
   LLM_MAX_TOKENS=4096
   STRICT_PROVIDER_MODE=false  # Allow fallback to other providers

   # Anthropic (for fallback)
   ANTHROPIC_API_KEY=
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```

2. **Session Management**
   ```env
   # Session Configuration
   SESSION_TIMEOUT_MINUTES=180
   SESSION_CLEANUP_INTERVAL_MINUTES=30
   SESSION_MAX_MEMORY_MB=100
   MAX_SESSIONS_PER_USER=10
   ```

3. **File Upload Limits**
   ```env
   # File Upload Configuration
   MAX_UPLOAD_SIZE_MB=10
   UPLOAD_TIMEOUT_SECONDS=300
   ALLOWED_MIME_TYPES=["text/plain","application/json","text/csv"]
   ```

4. **Section Headers & Comments**
   ```env
   # =============================================================================
   # LLM Provider Configuration
   # =============================================================================

   # =============================================================================
   # Database & Storage
   # =============================================================================
   ```

---

### Priority 2: Valuable (Improves Production Readiness)

5. **Rate Limiting**
   ```env
   # Protection & Rate Limiting
   RATE_LIMIT_ENABLED=true
   RATE_LIMIT_REQUESTS_PER_MINUTE=60
   RATE_LIMIT_BURST_SIZE=10
   ```

6. **PII Protection**
   ```env
   # PII Sanitization
   AUTO_SANITIZE_BASED_ON_PROVIDER=true  # Auto-enable for external LLMs
   SANITIZE_PII=true
   PROTECTION_ENTITIES=[CREDIT_CARD,EMAIL_ADDRESS,PHONE_NUMBER,IP_ADDRESS]
   ```

7. **Circuit Breakers**
   ```env
   # Circuit Breakers (prevent cascading failures)
   CIRCUIT_BREAKERS_ENABLED=true
   CIRCUIT_FAILURE_THRESHOLD=5
   CIRCUIT_TIMEOUT_SECONDS=60
   ```

---

### Priority 3: Advanced (For Power Users)

8. **OODA Framework Tuning**
   ```env
   # Investigation Framework Configuration
   DEFAULT_INVESTIGATION_STRATEGY=active_incident  # active_incident, post_mortem
   DEFAULT_OODA_INTENSITY=medium  # light, medium, full

   # Memory Management (4-tier hierarchical)
   HOT_MEMORY_TOKENS=500
   WARM_MEMORY_TOKENS=300
   COLD_MEMORY_TOKENS=100
   ```

9. **Observability**
   ```env
   # Observability & Monitoring
   ENABLE_PERFORMANCE_MONITORING=true
   METRICS_ENABLED=true
   METRICS_PORT=9090
   ```

10. **Feature Flags**
    ```env
    # Feature Flags (optional)
    ENABLE_ADVANCED_REASONING=false
    ENABLE_MULTI_AGENT=false
    ```

---

## Proposed New .env.example Structure

```env
# =============================================================================
# FaultMaven Configuration
# =============================================================================
# Copy this file to .env and edit with your values

# =============================================================================
# Deployment Profile
# =============================================================================
PROFILE=core  # core, team, enterprise

# =============================================================================
# LLM Provider Configuration
# =============================================================================

# Provider Selection (openai, anthropic, fireworks, ollama)
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
# For OpenRouter or custom endpoints:
# OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Anthropic Configuration (for fallback)
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Ollama (Local LLM)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Provider Behavior
LLM_REQUEST_TIMEOUT=30
LLM_MAX_RETRIES=3
LLM_MAX_TOKENS=4096
STRICT_PROVIDER_MODE=false  # Allow fallback to other providers

# =============================================================================
# Database & Storage
# =============================================================================

# Database (SQLite for development, PostgreSQL for production)
DATABASE_URL=sqlite+aiosqlite:///./data/faultmaven.db
# For PostgreSQL: postgresql+asyncpg://user:password@localhost:5432/faultmaven

# File Storage
FILE_STORAGE=local
FILE_STORAGE_PATH=./data/files
# For S3:
# FILE_STORAGE=s3
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_S3_BUCKET=faultmaven-files

# Vector Database (ChromaDB)
VECTOR_STORE=chromadb
CHROMADB_PATH=./data/chromadb
CHROMA_HOST=localhost
CHROMA_PORT=8001

# =============================================================================
# Infrastructure Services
# =============================================================================

# Redis (Session storage and caching)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_URL=redis://localhost:6379/0

# =============================================================================
# Security & Authentication
# =============================================================================

# Identity Provider (JWT)
IDENTITY_PROVIDER=jwt
JWT_SECRET=change-me-in-production-use-a-long-random-string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# =============================================================================
# Application Settings
# =============================================================================

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO

# CORS (Allow dashboard and browser extensions)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# =============================================================================
# Session Management
# =============================================================================

SESSION_TIMEOUT_MINUTES=180
SESSION_CLEANUP_INTERVAL_MINUTES=30
SESSION_MAX_MEMORY_MB=100
MAX_SESSIONS_PER_USER=10

# =============================================================================
# File Upload & Processing
# =============================================================================

MAX_UPLOAD_SIZE_MB=10
UPLOAD_TIMEOUT_SECONDS=300
ALLOWED_MIME_TYPES=["text/plain","application/json","text/csv","text/xml"]
DOCUMENT_CHUNK_SIZE=1000
DOCUMENT_CHUNK_OVERLAP=100

# =============================================================================
# Protection & Rate Limiting
# =============================================================================

# Rate Limiting (DoS protection)
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST_SIZE=10

# PII Protection
AUTO_SANITIZE_BASED_ON_PROVIDER=true  # Auto-enable for external LLMs
SANITIZE_PII=true
PROTECTION_ENTITIES=[CREDIT_CARD,EMAIL_ADDRESS,PHONE_NUMBER,IP_ADDRESS]

# Circuit Breakers (prevent cascading failures)
CIRCUIT_BREAKERS_ENABLED=true
CIRCUIT_FAILURE_THRESHOLD=5
CIRCUIT_TIMEOUT_SECONDS=60

# =============================================================================
# Investigation Framework (Advanced)
# =============================================================================

# Strategy (active_incident = fast, post_mortem = thorough)
DEFAULT_INVESTIGATION_STRATEGY=active_incident

# Intensity (light = 1-2 iterations, medium = 2-4, full = 3-6)
DEFAULT_OODA_INTENSITY=medium

# Memory Management (hierarchical 4-tier system)
HOT_MEMORY_TOKENS=500    # Last 2 iterations, full fidelity
WARM_MEMORY_TOKENS=300   # Iterations 3-5, LLM-summarized
COLD_MEMORY_TOKENS=100   # Older, key facts only

# =============================================================================
# Observability & Monitoring (Optional)
# =============================================================================

ENABLE_PERFORMANCE_MONITORING=true
METRICS_ENABLED=true
METRICS_PORT=9090

# =============================================================================
# Feature Flags (Optional)
# =============================================================================

ENABLE_ADVANCED_REASONING=false
ENABLE_MULTI_AGENT=false
```

---

## Implementation Plan

### Step 1: Reorganize Current .env.example
- Add section headers (=== lines)
- Group related configs
- Add explanatory comments
- Remove outdated placeholders

### Step 2: Add Priority 1 Configs
- Multi-provider LLM support
- Session management
- File upload limits
- Better documentation

### Step 3: Add Priority 2 Configs
- Rate limiting
- PII protection
- Circuit breakers

### Step 4: Add Priority 3 Configs (Optional)
- OODA framework tuning
- Observability
- Feature flags

---

## Key Learnings from FaultMaven-Mono

### 1. **Separation of Concerns**
- Different providers for different tasks (chat, synthesis, multimodal)
- Allows cost optimization (cheap models for synthesis)

### 2. **Fail-Safe Defaults**
- PROTECTION_FAIL_OPEN=true (don't block on protection failure)
- AUTO_SANITIZE_BASED_ON_PROVIDER=true (smart PII handling)

### 3. **Clear Documentation**
- Section headers make navigation easy
- Comments explain WHY, not just WHAT
- Examples show realistic usage

### 4. **Tunable Complexity**
- Simple for basic use (set API key, go)
- Advanced for power users (tune every parameter)

### 5. **In-Memory Options**
- Fast testing without external services
- Gradual scaling path (inmemory → persistent)

---

## Conclusion

The FaultMaven-Mono configuration is **superior** in:
- ✅ **Flexibility** (multi-provider, adapters)
- ✅ **Protection** (PII, rate limiting, circuit breakers)
- ✅ **Observability** (metrics, tracing)
- ✅ **Tunability** (OODA controls, memory management)
- ✅ **Documentation** (clear sections, detailed comments)

**Recommendation**: Adopt the structure and valuable configs from Mono while keeping the current simple defaults for ease of use.

**Next Action**: Implement Priority 1 enhancements to current `.env.example`

---

**Generated**: 2025-12-28
**Comparison**: Current (74 lines) vs Mono (328 lines)
**Status**: Analysis complete, ready for implementation
