#!/bin/bash
# restore-ai-models.sh - LUXOR AI CUA 模型恢复脚本

set -e

# 配置变量
BACKUP_DIR="E:/luxor9/backup_20250722_003534"
PROJECT_ROOT="E:/Project_Luxor9"
MODELS_DIR="$PROJECT_ROOT/ai-models"

echo "🤖 LUXOR AI CUA - 模型恢复助手"
echo "================================"

# 创建目录结构
echo "📁 创建目录结构..."
mkdir -p "$MODELS_DIR"/{ollama,docker-backup}
mkdir -p "$PROJECT_ROOT"/scripts

# 恢复Ollama模型
echo "📦 恢复Ollama模型..."
if [ -f "$BACKUP_DIR/luxor9_ollama_models.tar.gz" ]; then
    cd "$MODELS_DIR/ollama/"
    tar -xzf "$BACKUP_DIR/luxor9_ollama_models.tar.gz"
    echo "✅ Ollama模型恢复完成"
    
    # 统计模型数量
    model_count=$(find . -name "*.gguf" -o -name "*.bin" -o -name "*.safetensors" 2>/dev/null | wc -l)
    echo "📊 发现 $model_count 个模型文件"
else
    echo "⚠️ Ollama模型备份文件不存在"
fi

# 恢复Docker镜像
echo "🐳 恢复Docker镜像..."
if [ -f "$BACKUP_DIR/images.tar.gz" ]; then
    cd "$MODELS_DIR/docker-backup/"
    tar -xzf "$BACKUP_DIR/images.tar.gz"
    echo "✅ Docker镜像备份已解压"
else
    echo "⚠️ Docker镜像备份文件不存在"
fi

# 生成模型配置
echo "⚙️ 生成配置文件..."
cat > "$MODELS_DIR/model-config.yml" << EOF
# LUXOR AI CUA 模型配置
models:
  chinese_nlp:
    chatglm3:
      path: "./ollama/chatglm3-6b"
      type: "conversational"
      language: "zh-CN"
    qwen:
      path: "./ollama/qwen-14b"
      type: "conversational"
      language: "zh-CN"
  
  code_generation:
    codellama:
      path: "./ollama/codellama-7b"
      type: "code"
      languages: ["python", "javascript", "java"]

ollama:
  host: "localhost"
  port: 11434
  models_path: "./ollama"
EOF

# 更新环境配置
echo "📝 更新项目配置..."
cat >> "$PROJECT_ROOT/.env" << EOF

# AI模型配置 (恢复于 $(date))
OLLAMA_MODELS_PATH=$MODELS_DIR/ollama
MODEL_CONFIG_PATH=$MODELS_DIR/model-config.yml
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
EOF

# 创建模型管理脚本
echo "🛠️ 创建管理脚本..."
cat > "$PROJECT_ROOT/scripts/manage-models.sh" << 'EOF'
#!/bin/bash
MODELS_DIR="./ai-models/ollama"

case "$1" in
    "list")
        echo "=== 本地模型文件 ==="
        find "$MODELS_DIR" -name "*.gguf" -o -name "*.bin" 2>/dev/null | head -10
        ;;
    "start")
        echo "=== 启动Ollama服务 ==="
        if command -v ollama &> /dev/null; then
            export OLLAMA_MODELS="$(pwd)/$MODELS_DIR"
            ollama serve &
            echo "Ollama服务已启动"
        else
            echo "请先安装Ollama: curl -fsSL https://ollama.com/install.sh | sh"
        fi
        ;;
    "test")
        echo "=== 测试模型 ==="
        model=${2:-"chatglm3"}
        echo "你好，介绍一下LUXOR AI项目" | ollama run "$model"
        ;;
    *)
        echo "用法: $0 {list|start|test}"
        ;;
esac
EOF

chmod +x "$PROJECT_ROOT/scripts/manage-models.sh"

echo ""
echo "🎉 模型恢复完成!"
echo ""
echo "📋 下一步操作:"
echo "1. 查看模型: ./scripts/manage-models.sh list"
echo "2. 启动服务: ./scripts/manage-models.sh start"  
echo "3. 测试模型: ./scripts/manage-models.sh test"
echo ""
echo "📖 详细说明请查看: BACKUP_RESTORATION_GUIDE.md"