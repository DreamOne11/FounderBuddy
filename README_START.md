# Founder Buddy - 快速启动指南

## ✅ 环境配置已完成

### 后端配置
- ✅ `.env` 文件已存在（包含你的API Key）
- ✅ 后端默认端口：`8080`

### 前端配置  
- ✅ `frontend/.env.local` 已创建
- ✅ 前端默认端口：`3000`
- ✅ API地址：`http://localhost:8080`

## 🚀 启动项目

### 方式1：使用启动脚本（推荐）

```bash
./start.sh
```

然后选择要启动的服务（1=后端，2=前端，3=查看说明）

### 方式2：手动启动

#### 终端1：启动后端
```bash
uv run python src/run_service.py
```

后端将在 `http://localhost:8080` 启动

#### 终端2：启动前端
```bash
cd frontend
npm run dev
```

前端将在 `http://localhost:3000` 启动

## 🌐 访问应用

1. 打开浏览器访问：**http://localhost:3000**
2. 默认使用 `founder-buddy` agent
3. 点击左上角 **Settings** 按钮可以切换agent

## 📝 验证步骤

### 1. 检查后端是否运行
```bash
curl http://localhost:8080/health
```
应该返回：`{"status":"ok"}`

### 2. 检查API文档
访问：http://localhost:8080/docs

### 3. 检查前端连接
- 打开浏览器开发者工具（F12）
- 查看Console标签，应该没有连接错误
- 尝试发送一条消息测试

## 🐛 常见问题排查

### 后端启动失败
```bash
# 检查端口是否被占用
lsof -i :8080

# 检查.env文件
cat .env | grep OPENAI_API_KEY
```

### 前端无法连接后端
1. 确认后端已启动：`curl http://localhost:8080/health`
2. 检查 `frontend/.env.local` 中的 `NEXT_PUBLIC_API_ENV=local`
3. 重启前端：`cd frontend && npm run dev`

### 端口冲突
如果8080或3000端口被占用：
- 修改后端端口：在 `.env` 中设置 `PORT=8081`
- 修改前端端口：运行 `cd frontend && PORT=3001 npm run dev`
- 别忘了更新 `frontend/.env.local` 中的API URL

## 📚 下一步

1. **测试基本功能**：启动项目，尝试与founder-buddy对话
2. **查看API文档**：访问 http://localhost:8080/docs
3. **自定义配置**：根据需要修改section prompts和数据模型
4. **添加功能**：扩展agent功能或改进UI

## 💡 提示

- 后端日志会在运行后端的终端显示
- 前端日志在浏览器控制台（F12）
- API调试可以在 http://localhost:8080/docs 进行
- 修改代码后，后端需要重启，前端会自动热重载

祝使用愉快！🎉

