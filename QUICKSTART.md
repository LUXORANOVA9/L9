# 🚀 LUXORANOVA Quick Start Guide

Get LUXORANOVA up and running in minutes!

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.11+** installed
- **Node.js 18+** installed
- **Docker & Docker Compose** installed
- **Git** installed

## ⚡ Quick Start (Docker - Recommended)

### 1. Clone & Configure

```bash
# Clone repository
git clone https://github.com/yourusername/luxoranova.git
cd luxoranova

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (required)
# At minimum, set:
# - OPENAI_API_KEY or ANTHROPIC_API_KEY
# - POSTGRES_PASSWORD
# - JWT_SECRET_KEY
```

### 2. Start All Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **N8N Workflows**: http://localhost:5678
- **Grafana Dashboards**: http://localhost:3001
- **Prometheus Metrics**: http://localhost:9090

### 4. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove data (⚠️ deletes everything)
docker-compose down -v
```

---

## 🛠️ Local Development Setup

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\scripts\setup.ps1
```

**Linux/macOS:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup (Coming in Phase 6)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Agent Orchestrator (Coming in Phase 7)

```bash
cd agent-orchestrator

# Install dependencies
npm install

# Start orchestrator
npm run dev
```

---

## 🧪 Testing

### Test Foundation

```bash
# Run foundation tests
python scripts/test_foundation.py
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/api/docs
```

---

## 📚 Next Steps

### 1. Configure AI Models

Edit `.env` and add your API keys:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-opus-20240229

# Ollama (Local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 2. Create Your First Agent

```bash
# Using API
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Agent",
    "description": "A helpful AI assistant",
    "agent_type": "worker",
    "model_provider": "openai",
    "model_name": "gpt-4-turbo-preview"
  }'
```

### 3. Execute a Task

```bash
# Create and execute a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Task",
    "description": "My first task",
    "agent_id": 1,
    "input_data": {
      "prompt": "Hello, world!"
    }
  }'
```

### 4. Create a Workflow

```bash
# Create a workflow
curl -X POST http://localhost:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Workflow",
    "description": "Automated workflow",
    "trigger_type": "manual"
  }'
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8000

# Linux/macOS:
lsof -i :8000

# Kill the process or change port in .env
```

### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Redis Connection Failed

```bash
# Check if Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Module Not Found Errors

```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Or rebuild Docker images
docker-compose build --no-cache
```

---

## 📖 Documentation

- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Deployment**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **API Reference**: http://localhost:8000/api/docs
- **Full README**: [README.md](README.md)

---

## 🆘 Getting Help

- **Documentation**: https://docs.luxoranova.io
- **Discord Community**: https://discord.gg/luxoranova
- **GitHub Issues**: https://github.com/yourusername/luxoranova/issues
- **Email Support**: support@luxoranova.io

---

## 🎯 What's Next?

### Current Status: Phase 1 Complete ✅

**Completed:**
- ✅ Project structure and documentation
- ✅ Docker Compose setup
- ✅ Backend core (FastAPI, database, Redis)
- ✅ Database models (User, Agent, Task, Workflow)
- ✅ Configuration management
- ✅ Logging system

**Coming Next (Phase 2):**
- 🚧 API endpoints and routes
- 🚧 Authentication system (JWT, OAuth2)
- 🚧 Service layer implementation
- 🚧 Middleware components

**Future Phases:**
- Phase 3: AI Agent System
- Phase 4: Computer Use Service
- Phase 5: MCP Integration
- Phase 6: Frontend Application
- Phase 7: Agent Orchestrator
- Phase 8-12: Advanced features

See [TODO.md](TODO.md) for complete roadmap.

---

**Happy Building! 🚀**

For detailed information, see the full documentation in the `docs/` directory.
