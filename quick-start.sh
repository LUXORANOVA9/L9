#!/bin/bash
# LUXOR AI CUA - 快速启动脚本
# Quick Start Script for LUXOR AI CUA System

set -e

# 颜色输出函数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# 项目配置
PROJECT_NAME="luxor-ai-cua"
PROJECT_VERSION="1.0.0"
GITHUB_REPO="https://github.com/luxor-ai/luxor-cua.git"

# 显示欢迎信息
show_banner() {
    echo -e "${BLUE}"
    cat << "EOF"
╦  ╦ ╦═╗ ╦╔═╗╦═╗  ╔═╗╦  ╔═╗╦ ╦╔╗ 
║  ║ ║╔╩╦╝║ ║╠╦╝  ║  ║  ║ ║║ ║ ║║
╩═╝╚╝╩ ╚═╚═╝╩╚═  ╚═╝╩═╝╚═╝╚╝╚╝╚╝
Chinese AI Agentic CUA Cloud System
EOF
    echo -e "${NC}"
    echo "🚀 欢迎使用 LUXOR AI CUA 开源云系统！"
    echo "📖 版本: $PROJECT_VERSION"
    echo "🌟 让AI帮你从自然语言创建完整的创业项目！"
    echo ""
}

# 检查系统要求
check_requirements() {
    info "检查系统要求..."
    
    local missing_tools=()
    
    # 检查必需的工具
    tools=("docker" "docker-compose" "git" "curl" "python3" "node" "npm")
    
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -eq 0 ]; then
        success "所有必需的工具都已安装"
    else
        error "缺少以下工具: ${missing_tools[*]}"
        info "请安装缺少的工具后重新运行此脚本"
        exit 1
    fi
    
    # 检查系统资源
    total_memory=$(free -m | awk '/^Mem:/{print $2}')
    if [ "$total_memory" -lt 8192 ]; then
        warn "建议至少 8GB 内存，当前: ${total_memory}MB"
    fi
    
    available_space=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_space" -lt 20 ]; then
        warn "建议至少 20GB 可用磁盘空间，当前: ${available_space}GB"
    fi
}

# 选择安装模式
select_installation_mode() {
    info "选择安装模式:"
    echo "1) 🚀 快速体验模式 (单机Docker Compose)"
    echo "2) 🏭 生产环境模式 (Kubernetes集群)"
    echo "3) 👨‍💻 开发者模式 (本地开发环境)"
    echo "4) ☁️  云服务模式 (云平台部署)"
    echo ""
    
    while true; do
        read -p "请选择安装模式 [1-4]: " mode
        case $mode in
            1) INSTALL_MODE="quick"; break;;
            2) INSTALL_MODE="production"; break;;
            3) INSTALL_MODE="development"; break;;
            4) INSTALL_MODE="cloud"; break;;
            *) warn "请输入有效的选择 [1-4]";;
        esac
    done
    
    success "选择了安装模式: $INSTALL_MODE"
}

# 配置项目参数
configure_project() {
    info "配置项目参数..."
    
    # 默认配置
    DB_PASSWORD="luxor-ai-2024"
    REDIS_PASSWORD=""
    JWT_SECRET="your-super-secret-jwt-key-change-in-production"
    
    # 如果是生产环境，提示用户更改默认密码
    if [ "$INSTALL_MODE" = "production" ]; then
        warn "生产环境部署，建议更改默认配置"
        read -p "数据库密码 (默认: $DB_PASSWORD): " input_db_pass
        [ -n "$input_db_pass" ] && DB_PASSWORD="$input_db_pass"
        
        read -p "Redis密码 (可选): " input_redis_pass
        [ -n "$input_redis_pass" ] && REDIS_PASSWORD="$input_redis_pass"
    fi
    
    # 创建环境变量文件
    cat > .env << EOF
# LUXOR AI CUA 环境配置
PROJECT_NAME=$PROJECT_NAME
VERSION=$PROJECT_VERSION

# 数据库配置
DATABASE_URL=postgresql://luxor:$DB_PASSWORD@postgres:5432/luxor_ai
POSTGRES_DB=luxor_ai
POSTGRES_USER=luxor
POSTGRES_PASSWORD=$DB_PASSWORD

# Redis配置
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=$REDIS_PASSWORD

# API配置
API_HOST=0.0.0.0
API_PORT=8000
JWT_SECRET=$JWT_SECRET

# 前端配置
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=$PROJECT_VERSION

# AI模型配置
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
CHINESE_MODEL_PATH=./models/chatglm3-6b

# 监控配置
ENABLE_MONITORING=true
GRAFANA_ADMIN_PASSWORD=admin123
EOF
    
    success "项目配置完成"
}

# 下载/克隆项目代码
setup_project() {
    info "设置项目代码..."
    
    if [ -d "$PROJECT_NAME" ]; then
        warn "项目目录 $PROJECT_NAME 已存在"
        read -p "是否删除并重新创建? [y/N]: " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_NAME"
        else
            info "使用现有项目目录"
            cd "$PROJECT_NAME"
            return
        fi
    fi
    
    # 创建项目结构
    mkdir -p "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    # 由于这是一个新项目，我们创建基础结构
    create_project_structure
    
    success "项目代码设置完成"
}

