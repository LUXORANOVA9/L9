# LUXOR AI CUA - 备份恢复与模型集成指南
## Backup Restoration & Model Integration Guide

### 📦 备份文件分析 / Backup Files Analysis

基于您提供的备份文件列表，我们需要恢复以下组件：

```
E:\luxor9\backup_20250722_003534\
├── luxor9_ollama_models.tar.gz          # Ollama AI模型备份
├── anaconda_ollama_models.tar.gz        # Anaconda环境中的Ollama模型
├── containers.tar.gz                    # Docker容器备份
├── images.tar.gz                        # Docker镜像备份
└── luxor9_luxor9_ollama_models.tar.gz   # 重复的Ollama模型备份
```

### 🔄 恢复策略 / Restoration Strategy

#### 1. 创建模型存储目录结构

```bash
# 在项目根目录下创建AI模型存储结构
mkdir -p ai-models/{ollama,huggingface,custom}
mkdir -p ai-models/ollama/{chinese-models,code-models,embeddings}
mkdir -p docker-backup/{containers,images}
mkdir -p environments/{anaconda,python}
```

#### 2. 模型恢复优先级

**高优先级 (立即恢复)**:
- `luxor9_ollama_models.tar.gz` - 核心Ollama模型
- `images.tar.gz` - Docker镜像 (包含预配置的AI服务)

**中优先级 (按需恢复)**:
- `anaconda_ollama_models.tar.gz` - Anaconda环境模型
- `containers.tar.gz` - Docker容器状态

**低优先级 (验证后恢复)**:
- `luxor9_luxor9_ollama_models.tar.gz` - 可能是重复备份

### 🚀 自动化恢复脚本

