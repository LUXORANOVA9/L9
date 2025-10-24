# LUXOR AI CUA - 项目结构模板
## Project Structure Templates

### 📁 完整项目目录结构

```
luxor-ai-cua/
├── 📁 backend/                     # 后端服务
│   ├── 📁 core/                    # 核心AI引擎
│   │   ├── agent_engine.py         # 智能体引擎
│   │   ├── nlp_processor.py        # 中文NLP处理
│   │   ├── memory_manager.py       # 上下文记忆管理
│   │   ├── code_generator.py       # 代码生成引擎
│   │   └── deployment_manager.py   # 部署管理器
│   ├── 📁 api/                     # API接口层
│   │   ├── routes/                 # 路由定义
│   │   ├── middleware/             # 中间件
│   │   └── schemas/                # 数据模型
│   ├── 📁 services/                # 业务服务层
│   │   ├── project_service.py      # 项目管理服务
│   │   ├── user_service.py         # 用户管理服务
│   │   └── deployment_service.py   # 部署服务
│   ├── 📁 models/                  # 数据模型
│   ├── 📁 utils/                   # 工具函数
│   ├── 📁 config/                  # 配置文件
│   ├── requirements.txt            # Python依赖
│   ├── Dockerfile                  # Docker构建文件
│   └── main.py                     # 应用入口
├── 📁 frontend/                    # 前端应用
│   ├── 📁 src/
│   │   ├── 📁 components/          # React组件
│   │   │   ├── chat/               # 聊天界面组件
│   │   │   ├── project/            # 项目管理组件
│   │   │   ├── dashboard/          # 仪表板组件
│   │   │   └── common/             # 通用组件
│   │   ├── 📁 pages/               # 页面组件
│   │   ├── 📁 hooks/               # 自定义Hooks
│   │   ├── 📁 services/            # API服务
│   │   ├── 📁 stores/              # 状态管理(Zustand)
│   │   ├── 📁 types/               # TypeScript类型定义
│   │   ├── 📁 utils/               # 工具函数
│   │   └── App.tsx                 # 根组件
│   ├── package.json                # Node.js依赖
│   ├── tsconfig.json              # TypeScript配置
│   ├── tailwind.config.js         # Tailwind CSS配置
│   ├── vite.config.ts             # Vite构建配置
│   └── Dockerfile                 # Docker构建文件
├── 📁 infrastructure/              # 基础设施代码
│   ├── 📁 kubernetes/              # K8s部署文件
│   │   ├── 📁 core-services/       # 核心服务配置
│   │   ├── 📁 monitoring/          # 监控配置
│   │   ├── 📁 ingress/             # 入口配置
│   │   └── 📁 storage/             # 存储配置
│   ├── 📁 terraform/               # Terraform IaC
│   │   ├── modules/                # Terraform模块
│   │   ├── environments/           # 环境配置
│   │   └── main.tf                 # 主配置文件
│   ├── 📁 ansible/                 # Ansible自动化
│   │   ├── playbooks/              # 剧本文件
│   │   ├── roles/                  # 角色定义
│   │   └── inventory/              # 主机清单
│   └── 📁 helm-charts/             # Helm图表
│       ├── luxor-ai-core/          # 核心服务图表
│       └── luxor-ai-frontend/      # 前端服务图表
├── 📁 ai-models/                   # AI模型文件
│   ├── 📁 chinese-nlp/             # 中文NLP模型
│   ├── 📁 code-generation/         # 代码生成模型
│   ├── 📁 fine-tuned/              # 微调模型
│   └── 📁 embeddings/              # 向量嵌入模型
├── 📁 templates/                   # 代码模板库
│   ├── 📁 backend-templates/       # 后端模板
│   │   ├── fastapi/                # FastAPI项目模板
│   │   ├── spring-boot/            # Spring Boot模板
│   │   └── nodejs/                 # Node.js模板
│   ├── 📁 frontend-templates/      # 前端模板
│   │   ├── react-ts/               # React+TypeScript模板
│   │   ├── vue3-ts/                # Vue3+TypeScript模板
│   │   └── nextjs/                 # Next.js模板
│   ├── 📁 database-schemas/        # 数据库模式模板
│   └── 📁 deployment-configs/      # 部署配置模板
├── 📁 docs/                        # 文档
│   ├── 📁 api/                     # API文档
│   ├── 📁 architecture/            # 架构文档
│   ├── 📁 deployment/              # 部署文档
│   ├── 📁 user-guide/              # 用户指南
│   └── README.md                   # 项目说明
├── 📁 tests/                       # 测试代码
│   ├── 📁 unit/                    # 单元测试
│   ├── 📁 integration/             # 集成测试
│   ├── 📁 e2e/                     # 端到端测试
│   └── 📁 performance/             # 性能测试
├── 📁 scripts/                     # 脚本文件
│   ├── setup.sh                   # 环境设置脚本
│   ├── deploy.sh                  # 部署脚本
│   ├── backup.sh                  # 备份脚本
│   └── health-check.sh            # 健康检查脚本
├── 📁 monitoring/                  # 监控配置
│   ├── 📁 prometheus/              # Prometheus配置
│   ├── 📁 grafana/                 # Grafana仪表板
│   ├── 📁 alerts/                  # 告警规则
│   └── 📁 logs/                    # 日志配置
├── 📁 security/                    # 安全配置
│   ├── 📁 certificates/            # 证书文件
│   ├── 📁 policies/                # 安全策略
│   └── 📁 rbac/                    # 权限控制
├── .github/                       # GitHub配置
│   ├── workflows/                  # GitHub Actions
│   ├── ISSUE_TEMPLATE/             # Issue模板
│   └── PULL_REQUEST_TEMPLATE.md    # PR模板
├── docker-compose.yml             # 本地开发环境
├── docker-compose.prod.yml        # 生产环境
├── Makefile                       # 构建脚本
├── README.md                      # 项目说明
├── LICENSE                        # 开源许可证
└── CONTRIBUTING.md                # 贡献指南
```

