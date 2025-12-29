# Docker Deployment Fixes - December 28, 2024

## Issues Resolved

### 1. ✅ Docker Build Disk Space (1.6GB+ Saved)
**Problem:** Build failed with "No space left on device" when installing dependencies.

**Root Cause:** `sentence-transformers` dependency pulled 1.6GB+ of packages:
- PyTorch: 900MB
- CUDA libraries: 700MB+

**Fix:** Removed `sentence-transformers` from required dependencies in [pyproject.toml](../../pyproject.toml#L47)
- Not actually used in code (ChromaDB accepts pre-computed embeddings)
- Verified with `grep -r "import sentence_transformers" src/` - no matches

**Commit:** 5703c3e

---

### 2. ✅ Missing email-validator Dependency
**Problem:** Container crashed with `ImportError: email-validator is not installed`

**Root Cause:** Pydantic `EmailStr` in auth module requires email-validator package

**Fix:** Added `email-validator>=2.1.0` to dependencies in [pyproject.toml](../../pyproject.toml#L26)

**Commit:** 5703c3e

---

### 3. ✅ Multi-LLM Provider Support
**Problem:** Application hardcoded to use OpenAI's CoreLLMProvider, ignored LLM_PROVIDER env var

**Root Cause:** [app.py](../../src/faultmaven/app.py#L96) directly called `CoreLLMProvider()`

**Fix:** Created factory pattern in [factory.py](../../src/faultmaven/providers/factory.py)

**Supported Providers:**
- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models
- `groq` - Groq (OpenAI-compatible API)
- `gemini` - Google Gemini (OpenAI-compatible)
- `fireworks` - Fireworks AI (OpenAI-compatible)
- `openrouter` - OpenRouter multi-model proxy
- `ollama` - Local Ollama models

**Usage:**
```bash
# In .env file
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
```

**Commit:** bf08a0d

---

### 4. ✅ Docker BuildKit Cache Issue (CRITICAL)
**Problem:** Even with `--no-cache`, containers ran old code after source changes

**Root Cause:**
- Docker BuildKit layer caching
- Pip wheel cache persisting across builds
- `faultmaven` package wheel was cached with old code

**Symptoms:**
```python
# Source code had:
llm_provider = create_llm_provider()

# But container was running:
llm_provider = CoreLLMProvider()  # OLD CODE!
```

**Solution:**
```bash
# 1. Clear BuildKit cache
docker builder prune -af
docker buildx prune -af

# 2. Force clean build
DOCKER_BUILDKIT=1 docker build --no-cache --pull \\
  -f deploy/docker/Dockerfile \\
  -t test-backend:latest .

# 3. Tag and deploy
docker tag test-backend:latest faultmaven-faultmaven-backend:latest
docker compose up -d --force-recreate faultmaven-backend
```

**Verification:**
```bash
# Check code in image
docker run --rm faultmaven-faultmaven-backend:latest \\
  cat /usr/local/lib/python3.11/site-packages/faultmaven/app.py \\
  | grep -A 3 "# 4. Initialize LLM"

# Should show:
# llm_provider = create_llm_provider()  # ✅ NEW CODE
```

---

## Current Deployment Status

**Container Status:** ✅ Running and healthy
```bash
$ curl http://localhost:8000/health
{"status":"healthy"}
```

**LLM Provider:** ✅ Groq (configured via LLM_PROVIDER=groq)

**Docker Images:**
- Backend: `faultmaven-faultmaven-backend:latest`
- Build context: `/home/swhouse/product/faultmaven`
- Dockerfile: `deploy/docker/Dockerfile`

---

## Deployment Commands

### Quick Start (Normal Deploy)
```bash
docker compose up -d
```

### Clean Rebuild (After Code Changes)
```bash
# Stop all services
docker compose down -v

# Clear BuildKit cache
docker builder prune -af

# Rebuild from scratch
docker compose build --no-cache faultmaven-backend

# Start services
docker compose up -d

# Verify
curl http://localhost:8000/health
```

### Force Fresh Build (When Cache Issues Occur)
```bash
# Complete cleanup
docker compose down -v
docker builder prune -af
docker system prune -af

# Build with explicit flags
DOCKER_BUILDKIT=1 docker build \\
  --no-cache \\
  --pull \\
  --progress=plain \\
  -f deploy/docker/Dockerfile \\
  -t faultmaven-backend:clean .

# Tag for docker-compose
docker tag faultmaven-backend:clean faultmaven-faultmaven-backend:latest

# Deploy
docker compose up -d --force-recreate faultmaven-backend
```

---

## Files Changed

### New Files
- ✅ `src/faultmaven/providers/factory.py` - Multi-provider factory (224 lines)
- ✅ `deploy/docker/Dockerfile` - Docker build configuration
- ✅ `deploy/docker/.env` - Symlink to project root .env

### Modified Files
- ✅ `src/faultmaven/app.py` - Uses factory instead of CoreLLMProvider
- ✅ `deploy/docker/docker-compose.yml` - Updated build context paths
- ✅ `pyproject.toml` - Removed sentence-transformers, added email-validator
- ✅ `Dockerfile` - Changed from editable to regular install

---

## Troubleshooting

### Container shows old code after rebuild
**Symptom:** Traceback shows `CoreLLMProvider()` instead of `create_llm_provider()`

**Fix:**
```bash
# Verify source code
cat src/faultmaven/app.py | grep create_llm_provider

# Clear ALL caches
docker builder prune -af
docker buildx prune -af
docker system prune -af --volumes

# Build from scratch
docker compose build --no-cache --pull faultmaven-backend
```

### Health check fails
**Symptom:** Container shows as unhealthy

**Check logs:**
```bash
docker compose logs faultmaven-backend --tail=100
```

**Common causes:**
1. Missing LLM_PROVIDER in .env
2. Invalid API key
3. Redis not running
4. Port 8000 already in use

---

## Next Steps

**✅ Completed:**
- Docker build optimized (1.6GB saved)
- Multi-provider support implemented
- Cache issues resolved
- Application running successfully

**📋 To Do (if needed):**
- [ ] Test with other providers (anthropic, gemini, etc.)
- [ ] Add provider-specific integration tests
- [ ] Document provider-specific configuration
- [ ] Set up CI/CD with cache management

---

**Last Updated:** December 28, 2024
**Status:** ✅ All issues resolved, application deployed successfully
