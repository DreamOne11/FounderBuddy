# Vercel 环境变量配置指南

## 🚨 问题：部署后出现 500 错误

如果部署后看到 "Sorry, an error occurred while connecting to Founder Buddy"，通常是因为**环境变量未配置**。

## ✅ 解决方案：配置环境变量

### 步骤 1: 进入 Vercel 项目设置

1. 访问 [vercel.com](https://vercel.com)
2. 登录你的账户
3. 找到 `FounderBuddy` 项目
4. 点击项目进入详情页
5. 点击顶部菜单的 **Settings**
6. 在左侧菜单选择 **Environment Variables**

### 步骤 2: 添加必需的环境变量

点击 **Add New** 按钮，添加以下变量：

#### 1. `NEXT_PUBLIC_API_ENV`
- **Value**: `production`
- **Environment**: 选择所有环境（Production, Preview, Development）
- **说明**: 告诉前端使用生产环境配置

#### 2. `VALUE_CANVAS_API_URL_PRODUCTION`
- **Value**: 你的后端 API URL（例如：`https://founder-buddy-production.up.railway.app`）
- **Environment**: 选择所有环境
- **说明**: 后端 API 的完整 URL（**不要**包含尾部斜杠 `/`）

#### 3. `VALUE_CANVAS_API_TOKEN`（可选）
- **Value**: 如果你的后端需要认证 token
- **Environment**: 选择所有环境
- **说明**: 仅在需要 API 认证时配置

### 步骤 3: 重新部署

配置完环境变量后：

1. 回到项目首页
2. 点击最新的部署（Deployment）
3. 点击右上角的 **"..."** 菜单
4. 选择 **Redeploy**
5. 选择 **"Use existing Build Cache"** 或 **"Rebuild"**（建议选择 Rebuild）

或者，你可以：
- Push 一个新的 commit 到 GitHub（Vercel 会自动重新部署）
- 或者等待 Vercel 自动检测到环境变量变化并重新部署

## 🔍 验证配置

部署完成后：

1. 访问你的 Vercel URL
2. 打开浏览器开发者工具（F12）
3. 查看 **Console** 标签，应该没有错误
4. 查看 **Network** 标签，API 请求应该指向正确的后端 URL
5. 尝试发送一条消息测试

## 📋 环境变量检查清单

- [ ] `NEXT_PUBLIC_API_ENV` = `production`
- [ ] `VALUE_CANVAS_API_URL_PRODUCTION` = 你的后端 URL（例如：`https://xxx.railway.app`）
- [ ] 所有变量都设置为所有环境（Production, Preview, Development）
- [ ] 后端 URL **不包含**尾部斜杠 `/`
- [ ] 已重新部署项目

## 🐛 常见问题

### Q: 后端还没部署怎么办？

**A**: 你需要先部署后端（推荐使用 Railway），然后获取后端 URL，再配置到 Vercel。

参考：[后端部署指南](./BACKEND_DEPLOYMENT.md)

### Q: 如何知道后端 URL 是什么？

**A**: 
- 如果使用 Railway：在 Railway 项目页面，点击你的服务，在 **Settings** → **Networking** 可以看到 URL
- 如果使用其他平台：查看平台提供的服务 URL

### Q: 环境变量配置后还是不工作？

**A**: 
1. 确保变量名完全正确（区分大小写）
2. 确保已重新部署
3. 检查 Vercel 部署日志，查看是否有错误信息
4. 确认后端服务正在运行（访问后端 URL 的 `/health` 端点）

### Q: 如何测试后端是否可用？

**A**: 在浏览器访问：
```
https://your-backend-url.com/health
```

应该返回 `{"status":"ok"}` 或类似的成功响应。

## 📞 需要帮助？

如果按照以上步骤操作后仍有问题，请检查：
1. Vercel 部署日志
2. 浏览器控制台错误信息
3. 后端服务日志