### 🎯 核心组件代码模板

#### 1. FastAPI 后端项目模板

```python
# templates/backend-templates/fastapi/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="{{project_name}} API",
    description="{{project_description}}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全配置
security = HTTPBearer()

# 数据模型
class {{model_name}}(BaseModel):
    {{#each fields}}
    {{name}}: {{type}}
    {{/each}}

class {{model_name}}Create(BaseModel):
    {{#each create_fields}}
    {{name}}: {{type}}
    {{/each}}

class {{model_name}}Update(BaseModel):
    {{#each update_fields}}
    {{name}}: Optional[{{type}}] = None
    {{/each}}

# 依赖注入
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # 这里实现用户认证逻辑
    return {"user_id": "user123", "username": "demo"}

# API 路由
@app.get("/")
async def root():
    return {"message": "Welcome to {{project_name}} API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/{{plural_model_name}}", response_model=List[{{model_name}}])
async def get_{{plural_model_name}}(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user)
):
    # 这里实现获取列表的逻辑
    return []

@app.post("/{{plural_model_name}}", response_model={{model_name}})
async def create_{{model_name}}(
    {{model_name_lower}}: {{model_name}}Create,
    current_user = Depends(get_current_user)
):
    # 这里实现创建逻辑
    return {{model_name}}(**{{model_name_lower}}.dict())

@app.get("/{{plural_model_name}}/{item_id}", response_model={{model_name}})
async def get_{{model_name}}(
    item_id: str,
    current_user = Depends(get_current_user)
):
    # 这里实现获取单个项目的逻辑
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/{{plural_model_name}}/{item_id}", response_model={{model_name}})
async def update_{{model_name}}(
    item_id: str,
    {{model_name_lower}}: {{model_name}}Update,
    current_user = Depends(get_current_user)
):
    # 这里实现更新逻辑
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/{{plural_model_name}}/{item_id}")
async def delete_{{model_name}}(
    item_id: str,
    current_user = Depends(get_current_user)
):
    # 这里实现删除逻辑
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

```dockerfile
# templates/backend-templates/fastapi/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. React TypeScript 前端模板

```tsx
// templates/frontend-templates/react-ts/src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from 'react-hot-toast';

// 页面组件
import HomePage from './pages/HomePage';
import {{#each pages}}
import {{name}}Page from './pages/{{name}}Page';
{{/each}}

// 布局组件
import Layout from './components/layout/Layout';
import AuthProvider from './providers/AuthProvider';

// 样式
import './App.css';

// 创建 React Query 客户端
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                {{#each routes}}
                <Route path="{{path}}" element={<{{component}} />} />
                {{/each}}
              </Routes>
            </Layout>
          </div>
        </Router>
      </AuthProvider>
      
      {/* Toast 通知 */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      {/* React Query 开发工具 */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
```

