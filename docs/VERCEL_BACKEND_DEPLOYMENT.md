# Vercel 部署 Python 后端指南

## ⚠️ 重要限制

Vercel 可以部署 Python 后端，但有以下限制：

### 1. **执行时间限制**
- **免费版**: 10秒超时
- **Pro版**: 60秒超时
- **Enterprise**: 300秒超时

**问题**：你的后端有 streaming endpoints，可能需要长时间运行，可能超过免费版的10秒限制。

### 2. **无状态要求**
- Serverless Functions 应该是无状态的
- 你的后端使用了数据库连接和内存存储，可能需要调整

### 3. **冷启动**
- 每次请求可能需要冷启动（加载依赖）
- Python 依赖较多，冷启动可能较慢

## ✅ 解决方案

### 方案 1：使用 Vercel Serverless Functions（适合简单API）

创建 `api/index.py` 文件：

```python
from fastapi import FastAPI
from mangum import Mangum

from service.service import app

# 使用 Mangum 将 FastAPI 转换为 AWS Lambda handler
handler = Mangum(app)
```

**需要的文件结构**：
```
api/
  index.py  # Vercel会自动识别
requirements.txt  # Python依赖
vercel.json  # 配置
```

### 方案 2：分离前后端（推荐）

**前端** → Vercel（Next.js）
**后端** → Railway/Render（FastAPI）

**优点**：
- ✅ 无时间限制
- ✅ 支持长时间streaming
- ✅ 更好的性能
- ✅ 独立扩展

## 🚀 如果坚持使用 Vercel 部署后端

### 步骤 1：创建 API 目录结构

```
api/
  index.py
requirements.txt
vercel.json
```

### 步骤 2：安装依赖

```bash
pip install mangum
```

### 步骤 3：创建 `api/index.py`

```python
from mangum import Mangum
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from service.service import app

handler = Mangum(app, lifespan="off")  # 关闭lifespan事件
```

### 步骤 4：更新 `vercel.json`

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHONPATH": "src"
  }
}
```

### 步骤 5：创建 `requirements.txt`

```txt
fastapi
mangum
# ... 其他依赖
```

## ⚠️ 潜在问题

1. **Streaming超时**：如果streaming响应超过10秒（免费版），会失败
2. **数据库连接**：每次请求可能需要重新连接
3. **内存限制**：免费版512MB内存
4. **冷启动延迟**：首次请求可能很慢

## 💡 推荐方案

**最佳实践**：
- ✅ **前端** → Vercel（完美支持Next.js）
- ✅ **后端** → Railway/Render（更适合长时间运行的API）

这样你可以：
- 充分利用Vercel的前端优势
- 避免Vercel的后端限制
- 获得更好的性能和可靠性

## 🔄 如果一定要用Vercel

我可以帮你：
1. 创建Vercel serverless function结构
2. 调整代码以适应Vercel限制
3. 处理streaming超时问题

但建议还是使用Railway/Render部署后端，这样更稳定可靠。

你想选择哪个方案？

