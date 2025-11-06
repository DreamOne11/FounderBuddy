# Founder Buddy - 快速启动指南

## 📋 项目简介

Founder Buddy 是一个帮助创业者验证和优化创业想法的AI助手。通过结构化的对话，帮助你明确：
- **Mission** - 使命和愿景
- **Idea** - 核心产品想法
- **Team & Traction** - 团队和进展
- **Investment Plan** - 融资计划

## 🚀 快速开始

### 1. 环境配置

#### 后端配置

创建 `.env` 文件（参考 `.env.example`）：

```bash
# 必须：至少配置一个LLM API Key
OPENAI_API_KEY=your-openai-api-key-here

# 可选：服务器配置（默认端口8080）
PORT=8080

# 可选：认证token（如果设置了，前端需要配置）
# AUTH_SECRET=your-secret-token
```

#### 前端配置

前端环境变量文件已创建在 `frontend/.env.local`，默认配置：
- `NEXT_PUBLIC_API_ENV=local` - 使用本地开发环境
- `VALUE_CANVAS_API_URL_LOCAL=http://localhost:8080` - 本地后端地址

### 2. 安装依赖

```bash
# 后端依赖（如果还没安装）
uv sync

# 前端依赖（如果还没安装）
cd frontend
npm install
```

### 3. 运行项目

#### 终端1：启动后端服务

```bash
# 在项目根目录
uv run python src/run_service.py
```

后端将在 `http://localhost:8080` 启动

#### 终端2：启动前端服务

```bash
# 在项目根目录
cd frontend
npm run dev
```

前端将在 `http://localhost:3000` 启动

### 4. 访问应用

打开浏览器访问：`http://localhost:3000`

默认会使用 `founder-buddy` agent，你可以：
- 点击左上角的 Settings 按钮切换agent
- 开始与AI对话，验证你的创业想法

## 🛠️ 开发说明

### 项目结构

```
FounderBuddy/
├── src/
│   └── agents/
│       └── founder_buddy/    # Founder Buddy Agent
│           ├── sections/     # 4个section模板
│           ├── nodes/        # LangGraph节点
│           └── graph/        # Graph构建
├── frontend/                 # Next.js前端应用
└── .env                      # 后端环境变量
```

### 修改Agent

- Agent逻辑：`src/agents/founder_buddy/`
- Section模板：`src/agents/founder_buddy/sections/`
- 前端界面：`frontend/src/components/`

### 调试

- 后端日志：查看运行后端的终端输出
- 前端日志：查看浏览器控制台（F12）
- API调试：检查 `http://localhost:8080/docs` (FastAPI自动文档)

## 📝 常见问题

### 后端启动失败

1. 检查 `.env` 文件是否存在且配置了LLM API Key
2. 确认端口8080没有被占用：`lsof -i :8080`
3. 查看错误日志定位问题

### 前端无法连接后端

1. 确认后端已启动且运行在 `http://localhost:8080`
2. 检查 `frontend/.env.local` 配置是否正确
3. 确认 `NEXT_PUBLIC_API_ENV=local`
4. 重启前端服务：`npm run dev`

### 切换Agent

在Settings面板中可以选择不同的agent：
- `founder-buddy` - Founder Buddy（默认）
- `value-canvas` - Value Canvas
- `mission-pitch` - Mission Pitch
- 等等...

## 🎯 下一步

1. **测试基本流程**：启动项目，尝试与founder-buddy对话
2. **自定义Section**：修改 `src/agents/founder_buddy/sections/` 中的prompt模板
3. **优化UI**：调整 `frontend/src/components/` 中的组件样式
4. **添加功能**：根据需求扩展agent功能

祝你的创业项目顺利！🚀