```bash
#!/bin/bash
# restore-ai-models.sh - LUXOR AI CUA 模型恢复脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# 配置变量
BACKUP_DIR="E:/luxor9/backup_20250722_003534"
PROJECT_ROOT="E:/Project_Luxor9"
MODELS_DIR="$PROJECT_ROOT/ai-models"
DOCKER_BACKUP_DIR="$PROJECT_ROOT/docker-backup"

# 检查备份文件是否存在
check_backup_files() {
    info "检查备份文件..."
    
    local backup_files=(
        "luxor9_ollama_models.tar.gz"
        "anaconda_ollama_models.tar.gz"
        "containers.tar.gz"
        "images.tar.gz"
        "luxor9_luxor9_ollama_models.tar.gz"
    )
    
    for file in "${backup_files[@]}"; do
        if [ -f "$BACKUP_DIR/$file" ]; then
            success "找到备份文件: $file"
        else
            warn "备份文件不存在: $file"
        fi
    done
}

# 创建目录结构
create_directories() {
    info "创建目录结构..."
    
    mkdir -p "$MODELS_DIR"/{ollama,huggingface,custom}
    mkdir -p "$MODELS_DIR"/ollama/{chinese-models,code-models,embeddings}
    mkdir -p "$DOCKER_BACKUP_DIR"/{containers,images}
    mkdir -p "$PROJECT_ROOT"/environments/{anaconda,python}
    
    success "目录结构创建完成"
}

# 恢复Ollama模型
restore_ollama_models() {
    info "恢复Ollama模型..."
    
    if [ -f "$BACKUP_DIR/luxor9_ollama_models.tar.gz" ]; then
        info "解压主要Ollama模型备份..."
        tar -xzf "$BACKUP_DIR/luxor9_ollama_models.tar.gz" -C "$MODELS_DIR/ollama/"
        success "Ollama模型恢复完成"
        
        # 列出恢复的模型
        info "已恢复的模型列表:"
        find "$MODELS_DIR/ollama/" -name "*.bin" -o -name "*.gguf" -o -name "*.safetensors" | head -10
    else
        warn "Ollama模型备份文件不存在"
    fi
}

# 恢复Docker镜像
restore_docker_images() {
    info "恢复Docker镜像..."
    
    if [ -f "$BACKUP_DIR/images.tar.gz" ]; then
        info "解压Docker镜像备份..."
        tar -xzf "$BACKUP_DIR/images.tar.gz" -C "$DOCKER_BACKUP_DIR/images/"
        
        # 加载Docker镜像 (如果Docker正在运行)
        if command -v docker &> /dev/null && docker info &> /dev/null; then
            info "加载Docker镜像到本地Docker daemon..."
            find "$DOCKER_BACKUP_DIR/images/" -name "*.tar" -exec docker load -i {} \;
            success "Docker镜像加载完成"
        else
            warn "Docker未运行，镜像文件已解压到 $DOCKER_BACKUP_DIR/images/"
        fi
    else
        warn "Docker镜像备份文件不存在"
    fi
}

# 恢复Anaconda环境
restore_anaconda_models() {
    info "恢复Anaconda环境模型..."
    
    if [ -f "$BACKUP_DIR/anaconda_ollama_models.tar.gz" ]; then
        info "解压Anaconda Ollama模型..."
        tar -xzf "$BACKUP_DIR/anaconda_ollama_models.tar.gz" -C "$PROJECT_ROOT/environments/anaconda/"
        success "Anaconda模型恢复完成"
    else
        warn "Anaconda模型备份文件不存在"
    fi
}

# 恢复Docker容器
restore_docker_containers() {
    info "恢复Docker容器配置..."
    
    if [ -f "$BACKUP_DIR/containers.tar.gz" ]; then
        info "解压Docker容器备份..."
        tar -xzf "$BACKUP_DIR/containers.tar.gz" -C "$DOCKER_BACKUP_DIR/containers/"
        success "Docker容器配置恢复完成"
        
        info "容器配置文件位于: $DOCKER_BACKUP_DIR/containers/"
        info "可以使用这些配置重新创建容器"
    else
        warn "Docker容器备份文件不存在"
    fi
}

# 验证模型完整性
verify_models() {
    info "验证恢复的模型..."
    
    local model_count=0
    local total_size=0
    
    if [ -d "$MODELS_DIR/ollama" ]; then
        model_count=$(find "$MODELS_DIR/ollama" -type f \( -name "*.bin" -o -name "*.gguf" -o -name "*.safetensors" \) | wc -l)
        total_size=$(du -sh "$MODELS_DIR/ollama" | cut -f1)
        
        success "发现 $model_count 个模型文件"
        success "总大小: $total_size"
    fi
    
    # 检查是否有中文模型
    if find "$MODELS_DIR" -name "*chatglm*" -o -name "*baichuan*" -o -name "*qwen*" | grep -q .; then
        success "检测到中文语言模型"
    else
        warn "未检测到中文语言模型，可能需要额外下载"
    fi
}

# 生成模型配置文件
generate_model_config() {
    info "生成模型配置文件..."
    
    cat > "$MODELS_DIR/model-config.yml" << EOF
# LUXOR AI CUA 模型配置
models:
  chinese_nlp:
    # 中文自然语言处理模型
    chatglm3:
      path: "./ollama/chinese-models/chatglm3-6b"
      type: "conversational"
      language: "zh-CN"
    
    qwen:
      path: "./ollama/chinese-models/qwen-14b"
      type: "conversational" 
      language: "zh-CN"
      
    baichuan2:
      path: "./ollama/chinese-models/baichuan2-13b"
      type: "conversational"
      language: "zh-CN"
  
  code_generation:
    # 代码生成模型
    codellama:
      path: "./ollama/code-models/codellama-7b"
      type: "code"
      languages: ["python", "javascript", "java", "go"]
    
    starcoder:
      path: "./ollama/code-models/starcoder-15b"
      type: "code"
      languages: ["python", "javascript", "typescript", "java"]
  
  embeddings:
    # 向量嵌入模型
    bge_large:
      path: "./ollama/embeddings/bge-large-zh"
      type: "embedding"
      language: "zh-CN"
      dimensions: 1024

# Ollama服务配置
ollama:
  host: "localhost"
  port: 11434
  models_path: "./ollama"
  
# Docker配置
docker:
  images_path: "../docker-backup/images"
  containers_path: "../docker-backup/containers"
EOF

    success "模型配置文件已生成: $MODELS_DIR/model-config.yml"
}

# 更新项目配置
update_project_config() {
    info "更新项目配置文件..."
    
    # 更新 .env 文件以包含模型路径
    if [ -f "$PROJECT_ROOT/.env" ]; then
        # 添加或更新模型相关配置
        cat >> "$PROJECT_ROOT/.env" << EOF

# AI模型配置 (从备份恢复)
MODELS_BASE_PATH=$MODELS_DIR
OLLAMA_MODELS_PATH=$MODELS_DIR/ollama
CHINESE_MODEL_PATH=$MODELS_DIR/ollama/chinese-models/chatglm3-6b
CODE_MODEL_PATH=$MODELS_DIR/ollama/code-models/codellama-7b
EMBEDDING_MODEL_PATH=$MODELS_DIR/ollama/embeddings/bge-large-zh

# Ollama服务配置
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_KEEP_ALIVE=24h

# 模型配置文件
MODEL_CONFIG_PATH=$MODELS_DIR/model-config.yml
EOF
        success "环境配置已更新"
    fi
}

# 创建模型管理脚本
create_model_manager() {
    info "创建模型管理脚本..."
    
    cat > "$PROJECT_ROOT/scripts/manage-models.sh" << 'EOF'
#!/bin/bash
# LUXOR AI CUA 模型管理脚本

MODELS_DIR="./ai-models"
OLLAMA_HOST="localhost:11434"

list_models() {
    echo "=== 已安装的模型 ==="
    if command -v ollama &> /dev/null; then
        ollama list
    else
        echo "Ollama未安装或未运行"
        echo "本地模型文件:"
        find "$MODELS_DIR" -name "*.gguf" -o -name "*.bin" -o -name "*.safetensors" | head -10
    fi
}

start_ollama() {
    echo "=== 启动Ollama服务 ==="
    if command -v ollama &> /dev/null; then
        ollama serve &
        echo "Ollama服务已在后台启动"
    else
        echo "Ollama未安装，请先安装Ollama"
    fi
}

load_model() {
    local model_name=$1
    if [ -z "$model_name" ]; then
        echo "使用方法: $0 load <model_name>"
        return 1
    fi
    
    echo "=== 加载模型: $model_name ==="
    ollama pull "$model_name"
}

test_model() {
    local model_name=${1:-"chatglm3"}
    echo "=== 测试模型: $model_name ==="
    echo "你好，我是LUXOR AI助手" | ollama run "$model_name"
}

case "$1" in
    "list"|"ls")
        list_models
        ;;
    "start")
        start_ollama
        ;;
    "load")
        load_model "$2"
        ;;
    "test")
        test_model "$2"
        ;;
    *)
        echo "LUXOR AI CUA 模型管理器"
        echo "使用方法: $0 {list|start|load|test} [参数]"
        echo ""
        echo "命令:"
        echo "  list          列出所有模型"
        echo "  start         启动Ollama服务"
        echo "  load <name>   加载指定模型"
        echo "  test [name]   测试模型功能"
        ;;
esac
EOF

    chmod +x "$PROJECT_ROOT/scripts/manage-models.sh"
    success "模型管理脚本已创建"
}

# 主函数
main() {
    echo "🤖 LUXOR AI CUA - 模型恢复助手"
    echo "================================"
    
    check_backup_files
    create_directories
    restore_ollama_models
    restore_docker_images
    restore_anaconda_models
    restore_docker_containers
    verify_models
    generate_model_config
    update_project_config
    create_model_manager
    
    echo ""
    success "🎉 模型恢复完成!"
    echo ""
    info "下一步操作:"
    echo "1. 验证模型: ./scripts/manage-models.sh list"
    echo "2. 启动Ollama: ./scripts/manage-models.sh start"
    echo "3. 测试模型: ./scripts/manage-models.sh test"
    echo "4. 运行LUXOR AI: ./quick-start.sh"
}

# 执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### 🔧 Docker集成策略

#### 1. 恢复的镜像集成到项目

```yaml
# docker-compose.ai-models.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ai-models/ollama:/root/.ollama
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_KEEP_ALIVE=24h
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  model-manager:
    build:
      context: ./backend
      dockerfile: Dockerfile.model-manager
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - MODELS_CONFIG_PATH=/app/ai-models/model-config.yml
    volumes:
      - ./ai-models:/app/ai-models
    ports:
      - "8001:8001"