# 创建项目基础结构
create_project_structure() {
    info "创建项目基础结构..."
    
    # 创建目录结构
    mkdir -p {backend/{core,api,services,models,utils,config},frontend/src/{components,pages,hooks,services,types,utils},infrastructure/{kubernetes,terraform,ansible,helm-charts},docs,tests,scripts,monitoring}
    
    # 创建基础文件
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=${REACT_APP_API_URL}
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF
    
    # 创建后端基础文件
    create_backend_files
    
    # 创建前端基础文件
    create_frontend_files
    
    # 创建nginx配置
    create_nginx_config
    
    success "项目结构创建完成"
}

# 创建后端基础文件
create_backend_files() {
    # requirements.txt
    cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
transformers==4.35.2
torch==2.1.1
langchain==0.0.340
openai==1.3.7
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
EOF

    # main.py
    cat > backend/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(
    title="LUXOR AI CUA API",
    description="Chinese AI Agentic Conversational User Agent",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to LUXOR AI CUA API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(message: dict):
    # TODO: 实现AI聊天逻辑
    return {"response": f"我收到了你的消息: {message.get('content', '')}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF

    # Dockerfile
    cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
}

# 创建前端基础文件
create_frontend_files() {
    # package.json
    cat > frontend/package.json << 'EOF'
{
  "name": "luxor-ai-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@tanstack/react-query": "^5.0.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "react-scripts": "5.0.1"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
EOF

    # public/index.html
    mkdir -p frontend/public
    cat > frontend/public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>LUXOR AI CUA</title>
    <meta name="description" content="中文AI智能体云系统" />
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
EOF

    # src/App.tsx
    mkdir -p frontend/src
    cat > frontend/src/App.tsx << 'EOF'
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>LUXOR AI CUA</h1>
        <p>中文AI智能体云系统</p>
        <p>🚀 让AI帮你创建完整的创业项目！</p>
      </header>
    </div>
  );
}

export default App;
EOF

    # src/index.tsx
    cat > frontend/src/index.tsx << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

    # src/App.css
    cat > frontend/src/App.css << 'EOF'
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
}
EOF

    # src/index.css
    cat > frontend/src/index.css << 'EOF'
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
EOF

    # Dockerfile
    cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
EOF
}

# 创建nginx配置
create_nginx_config() {
    mkdir -p nginx
    cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    server {
        listen 80;
        
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location / {
            proxy_pass http://frontend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF
}

# 根据模式执行安装
install_based_on_mode() {
    case $INSTALL_MODE in
        "quick")
            install_quick_mode
            ;;
        "production")
            install_production_mode
            ;;
        "development")
            install_development_mode
            ;;
        "cloud")
            install_cloud_mode
            ;;
    esac
}

# 快速体验模式
install_quick_mode() {
    info "🚀 启动快速体验模式..."
    
    # 启动Docker Compose
    docker-compose up -d
    
    success "快速体验环境已启动!"
    show_access_info
}

# 生产环境模式
install_production_mode() {
    info "🏭 设置生产环境..."
    
    warn "生产环境需要Kubernetes集群"
    read -p "是否继续? [y/N]: " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        info "取消生产环境安装"
        return
    fi
    
    # 创建Kubernetes配置文件
    create_k8s_configs
    
    # 部署到Kubernetes
    kubectl apply -f infrastructure/kubernetes/
    
    success "生产环境部署完成!"
}

# 开发者模式
install_development_mode() {
    info "👨‍💻 设置开发环境..."
    
    # 安装后端依赖
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # 安装前端依赖
    cd frontend
    npm install
    cd ..
    
    success "开发环境设置完成!"
    info "后端启动: cd backend && source venv/bin/activate && python main.py"
    info "前端启动: cd frontend && npm start"
}

# 云服务模式
install_cloud_mode() {
    info "☁️ 云服务部署..."
    
    echo "选择云服务提供商:"
    echo "1) 阿里云 (Alibaba Cloud)"
    echo "2) 腾讯云 (Tencent Cloud)"
    echo "3) AWS"
    echo "4) Azure"
    
    read -p "请选择 [1-4]: " cloud_provider
    
    case $cloud_provider in
        1) deploy_to_alibaba_cloud;;
        2) deploy_to_tencent_cloud;;
        3) deploy_to_aws;;
        4) deploy_to_azure;;
        *) warn "暂不支持该云服务商";;
    esac
}

# 创建Kubernetes配置
create_k8s_configs() {
    mkdir -p infrastructure/kubernetes
    
    # 这里创建基础的K8s配置文件
    # 实际实现会更复杂，包含完整的部署配置
    info "创建Kubernetes配置文件..."
}

# 显示访问信息
show_access_info() {
    echo ""
    success "🎉 LUXOR AI CUA 安装完成!"
    echo ""
    info "访问信息:"
    echo "🌐 前端页面: http://localhost"
    echo "🔧 API文档: http://localhost/docs"
    echo "📊 健康检查: http://localhost/health"
    echo ""
    info "管理命令:"
    echo "📋 查看状态: docker-compose ps"
    echo "📜 查看日志: docker-compose logs"
    echo "⏹️  停止服务: docker-compose down"
    echo "🔄 重启服务: docker-compose restart"
    echo ""
    warn "首次启动可能需要几分钟来下载和构建镜像"
}

# 主函数
main() {
    show_banner
    check_requirements
    select_installation_mode
    configure_project
    setup_project
    install_based_on_mode
}

# 如果脚本被直接执行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi