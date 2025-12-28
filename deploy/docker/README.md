# Docker Deployment Guide

Docker-based deployment for FaultMaven. Choose between development and production modes.

## Files in This Directory

```
docker/
├── docker-compose.yml          # Development mode (4 containers)
├── docker-compose.prod.yml     # Production mode (3 containers)
├── Dockerfile.production       # Multi-stage build (dashboard + backend)
├── docker-entrypoint.sh        # Automatic database migrations
├── .dockerignore.production    # Production build exclusions
└── examples/
    └── resource-limits.yml     # Resource limit examples
```

---

## Development Mode

**4 containers:** backend, dashboard, redis, chromadb

### Quick Start

```bash
# From repository root
./faultmaven start
```

### Access Points

- **Dashboard:** <http://localhost:3000>
- **API:** <http://localhost:8000>
- **API Docs:** <http://localhost:8000/docs>

### Architecture

```
┌─────────────┐     ┌──────────────┐
│  Dashboard  │────▶│   Backend    │
│  (Port 3000)│     │  (Port 8000) │
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │              │
               ┌────▼────┐   ┌─────▼─────┐
               │  Redis  │   │ ChromaDB  │
               │ (Cache) │   │ (Vectors) │
               └─────────┘   └───────────┘
```

### When to Use

- Local development with hot-reload
- Testing dashboard changes
- Full separation of concerns
- Easier debugging (separate logs per service)

---

## Production Mode

**3 containers:** unified app, redis, chromadb

### Quick Start

```bash
# From repository root
./faultmaven --prod start
```

### Access Points

- **Unified App:** <http://localhost:8090>
- **API Docs:** <http://localhost:8090/docs>

### Architecture

```
┌────────────────────────┐
│    FaultMaven Core     │
│   (Port 8090)          │
│  ┌──────┬──────────┐   │
│  │ API  │Dashboard │   │
│  └──┬───┴────┬─────┘   │
└─────┼────────┼─────────┘
      │        │
  ┌───▼────┐ ┌▼────────┐
  │ Redis  │ │ChromaDB │
  └────────┘ └─────────┘
```

### When to Use

- Production deployments
- Single-container simplicity
- Lower resource usage (one less container)
- Simpler networking (one port instead of two)

---

## Build Details

### Multi-Stage Dockerfile

The [Dockerfile.production](Dockerfile.production) uses two build stages:

**Stage 1: Dashboard Builder**
- Base: `node:20-alpine`
- Installs pnpm
- Builds React dashboard with Vite
- Output: `dist/` directory

**Stage 2: Production Image**
- Base: `python:3.11-slim`
- Installs Python dependencies
- Copies backend code
- Copies dashboard from Stage 1
- Runs as non-root user for security

### Automated Migrations

[docker-entrypoint.sh](docker-entrypoint.sh) automatically runs `alembic upgrade head` on startup, ensuring database schema is always up-to-date.

---

## Resource Limits

### Default Limits (Development)

No limits by default. For systems with limited RAM, use override:

```bash
cp deploy/docker/examples/resource-limits.yml docker-compose.override.yml
```

**Recommended limits:**
- Backend: 2GB RAM, 2 CPUs
- Dashboard: 512MB RAM, 0.5 CPUs
- Redis: 512MB RAM, 0.25 CPUs
- ChromaDB: 1GB RAM, 0.5 CPUs

### Custom Configuration

Create `docker-compose.override.yml` in the repository root:

```yaml
services:
  faultmaven-backend:
    ports:
      - "8080:8000"  # Change port if 8000 conflicts
    mem_limit: 4096m  # Increase if needed
```

---

## Networking

### Port Mapping

**Development:**
- 8000: Backend API
- 3000: Dashboard
- 6379: Redis (localhost only)
- 8001: ChromaDB (localhost only)

**Production:**
- 8090: Unified application
- 6379: Redis (localhost only)
- 8001: ChromaDB (localhost only)

### Remote Access

To access FaultMaven from other machines on your network:

1. **Set SERVER_HOST in .env:**
   ```env
   SERVER_HOST=192.168.1.100  # Your machine's IP address
   ```

2. **Restart:**
   ```bash
   ./faultmaven restart
   ```

3. **Access from other machines:**
   - **Development Mode:** `http://192.168.1.100:3000` (dashboard) and `http://192.168.1.100:8000` (API)
   - **Production Mode:** `http://192.168.1.100:8090` (unified)

> **Note:** CORS is configured to allow all origins by default for development convenience. For production, consider restricting CORS in `src/faultmaven/app.py`.

---

## Data Persistence

All data persists in `./data/` directory:

```
./data/
├── faultmaven.db      # SQLite database (cases, sessions, etc.)
├── files/             # Uploaded evidence files
└── chromadb/          # Vector embeddings
```

### Backup

```bash
./faultmaven stop
tar -czf faultmaven-backup-$(date +%Y%m%d).tar.gz ./data .env
./faultmaven start
```

### Restore

```bash
./faultmaven stop
tar -xzf faultmaven-backup-YYYYMMDD.tar.gz
./faultmaven start
```

---

## Troubleshooting

See [../troubleshooting/README.md](../troubleshooting/README.md) for:
- Startup issues
- Port conflicts
- Database errors
- Performance tuning
- Complete troubleshooting guide

---

## Advanced

### Custom Docker Compose

For complex setups, extend the compose files:

```bash
docker compose -f deploy/docker/docker-compose.yml \
               -f my-custom-compose.yml \
               up -d
```

### Build from Source

```bash
docker compose -f deploy/docker/docker-compose.prod.yml build --no-cache
```

### View Build Logs

```bash
docker compose -f deploy/docker/docker-compose.prod.yml build 2>&1 | tee build.log
```

---

## Support

- **Quick help:** `./faultmaven help`
- **Troubleshooting:** [../troubleshooting/](../troubleshooting/)
- **Issues:** <https://github.com/FaultMaven/faultmaven/issues>
- **Discussions:** <https://github.com/FaultMaven/faultmaven/discussions>