volumes:
  ollama_data:
```

#### 2. 模型服务API

```python
# backend/services/model_service.py
import ollama
import yaml
from pathlib import Path
from typing import List, Dict, Optional

class ModelService:
    """LUXOR AI CUA 模型服务"""
    
    def __init__(self, config_path: str = "./ai-models/model-config.yml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.ollama_client = ollama.Client(
            host=self.config.get('ollama', {}).get('host', 'localhost:11434')
        )
    
    def _load_config(self) -> Dict:
        """加载模型配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def list_available_models(self) -> List[Dict]:
        """列出可用的模型"""
        try:
            models = self.ollama_client.list()
            return models.get('models', [])
        except Exception as e:
            print(f"获取模型列表失败: {e}")
            return []
    
    def get_chinese_model(self) -> Optional[str]:
        """获取最佳中文模型"""
        chinese_models = self.config.get('models', {}).get('chinese_nlp', {})
        
        # 按优先级检查模型是否可用
        priority_models = ['chatglm3', 'qwen', 'baichuan2']
        
        for model_key in priority_models:
            if model_key in chinese_models:
                model_path = chinese_models[model_key]['path']
                if self._is_model_available(model_key):
                    return model_key
        
        return None
    
    def get_code_model(self) -> Optional[str]:
        """获取最佳代码生成模型"""
        code_models = self.config.get('models', {}).get('code_generation', {})
        
        priority_models = ['codellama', 'starcoder']
        
        for model_key in priority_models:
            if model_key in code_models:
                if self._is_model_available(model_key):
                    return model_key
        
        return None
    
    def _is_model_available(self, model_name: str) -> bool:
        """检查模型是否可用"""
        try:
            models = self.list_available_models()
            return any(model['name'].startswith(model_name) for model in models)
        except:
            return False
    
    async def generate_text(self, prompt: str, model: str = None) -> str:
        """生成文本"""
        if not model:
            model = self.get_chinese_model()
        
        if not model:
            raise ValueError("没有可用的模型")
        
        try:
            response = self.ollama_client.generate(
                model=model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 2048
                }
            )
            return response.get('response', '')
        except Exception as e:
            raise Exception(f"文本生成失败: {e}")
    
    async def generate_code(self, description: str, language: str = 'python') -> str:
        """生成代码"""
        model = self.get_code_model()
        if not model:
            raise ValueError("没有可用的代码生成模型")
        
        prompt = f"""