```tsx
// templates/frontend-templates/react-ts/src/components/layout/Layout.tsx
import React, { ReactNode } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <div className="flex flex-1">
        <Sidebar />
        
        <main className="flex-1 p-6 bg-gray-50">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
      
      <Footer />
    </div>
  );
};

export default Layout;
```

```typescript
// templates/frontend-templates/react-ts/src/services/api.ts
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { toast } from 'react-hot-toast';

// API 基础配置
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 添加认证 token
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // 处理错误响应
    if (error.response?.status === 401) {
      // 未认证，跳转到登录页
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    } else if (error.response?.status >= 500) {
      toast.error('服务器错误，请稍后重试');
    } else if (error.response?.data?.message) {
      toast.error(error.response.data.message);
    }
    
    return Promise.reject(error);
  }
);

// API 接口定义
export interface {{model_name}} {
  {{#each fields}}
  {{name}}: {{type}};
  {{/each}}
}

export interface {{model_name}}CreateRequest {
  {{#each create_fields}}
  {{name}}: {{type}};
  {{/each}}
}

export interface {{model_name}}UpdateRequest {
  {{#each update_fields}}
  {{name}}?: {{type}};
  {{/each}}
}

// API 服务类
export class {{model_name}}Service {
  private static basePath = '/{{plural_model_name}}';

  static async getAll(params?: {
    skip?: number;
    limit?: number;
  }): Promise<{{model_name}}[]> {
    const response = await apiClient.get(this.basePath, { params });
    return response.data;
  }

  static async getById(id: string): Promise<{{model_name}}> {
    const response = await apiClient.get(`${this.basePath}/${id}`);
    return response.data;
  }

  static async create(data: {{model_name}}CreateRequest): Promise<{{model_name}}> {
    const response = await apiClient.post(this.basePath, data);
    return response.data;
  }

  static async update(id: string, data: {{model_name}}UpdateRequest): Promise<{{model_name}}> {
    const response = await apiClient.put(`${this.basePath}/${id}`, data);
    return response.data;
  }

  static async delete(id: string): Promise<void> {
    await apiClient.delete(`${this.basePath}/${id}`);
  }
}

export default apiClient;
```

#### 3. Kubernetes 部署模板

```yaml
# templates/deployment-configs/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{app_name}}
  namespace: {{namespace}}
  labels:
    app: {{app_name}}
    version: {{version}}
spec:
  replicas: {{replicas}}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: {{app_name}}
  template:
    metadata:
      labels:
        app: {{app_name}}
        version: {{version}}
    spec:
      containers:
      - name: {{container_name}}
        image: {{image_name}}:{{image_tag}}
        ports:
        - containerPort: {{container_port}}
          name: http
        env:
        {{#each env_vars}}
        - name: {{name}}
          value: "{{value}}"
        {{/each}}
        {{#if secrets}}
        {{#each secrets}}
        - name: {{env_name}}
          valueFrom:
            secretKeyRef:
              name: {{secret_name}}
              key: {{secret_key}}
        {{/each}}
        {{/if}}
        resources:
          requests:
            memory: "{{memory_request}}"
            cpu: "{{cpu_request}}"
          limits:
            memory: "{{memory_limit}}"
            cpu: "{{cpu_limit}}"
        livenessProbe:
          httpGet:
            path: {{health_check_path}}
            port: {{container_port}}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: {{readiness_check_path}}
            port: {{container_port}}
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        {{#each volume_mounts}}
        - name: {{name}}
          mountPath: {{mount_path}}
        {{/each}}
      volumes:
      {{#each volumes}}
      - name: {{name}}
        {{#if config_map}}
        configMap:
          name: {{config_map}}
        {{/if}}
        {{#if secret}}
        secret:
          secretName: {{secret}}
        {{/if}}
        {{#if persistent_volume}}
        persistentVolumeClaim:
          claimName: {{persistent_volume}}
        {{/if}}
      {{/each}}
---
apiVersion: v1
kind: Service
metadata:
  name: {{service_name}}
  namespace: {{namespace}}
  labels:
    app: {{app_name}}
spec:
  selector:
    app: {{app_name}}
  ports:
  - name: http
    port: {{service_port}}
    targetPort: {{container_port}}
    protocol: TCP
  type: {{service_type}}
  {{#if load_balancer_ip}}
  loadBalancerIP: {{load_balancer_ip}}
  {{/if}}
```

