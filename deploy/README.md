# FaultMaven Deployment Guide

This directory contains all deployment configurations and guides for FaultMaven.

## 📂 Directory Structure

```
deploy/
├── docker/              # Docker-based deployment (recommended)
├── local/               # Local development from source
├── kubernetes/          # Kubernetes/Helm deployment (coming soon)
└── troubleshooting/     # Deployment troubleshooting guides
```

---

## 🐳 Docker Deployment (Recommended)

**Location:** [docker/](docker/)

The easiest way to deploy FaultMaven. Two modes available:

### Development Mode (4 containers)
- Backend API on port 8000
- Dashboard on port 3000
- Redis + ChromaDB

```bash
./faultmaven start
```

### Production Mode (3 containers)
- Unified application on port 8090
- Redis + ChromaDB

```bash
./faultmaven --prod start
```

**See:** [docker/README.md](docker/README.md) for detailed Docker deployment guide.

---

## 💻 Local Development

**Location:** [local/](local/)
**Status:** ✅ Ready

Run FaultMaven from source code for active development:

- Hot-reload for backend and frontend
- Direct database access for debugging
- Full IDE integration
- Requires: Python 3.11+, Node 20+, Docker (for Redis/ChromaDB)

**Best for:**
- Contributing to FaultMaven
- Custom modifications
- Debugging issues

---

## ☸️ Kubernetes Deployment

**Location:** [kubernetes/](kubernetes/)
**Status:** 🚧 Coming soon

Production-grade orchestrated deployment:

- Helm charts for easy installation
- Horizontal scaling support
- Production-ready configurations
- Monitoring and observability built-in

**Best for:**
- Enterprise production deployments
- Multi-node clusters
- High availability requirements

---

## 🛠️ Troubleshooting

**Location:** [troubleshooting/](troubleshooting/)

Comprehensive troubleshooting guides for common deployment issues:

- Startup problems
- Port conflicts
- Database errors
- LLM provider issues
- Performance tuning
- Data persistence

**Start here:** [troubleshooting/README.md](troubleshooting/README.md)

---

## Quick Start

**Never deployed FaultMaven before?**

1. Choose Docker deployment (easiest)
2. Follow the main [README.md](../README.md) Quick Start
3. Run `./faultmaven start`
4. Access dashboard at <http://localhost:3000>

**Questions?**
- See [troubleshooting/](troubleshooting/) for common issues
- Check [GitHub Discussions](https://github.com/FaultMaven/faultmaven/discussions)
- Open an [issue](https://github.com/FaultMaven/faultmaven/issues) if stuck

---

## Deployment Comparison

| Method | Complexity | Use Case | Status |
|--------|------------|----------|--------|
| **Docker** | ⭐ Easy | Production, local testing | ✅ Ready |
| **Local** | ⭐⭐ Medium | Development, debugging | ✅ Ready |
| **Kubernetes** | ⭐⭐⭐ Advanced | Enterprise, HA | 🚧 Planned |

---

## Contributing

Deployment improvements welcome!

- Found a better Docker optimization? PR it!
- Have Kubernetes experience? Help us build the Helm chart!
- Wrote a deployment guide for your platform? Share it!

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