请根据以下描述生成{language}代码:
{description}

要求:
1. 代码结构清晰
2. 包含必要的注释
3. 遵循最佳实践
4. 包含错误处理

代码:
```{language}
"""
        
        return await self.generate_text(prompt, model)
```

### 📱 使用说明

#### 1. 立即执行恢复

```bash
# 1. 保存恢复脚本
chmod +x restore-ai-models.sh

# 2. 执行恢复
./restore-ai-models.sh

# 3. 验证恢复结果
ls -la ai-models/ollama/
```

#### 2. 集成到现有项目

```bash
# 1. 更新项目配置
source .env

# 2. 启动AI模型服务
docker-compose -f docker-compose.yml -f docker-compose.ai-models.yml up -d

# 3. 测试模型功能
./scripts/manage-models.sh test
```

### 🎯 集成优势

1. **完整的AI能力**: 恢复所有备份的模型，提供完整的AI功能
2. **中文优化**: 专门针对中文场景优化的模型配置
3. **代码生成**: 支持多种编程语言的代码生成
4. **本地部署**: 所有模型本地运行，保证数据安全
5. **容器化管理**: 通过Docker统一管理所有AI服务

这个恢复方案将您的备份模型完美集成到LUXOR AI CUA项目中，让系统具备真正的AI代码生成和中文理解能力！