#### 4. Docker Compose 开发环境模板

```yaml
# templates/deployment-configs/docker-compose.dev.yml
version: '3.8'

services:
  # 数据库服务
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: {{db_name}}
      POSTGRES_USER: {{db_user}}
      POSTGRES_PASSWORD: {{db_password}}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {{db_user}} -d {{db_name}}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis 缓存
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://{{db_user}}:{{db_password}}@postgres:5432/{{db_name}}
      - REDIS_URL=redis://redis:6379
      - DEBUG=true
      - LOG_LEVEL=debug
    volumes:
      - ./backend:/app
      - /app/node_modules
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - CHOKIDAR_USEPOLLING=true
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: {{project_name}}-network
```

### 🚀 代码生成器配置

```yaml
# templates/generator-config.yaml
project_templates:
  fullstack_web_app:
    name: "全栈Web应用"
    description: "包含前后端的完整Web应用模板"
    components:
      - backend_api
      - frontend_spa
      - database
      - docker_compose
    
  microservice_api:
    name: "微服务API"
    description: "单个微服务API模板"
    components:
      - backend_api
      - database
      - kubernetes_deployment
    
  static_website:
    name: "静态网站"
    description: "纯前端静态网站模板"
    components:
      - frontend_spa
      - static_hosting

backend_frameworks:
  fastapi:
    language: python
    template_path: "backend-templates/fastapi"
    dependencies:
      - fastapi
      - uvicorn
      - sqlalchemy
      - alembic
      - pydantic
      - python-multipart
    
  spring_boot:
    language: java
    template_path: "backend-templates/spring-boot"
    dependencies:
      - spring-boot-starter-web
      - spring-boot-starter-data-jpa
      - spring-boot-starter-security
      - postgresql
    
  express_js:
    language: typescript
    template_path: "backend-templates/express-ts"
    dependencies:
      - express
      - typescript
      - typeorm
      - jsonwebtoken
      - bcryptjs

frontend_frameworks:
  react_ts:
    language: typescript
    template_path: "frontend-templates/react-ts"
    dependencies:
      - react
      - typescript
      - tailwindcss
      - react-router-dom
      - "@tanstack/react-query"
      - axios
    
  vue3_ts:
    language: typescript
    template_path: "frontend-templates/vue3-ts"
    dependencies:
      - vue
      - typescript
      - vue-router
      - pinia
      - axios
    
  nextjs:
    language: typescript
    template_path: "frontend-templates/nextjs"
    dependencies:
      - next
      - react
      - typescript
      - tailwindcss

databases:
  postgresql:
    type: relational
    template_path: "database-schemas/postgresql"
    
  mongodb:
    type: document
    template_path: "database-schemas/mongodb"
    
  redis:
    type: cache
    template_path: "database-schemas/redis"

deployment_targets:
  kubernetes:
    template_path: "deployment-configs/kubernetes"
    files:
      - deployment.yaml
      - service.yaml
      - ingress.yaml
      - configmap.yaml
    
  docker_compose:
    template_path: "deployment-configs/docker-compose"
    files:
      - docker-compose.yml
      - docker-compose.prod.yml
    
  cloud_functions:
    template_path: "deployment-configs/serverless"
    files:
      - serverless.yml
      - handler.py
```

这个项目结构模板提供了：

1. **完整的项目目录结构**，涵盖前后端、基础设施、文档等所有组件
2. **多种技术栈的代码模板**，支持 FastAPI、Spring Boot、React、Vue 等主流框架
3. **Kubernetes 和 Docker 部署配置**，支持从开发到生产的完整部署流程
4. **灵活的模板配置系统**，可以根据需求组合不同的技术组件
5. **自动化脚本和工具**，简化开发和部署过程

所有模板都使用 Handlebars 语法，支持变量替换和条件渲染，可以根据用户需求动态生成项目代码。