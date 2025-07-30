# Mission Pitch Agent API 文档

## 概述

Mission Pitch Agent 是一个专业的商业故事创建助手，帮助企业主通过6步框架开发连接起源、使命和愿景的真实故事，可在2分钟内完成演讲。

**Base URL**: `https://chat-agent-y6oijw.fly.dev`

## 目录

- [快速开始](#快速开始)
- [API 端点](#api-端点)
- [请求参数](#请求参数)
- [响应格式](#响应格式)
- [工作流程](#工作流程)
- [代码示例](#代码示例)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

## 快速开始

### 基础调用示例

```bash
curl -X POST "https://chat-agent-y6oijw.fly.dev/mission-pitch-agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to create my Mission Pitch story",
    "model": "gpt-4o-mini",
    "thread_id": "my-session-001",
    "user_id": "user-123"
  }'
```

## API 端点

### 1. 同步调用

**端点**: `POST /mission-pitch-agent/invoke`

获取完整的响应后返回结果，适合需要等待完整回答的场景。

### 2. 流式调用

**端点**: `POST /mission-pitch-agent/stream`

实时流式返回响应，适合需要实时显示生成过程的场景。

### 3. 服务信息

**端点**: `GET /info`

获取服务元数据和所有可用的 agents 信息。

## 请求参数

### 通用参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `message` | string | ✅ | - | 用户输入的消息内容 |
| `model` | string | ❌ | gpt-4o-mini | LLM 模型选择 |
| `thread_id` | string | ❌ | 随机生成 | 会话ID，用于保持对话连续性 |
| `user_id` | string | ❌ | 随机生成 | 用户ID，用于个性化和数据持久化 |
| `agent_config` | object | ❌ | {} | 额外的配置参数 |

### 流式调用专有参数

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `stream_tokens` | boolean | ❌ | true | 是否流式返回 tokens |

### 支持的模型

- `gpt-4o`
- `gpt-4o-mini` (推荐，成本效益高)

## 响应格式

### 同步响应

```json
{
  "type": "ai",
  "content": "Let's discover your hidden theme—the consistent thread that's been running through your life...",
  "tool_calls": [],
  "tool_call_id": null,
  "run_id": "12345-abcde-67890",
  "response_metadata": {
    "token_usage": {
      "completion_tokens": 150,
      "prompt_tokens": 100,
      "total_tokens": 250
    }
  },
  "custom_data": {}
}
```

### 流式响应

Server-Sent Events (SSE) 格式：

```
data: {"type": "token", "content": "Let's"}
data: {"type": "token", "content": " discover"}
data: {"type": "message", "content": {"type": "ai", "content": "Complete message..."}}
data: [DONE]
```

## 工作流程

Mission Pitch Agent 遵循6步框架：

### 第1步：Hidden Theme（隐藏主题）
发现贯穿生活的一致线索

**示例调用**:
```json
{
  "message": "I want to create my Mission Pitch story",
  "thread_id": "session-001",
  "user_id": "user-123"
}
```

**期望响应**: 主题发现练习和句式选择

### 第2步：Personal Origin（个人起源）
早期体现主题的关键时刻

**示例调用**:
```json
{
  "message": "I deeply believe the world needs better connection between technology and human empathy",
  "thread_id": "session-001", 
  "user_id": "user-123"
}
```

**期望响应**: 个人故事开发指导

### 第3步：Business Origin（商业起源）
"这应该成为一门生意"的实现时刻

### 第4步：Mission（使命）
为客户创造的具体转变

### 第5步：3-Year Vision（3年愿景）
值得庆祝的具体商业里程碑

### 第6步：Big Vision（大愿景）
无私的世界变革愿景

### 完成
生成完整的 Mission Pitch 故事和测试指南

## 代码示例

### JavaScript/Node.js

```javascript
class MissionPitchClient {
  constructor(baseUrl = 'https://chat-agent-y6oijw.fly.dev') {
    this.baseUrl = baseUrl;
  }

  async invoke(message, options = {}) {
    const response = await fetch(`${this.baseUrl}/mission-pitch-agent/invoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        model: options.model || 'gpt-4o-mini',
        thread_id: options.threadId,
        user_id: options.userId,
        ...options
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async stream(message, options = {}, onToken, onMessage) {
    const response = await fetch(`${this.baseUrl}/mission-pitch-agent/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        model: options.model || 'gpt-4o-mini',
        thread_id: options.threadId,
        user_id: options.userId,
        stream_tokens: true,
        ...options
      })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') return;

          try {
            const parsed = JSON.parse(data);
            if (parsed.type === 'token' && onToken) {
              onToken(parsed.content);
            } else if (parsed.type === 'message' && onMessage) {
              onMessage(parsed.content);
            }
          } catch (e) {
            // Ignore parsing errors
          }
        }
      }
    }
  }
}

// 使用示例
const client = new MissionPitchClient();

// 同步调用
const response = await client.invoke(
  "I want to develop my Mission Pitch", 
  { threadId: "session-001", userId: "user-123" }
);
console.log(response.content);

// 流式调用
await client.stream(
  "Continue with my story development",
  { threadId: "session-001", userId: "user-123" },
  (token) => process.stdout.write(token),
  (message) => console.log('\nComplete:', message)
);
```

### Python

```python
import requests
import json
from typing import Optional, Dict, Any, Callable

class MissionPitchClient:
    def __init__(self, base_url: str = "https://chat-agent-y6oijw.fly.dev"):
        self.base_url = base_url
    
    def invoke(self, message: str, **options) -> Dict[str, Any]:
        """同步调用 Mission Pitch Agent"""
        payload = {
            "message": message,
            "model": options.get("model", "gpt-4o-mini"),
            "thread_id": options.get("thread_id"),
            "user_id": options.get("user_id"),
            **{k: v for k, v in options.items() if k not in ["model", "thread_id", "user_id"]}
        }
        
        response = requests.post(
            f"{self.base_url}/mission-pitch-agent/invoke",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    def stream(self, message: str, on_token: Optional[Callable] = None, 
               on_message: Optional[Callable] = None, **options):
        """流式调用 Mission Pitch Agent"""
        payload = {
            "message": message,
            "model": options.get("model", "gpt-4o-mini"),
            "thread_id": options.get("thread_id"),
            "user_id": options.get("user_id"),
            "stream_tokens": True,
            **{k: v for k, v in options.items() if k not in ["model", "thread_id", "user_id"]}
        }
        
        response = requests.post(
            f"{self.base_url}/mission-pitch-agent/stream",
            json=payload,
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    
                    try:
                        parsed = json.loads(data)
                        if parsed.get('type') == 'token' and on_token:
                            on_token(parsed.get('content', ''))
                        elif parsed.get('type') == 'message' and on_message:
                            on_message(parsed.get('content', {}))
                    except json.JSONDecodeError:
                        continue

# 使用示例
client = MissionPitchClient()

# 同步调用
response = client.invoke(
    "I want to create my Mission Pitch story",
    thread_id="session-001",
    user_id="user-123"
)
print(response['content'])

# 流式调用
client.stream(
    "Continue with my story development",
    on_token=lambda token: print(token, end=''),
    on_message=lambda msg: print(f"\n\nComplete: {msg}"),
    thread_id="session-001",
    user_id="user-123"
)
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type MissionPitchClient struct {
    BaseURL string
}

type InvokeRequest struct {
    Message    string `json:"message"`
    Model      string `json:"model,omitempty"`
    ThreadID   string `json:"thread_id,omitempty"`
    UserID     string `json:"user_id,omitempty"`
}

type InvokeResponse struct {
    Type       string      `json:"type"`
    Content    string      `json:"content"`
    RunID      string      `json:"run_id"`
    ToolCalls  []any       `json:"tool_calls"`
    CustomData interface{} `json:"custom_data"`
}

func NewMissionPitchClient(baseURL string) *MissionPitchClient {
    if baseURL == "" {
        baseURL = "https://chat-agent-y6oijw.fly.dev"
    }
    return &MissionPitchClient{BaseURL: baseURL}
}

func (c *MissionPitchClient) Invoke(req InvokeRequest) (*InvokeResponse, error) {
    if req.Model == "" {
        req.Model = "gpt-4o-mini"
    }

    jsonData, err := json.Marshal(req)
    if err != nil {
        return nil, err
    }

    resp, err := http.Post(
        c.BaseURL+"/mission-pitch-agent/invoke",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var result InvokeResponse
    err = json.Unmarshal(body, &result)
    return &result, err
}

// 使用示例
func main() {
    client := NewMissionPitchClient("")
    
    response, err := client.Invoke(InvokeRequest{
        Message:  "I want to develop my Mission Pitch story",
        ThreadID: "session-001",
        UserID:   "user-123",
    })
    
    if err != nil {
        panic(err)
    }
    
    fmt.Println(response.Content)
}
```

## 错误处理

### 常见错误码

| 状态码 | 错误类型 | 描述 | 解决方案 |
|--------|----------|------|----------|
| 400 | Bad Request | 请求参数错误 | 检查请求参数格式 |
| 401 | Unauthorized | 认证失败 | 检查 AUTH_SECRET (如果启用) |
| 422 | Validation Error | 参数验证失败 | 确认参数类型和必需字段 |
| 500 | Internal Server Error | 服务器内部错误 | 重试请求，联系支持 |
| 503 | Service Unavailable | 服务不可用 | 等待后重试 |

### 错误响应格式

```json
{
  "detail": "Error message description",
  "status_code": 400,
  "error_type": "validation_error"
}
```

### 重试策略

```python
import time
import random

def call_with_retry(func, max_retries=3, base_delay=1):
    """指数退避重试策略"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s...")
            time.sleep(delay)
```

## 最佳实践

### 1. 会话管理

```python
import uuid

class MissionPitchSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.thread_id = str(uuid.uuid4())
        self.client = MissionPitchClient()
        self.step = 1
    
    def send_message(self, message: str):
        return self.client.invoke(
            message,
            thread_id=self.thread_id,
            user_id=self.user_id
        )
```

### 2. 进度跟踪

Mission Pitch Agent 会自动跟踪用户进度，但建议在客户端也维护状态：

```python
MISSION_PITCH_STEPS = [
    "hidden_theme",
    "personal_origin", 
    "business_origin",
    "mission",
    "three_year_vision",
    "big_vision",
    "complete"
]

def track_progress(response_content: str) -> str:
    """从响应中推断当前步骤"""
    if "hidden theme" in response_content.lower():
        return "hidden_theme"
    elif "personal origin" in response_content.lower():
        return "personal_origin"
    # ... 其他步骤检测逻辑
    return "unknown"
```

### 3. 数据持久化

虽然 Agent 会自动保存进度，建议客户端也保存关键对话：

```python
import json
from datetime import datetime

def save_conversation(thread_id: str, message: str, response: dict):
    """保存对话到本地存储"""
    conversation_log = {
        "timestamp": datetime.now().isoformat(),
        "thread_id": thread_id,
        "user_message": message,
        "agent_response": response
    }
    
    with open(f"conversations/{thread_id}.jsonl", "a") as f:
        f.write(json.dumps(conversation_log) + "\n")
```

### 4. 内容安全

Agent 内置 LlamaGuard 安全检查，但建议客户端也进行预检：

```python
def is_safe_content(message: str) -> bool:
    """基础内容安全检查"""
    inappropriate_keywords = [
        # 添加不当内容关键词
    ]
    
    return not any(keyword in message.lower() for keyword in inappropriate_keywords)
```

### 5. 性能优化

- **使用适当的模型**: `gpt-4o-mini` 通常足够且更经济
- **合理的超时设置**: 推荐 60-120 秒
- **流式调用**: 长对话使用流式接口提升用户体验
- **连接池**: 高频调用时使用连接池

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

## 支持和反馈

如果你在使用过程中遇到问题：

1. **检查服务状态**: `GET /info` 端点
2. **查看错误日志**: 保存请求和响应用于调试
3. **测试网络连接**: 确保能正常访问 API 端点
4. **验证参数格式**: 使用提供的示例作为参考

## 更新日志

### v1.0.0 (2025-07-24)
- ✅ 初始版本发布
- ✅ 完整的6步 Mission Pitch 工作流程
- ✅ 品牌原型识别系统
- ✅ 抗阻模式处理
- ✅ 会话持久化和状态管理
- ✅ 支持同步和流式调用

---

**© 2025 Mission Pitch Agent API Documentation`**