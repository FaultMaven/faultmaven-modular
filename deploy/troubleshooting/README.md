# FaultMaven Troubleshooting Guide

This guide covers common issues you might encounter when running FaultMaven and their solutions.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Startup Issues](#startup-issues)
- [Port Conflicts](#port-conflicts)
- [Database Issues](#database-issues)
- [LLM Provider Issues](#llm-provider-issues)
- [Performance Issues](#performance-issues)
- [Data Persistence Issues](#data-persistence-issues)
- [Getting Help](#getting-help)

---

## Quick Diagnostics

Before diving into specific issues, run these commands to get a health snapshot:

```bash
# Check service status
./faultmaven status

# View recent logs
./faultmaven logs --tail 50

# Check resource usage
docker stats

# Verify Docker daemon is running
docker info
```

---

## Startup Issues

### Services won't start

**Symptoms:**
- `./faultmaven start` fails
- Containers exit immediately
- "Error response from daemon" messages

**Solutions:**

1. **Check Docker is running:**
   ```bash
   docker info
   ```
   If this fails, start Docker Desktop or the Docker daemon.

2. **Check for port conflicts:**
   ```bash
   # Development mode ports
   lsof -i :8000  # Backend API
   lsof -i :3000  # Dashboard
   lsof -i :6379  # Redis
   lsof -i :8001  # ChromaDB

   # Production mode port
   lsof -i :8090  # Unified application
   ```

3. **Check .env file exists:**
   ```bash
   ls -la .env
   ```
   If missing, create it:
   ```bash
   cp .env.example .env
   # Edit .env and add your LLM API key
   ```

4. **Check Docker Compose version:**
   ```bash
   docker compose version
   ```
   Requires Docker Compose v2.0+. Update if needed.

5. **View detailed error logs:**
   ```bash
   ./faultmaven logs
   ```

### Services start but show as "unhealthy"

**Symptoms:**
- `docker ps` shows services in "unhealthy" state
- Health checks failing

**Solutions:**

1. **Check if services are responding:**
   ```bash
   # Development mode
   curl http://localhost:8000/health

   # Production mode
   curl http://localhost:8090/health
   ```

2. **Wait longer:**
   The first startup can take 60-90 seconds while databases initialize and migrations run.

3. **Check database migrations ran:**
   ```bash
   # Development
   docker compose logs faultmaven-backend | grep alembic

   # Production
   docker compose -f docker-compose.prod.yml logs faultmaven | grep alembic
   ```

4. **Manually run migrations if needed:**
   ```bash
   # Development
   docker compose exec faultmaven-backend alembic upgrade head

   # Production
   docker compose -f docker-compose.prod.yml exec faultmaven alembic upgrade head
   ```

---

## Port Conflicts

### Port already in use

**Symptoms:**
- "bind: address already in use" error
- Services fail to start

**Solutions:**

1. **Find what's using the port:**
   ```bash
   # On macOS/Linux
   lsof -i :8000
   lsof -i :3000
   lsof -i :8090

   # On Windows (PowerShell)
   netstat -ano | findstr :8000
   ```

2. **Kill the conflicting process:**
   ```bash
   # On macOS/Linux
   kill -9 <PID>

   # On Windows (PowerShell)
   taskkill /PID <PID> /F
   ```

3. **Use custom ports via override file:**
   ```bash
   cp docker-compose.override.yml.example docker-compose.override.yml
   ```

   Edit `docker-compose.override.yml`:
   ```yaml
   services:
     faultmaven-backend:
       ports:
         - "8080:8000"  # Use 8080 instead of 8000

     faultmaven-dashboard:
       ports:
         - "3001:3000"  # Use 3001 instead of 3000
   ```

   Then restart:
   ```bash
   ./faultmaven restart
   ```

---

## Database Issues

### Database connection errors

**Symptoms:**
- "Connection refused" errors in logs
- "SQLSTATE[HY000]" errors
- Application won't start

**Solutions:**

1. **Check DATABASE_URL in .env:**
   ```bash
   grep DATABASE_URL .env
   ```

   Development (SQLite):
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./data/faultmaven.db
   ```

   Production (PostgreSQL):
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/faultmaven
   ```

2. **Verify database file exists (SQLite):**
   ```bash
   ls -la data/faultmaven.db
   ```

3. **Check database migrations:**
   ```bash
   docker compose exec faultmaven-backend alembic current
   docker compose exec faultmaven-backend alembic upgrade head
   ```

4. **Reset database (⚠️ DESTRUCTIVE):**
   ```bash
   # Backup first!
   cp data/faultmaven.db data/faultmaven.db.backup

   # Remove database
   rm data/faultmaven.db

   # Restart services (migrations will recreate DB)
   ./faultmaven restart
   ```

### Migration failures

**Symptoms:**
- "alembic.util.exc.CommandError" in logs
- Database schema out of sync

**Solutions:**

1. **Check current migration state:**
   ```bash
   docker compose exec faultmaven-backend alembic current
   docker compose exec faultmaven-backend alembic history
   ```

2. **Force migration to latest:**
   ```bash
   docker compose exec faultmaven-backend alembic upgrade head
   ```

3. **Reset migrations (⚠️ DESTRUCTIVE - development only):**
   ```bash
   # Backup database
   cp data/faultmaven.db data/faultmaven.db.backup

   # Remove database and restart
   rm data/faultmaven.db
   ./faultmaven restart
   ```

---

## LLM Provider Issues

### LLM API calls failing

**Symptoms:**
- "Anthropic API Error" / "OpenAI API Error" in logs
- "Rate limit exceeded" errors
- Slow or no responses from AI agent

**Solutions:**

1. **Verify API key is configured:**
   ```bash
   # Check which providers are configured
   grep -E "(OPENAI|ANTHROPIC|GROQ|OLLAMA)" .env
   ```

2. **Test API key manually:**
   ```bash
   # OpenAI
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"

   # Anthropic
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01"
   ```

3. **Check for rate limits:**
   - OpenAI: <https://platform.openai.com/account/rate-limits>
   - Anthropic: <https://console.anthropic.com/>

4. **Switch to alternative provider:**
   ```env
   # In .env, change from:
   LLM_PROVIDER=openai

   # To:
   LLM_PROVIDER=anthropic
   # or
   LLM_PROVIDER=groq  # FREE tier!
   ```

5. **Use local LLM (no API key needed):**
   ```bash
   # Install Ollama: https://ollama.ai/
   ollama run llama3.2
   ```

   In `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

---

## Performance Issues

### Application is slow or unresponsive

**Symptoms:**
- Slow API responses
- High CPU/memory usage
- Containers restarting frequently

**Solutions:**

1. **Check resource usage:**
   ```bash
   docker stats
   ```

   Look for:
   - CPU > 100% (throttling)
   - Memory near limits (OOM risk)
   - High memory % (swap thrashing)

2. **Increase resource limits:**
   ```bash
   cp docker-compose.override.yml.example docker-compose.override.yml
   ```

   Edit `docker-compose.override.yml`:
   ```yaml
   services:
     faultmaven-backend:
       mem_limit: 4096m    # Increase from 2GB to 4GB
       cpus: 4.0           # Increase from 2 to 4 cores
   ```

3. **Check for OOM kills:**
   ```bash
   docker inspect faultmaven-backend | grep OOMKilled
   ```

   If true, increase `mem_limit` in override file.

4. **Reduce concurrent requests:**
   In `.env`:
   ```env
   MAX_SESSIONS_PER_USER=5    # Reduce from 10
   SESSION_MAX_MEMORY_MB=50   # Reduce from 100
   ```

5. **Use faster LLM provider:**
   ```env
   LLM_PROVIDER=groq  # Ultra-fast FREE tier
   ```

### High memory usage

**Solutions:**

1. **Check which container is using memory:**
   ```bash
   docker stats --no-stream
   ```

2. **Restart high-memory container:**
   ```bash
   docker compose restart faultmaven-backend
   ```

3. **Clean up old sessions:**
   ```bash
   # Redis session cleanup
   docker compose exec redis redis-cli FLUSHDB
   ./faultmaven restart
   ```

---

## Data Persistence Issues

### Data lost after restart

**Symptoms:**
- Cases disappear after `docker compose down`
- Knowledge base empty after restart

**Solutions:**

1. **Verify volumes are mounted:**
   ```bash
   docker compose config | grep -A 5 volumes
   ```

   Should show:
   ```yaml
   volumes:
     - ./data:/app/data
   ```

2. **Check `./data` directory exists:**
   ```bash
   ls -la ./data
   ```

   Should contain:
   - `faultmaven.db` (SQLite database)
   - `files/` (uploaded evidence)
   - `chromadb/` (vector embeddings)

3. **Avoid `docker compose down -v`:**
   ```bash
   # WRONG - deletes volumes
   docker compose down -v

   # CORRECT - preserves data
   docker compose down
   ```

4. **Check volume permissions:**
   ```bash
   ls -la ./data
   ```

   Should be writable by Docker (uid 1000 or your user).

### Backup and restore data

**Backup:**
```bash
# Stop services
./faultmaven stop

# Backup everything
tar -czf faultmaven-backup-$(date +%Y%m%d).tar.gz ./data .env

# Restart
./faultmaven start
```

**Restore:**
```bash
# Stop services
./faultmaven stop

# Restore
tar -xzf faultmaven-backup-YYYYMMDD.tar.gz

# Restart
./faultmaven start
```

---

## Getting Help

If you're still stuck after trying these solutions:

### 1. Gather diagnostic information

```bash
# System info
docker version
docker compose version
uname -a

# Service status
./faultmaven status
docker compose ps

# Recent logs
./faultmaven logs --tail 100 > faultmaven-logs.txt

# Resource usage
docker stats --no-stream > docker-stats.txt
```

### 2. Check existing issues

- GitHub Issues: <https://github.com/FaultMaven/faultmaven/issues>
- Search for similar problems

### 3. Create a new issue

Include:
- What you were trying to do
- What happened instead
- Error messages (full stack trace if possible)
- Output from diagnostic commands above
- Your environment (OS, Docker version, RAM)

### 4. Community support

- GitHub Discussions: <https://github.com/FaultMaven/faultmaven/discussions>
- Discord: [Link if available]

---

## Advanced Troubleshooting

### Enable debug logging

In `.env`:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

Restart services:
```bash
./faultmaven restart
```

### Access container shell

```bash
# Development mode
docker compose exec faultmaven-backend bash

# Production mode
docker compose -f docker-compose.prod.yml exec faultmaven bash
```

### Check network connectivity

```bash
# From backend container
docker compose exec faultmaven-backend curl http://redis:6379
docker compose exec faultmaven-backend curl http://chromadb:8000
```

### Nuclear option: Complete reset

⚠️ **WARNING: This deletes ALL data!**

```bash
./faultmaven nuke

# Or manually:
docker compose down --volumes --remove-orphans
docker system prune -af --volumes
rm -rf ./data
rm .env

# Start fresh
cp .env.example .env
# Edit .env with your API keys
./faultmaven start
```

---

## Prevention Tips

1. **Regular backups:**
   ```bash
   # Add to cron/scheduled task
   tar -czf ~/backups/faultmaven-$(date +%Y%m%d).tar.gz ./data .env
   ```

2. **Monitor resources:**
   ```bash
   # Check weekly
   docker stats --no-stream
   ```

3. **Keep Docker updated:**
   ```bash
   docker version  # Should be 20.10+
   ```

4. **Use resource limits:**
   Always use `docker-compose.override.yml` for production deployments.

5. **Test updates in dev:**
   ```bash
   git pull
   docker compose build --no-cache
   docker compose up -d
   ```
