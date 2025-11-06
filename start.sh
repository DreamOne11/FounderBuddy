#!/bin/bash

# Founder Buddy 启动脚本

echo "🚀 Founder Buddy 启动脚本"
echo "=========================="
echo ""

# 检查是否在项目根目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到 .env 文件"
    echo "   请复制 .env.example 为 .env 并配置必要的环境变量"
    echo ""
    read -p "是否现在创建 .env 文件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✅ 已创建 .env 文件，请编辑并添加你的 API Key"
        exit 1
    fi
fi

echo "请选择要启动的服务："
echo "1) 仅启动后端 (端口 8080)"
echo "2) 仅启动前端 (端口 3000)"
echo "3) 同时启动后端和前端（需要两个终端）"
echo ""
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "📦 启动后端服务..."
        echo "后端将在 http://localhost:8080 运行"
        echo "API文档: http://localhost:8080/docs"
        echo ""
        uv run python src/run_service.py
        ;;
    2)
        echo ""
        echo "📦 启动前端服务..."
        echo "前端将在 http://localhost:3000 运行"
        echo ""
        if [ ! -d "frontend/node_modules" ]; then
            echo "⚠️  前端依赖未安装，正在安装..."
            cd frontend && npm install && cd ..
        fi
        cd frontend && npm run dev
        ;;
    3)
        echo ""
        echo "📦 启动后端服务（终端1）..."
        echo "📦 启动前端服务（终端2）..."
        echo ""
        echo "请打开两个终端窗口："
        echo ""
        echo "终端1 - 运行后端:"
        echo "  cd $(pwd)"
        echo "  uv run python src/run_service.py"
        echo ""
        echo "终端2 - 运行前端:"
        echo "  cd $(pwd)/frontend"
        echo "  npm run dev"
        echo ""
        echo "然后访问 http://localhost:3000"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

