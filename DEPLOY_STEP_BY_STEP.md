# 🚀 Founder Buddy - 完整部署指南（方案二：分离部署）

## 📋 部署概览

- ✅ **前端** → Vercel（Next.js）
- ✅ **后端** → Railway（FastAPI）

预计总时间：**15分钟**

---

## 第一步：部署后端到 Railway（5分钟）

### 1.1 访问 Railway

1. 打开 https://railway.app
2. 点击 **"Login"**，使用 **GitHub** 账户登录

### 1.2 创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 授权 Railway 访问你的 GitHub（如果还没授权）
4. 搜索并选择仓库：`Victoria824/FounderBuddy`
5. 点击 **"Deploy Now"**

### 1.3 配置环境变量

1. 等待项目创建完成（约30秒）
2. 点击项目进入详情页
3. 点击 **"Variables"** 标签
4. 点击 **"New Variable"**，添加：

   ```
   Name: OPENAI_API_KEY
   Value: sk-your-actual-openai-api-key
   ```

   ⚠️ **重要**：将 `sk-your-actual-openai-api-key` 替换为你的真实 OpenAI API Key

5. 点击 **"Add"**

### 1.4 配置启动命令（如果需要）

1. 点击 **"Settings"** 标签
2. 在 **"Start Command"** 中设置：
   ```
   uv run python src/run_service.py
   ```
   （Railway 通常会自动检测，但可以手动设置）

### 1.5 获取后端 URL

1. 等待部署完成（约2-3分钟）
2. 点击 **"Settings"** 标签
3. 在 **"Domains"** 部分，点击 **"Generate Domain"**
4. 复制生成的 URL，例如：`https://founder-buddy-production.up.railway.app`
5. **保存这个 URL**，下一步会用到

### 1.6 验证后端部署

1. 在浏览器中访问：`https://your-railway-url/health`
2. 应该看到：`{"status": "ok"}`
3. 如果看到这个响应，说明后端部署成功 ✅

---

## 第二步：部署前端到 Vercel（5分钟）

### 2.1 访问 Vercel

1. 打开 https://vercel.com
2. 点击 **"Sign Up"** 或 **"Login"**，使用 **GitHub** 账户登录

### 2.2 导入项目

1. 点击 **"Add New..."** → **"Project"**
2. 在 **"Import Git Repository"** 中搜索：`Victoria824/FounderBuddy`
3. 如果没看到，点击 **"Adjust GitHub App Permissions"** 授权
4. 找到仓库后，点击 **"Import"**

### 2.3 配置项目设置

Vercel 会自动检测到 Next.js 项目，确认以下设置：

- **Framework Preset**: `Next.js` ✅
- **Root Directory**: `frontend` ✅（重要！）
- **Build Command**: `npm run build` ✅（自动检测）
- **Output Directory**: `.next` ✅（自动检测）
- **Install Command**: `npm install` ✅（自动检测）

### 2.4 配置环境变量

在 **"Environment Variables"** 部分，点击 **"Add"** 添加以下变量：

#### 变量 1：
```
Name: NEXT_PUBLIC_API_ENV
Value: production
```

#### 变量 2：
```
Name: VALUE_CANVAS_API_URL_PRODUCTION
Value: https://your-railway-url-from-step-1
```

⚠️ **重要**：将 `https://your-railway-url-from-step-1` 替换为第一步获得的 Railway URL

**注意**：
- 不要有尾部斜杠 `/`
- 确保是 `https://` 开头
- 例如：`https://founder-buddy-production.up.railway.app`

### 2.5 部署

1. 确认所有设置正确
2. 点击 **"Deploy"** 按钮
3. 等待部署完成（约2-3分钟）
4. 部署完成后，Vercel 会显示一个 URL，例如：`https://founder-buddy.vercel.app`

---

## 第三步：验证部署（2分钟）

### 3.1 测试前端

1. 访问 Vercel 提供的 URL
2. 应该能看到 Founder Buddy 界面

### 3.2 测试聊天功能

1. 在聊天框中输入：`hi`
2. 点击发送
3. 应该能收到 AI 回复

### 3.3 检查网络请求

1. 打开浏览器开发者工具（F12）
2. 切换到 **"Network"** 标签
3. 发送一条消息
4. 查看请求，确认：
   - API 请求指向正确的 Railway URL
   - 请求成功（状态码 200）
   - 能收到 streaming 响应

---

## ✅ 部署完成检查清单

### 后端（Railway）
- [ ] 项目已创建并部署
- [ ] `OPENAI_API_KEY` 环境变量已设置
- [ ] `/health` 端点返回 `{"status": "ok"}`
- [ ] 已生成并复制了 Railway URL

### 前端（Vercel）
- [ ] 项目已导入并部署
- [ ] Root Directory 设置为 `frontend`
- [ ] `NEXT_PUBLIC_API_ENV=production` 已设置
- [ ] `VALUE_CANVAS_API_URL_PRODUCTION` 已设置为 Railway URL
- [ ] 前端可以正常访问
- [ ] 聊天功能正常工作

---

## 🐛 常见问题排查

### 问题 1: 前端显示 "Failed to fetch agents"

**可能原因**：
- 后端 URL 配置错误
- 后端服务未运行
- CORS 问题

**解决步骤**：
1. 检查 Vercel 环境变量中的 `VALUE_CANVAS_API_URL_PRODUCTION`
2. 访问 `https://your-railway-url/health` 确认后端运行
3. 检查浏览器控制台的错误信息

### 问题 2: Railway 部署失败

**可能原因**：
- 缺少依赖
- Python 版本不兼容
- 环境变量未设置

**解决步骤**：
1. 查看 Railway 的部署日志
2. 确认 `OPENAI_API_KEY` 已设置
3. 检查 `pyproject.toml` 中的 Python 版本要求

### 问题 3: Vercel 构建失败

**可能原因**：
- Node.js 版本问题
- 依赖安装失败
- Root Directory 设置错误

**解决步骤**：
1. 确认 Root Directory 是 `frontend`
2. 查看 Vercel 构建日志
3. 尝试在本地运行 `cd frontend && npm install && npm run build` 测试

### 问题 4: CORS 错误

**可能原因**：后端未允许前端域名

**解决步骤**：
1. 检查 `src/service/service.py` 中的 CORS 配置
2. 确保允许 `*.vercel.app` 域名
3. 如果需要，添加你的 Vercel 域名到 CORS 允许列表

---

## 🔄 后续更新

### 更新代码

1. **更新后端**：
   - 在本地修改代码
   - Push 到 GitHub
   - Railway 会自动重新部署

2. **更新前端**：
   - 在本地修改代码
   - Push 到 GitHub
   - Vercel 会自动重新部署

### 查看日志

- **Railway**: 项目页面 → "Deployments" → 点击部署 → "View Logs"
- **Vercel**: 项目页面 → "Deployments" → 点击部署 → "Build Logs" 或 "Function Logs"

---

## 📚 相关文档

- [Railway 文档](https://docs.railway.app)
- [Vercel 文档](https://vercel.com/docs)
- [后端部署详细指南](./BACKEND_DEPLOYMENT.md)
- [Vercel 部署详细指南](./VERCEL_DEPLOYMENT.md)

---

## 🎉 完成！

部署完成后，你的 Founder Buddy 应用就可以在线上使用了！

**前端 URL**: `https://your-vercel-url.vercel.app`
**后端 URL**: `https://your-railway-url.up.railway.app`

有任何问题，查看上面的常见问题部分或检查部署日志。

