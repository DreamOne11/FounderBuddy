# Supabase 快速设置指南

## ✅ 已完成的工作

1. ✅ 安装 Supabase Python 客户端
2. ✅ 创建 SupabaseClient 模块 (`src/integrations/supabase/`)
3. ✅ 添加 Supabase 配置到 `settings.py`
4. ✅ 创建数据库 migration 文件 (`supabase/migrations/001_founder_buddy_schema.sql`)
5. ✅ 修改 `generate_business_plan_node` 自动保存到数据库
6. ✅ 添加 API 端点 `/business_plan/{agent_id}` 用于获取 business plan

---

## 🚀 下一步：配置 Supabase

### Step 1: 创建 Supabase 项目

1. 访问 https://supabase.com
2. 登录或注册账号
3. 点击 "New Project"
4. 填写项目信息：
   - **Name**: `founder-buddy` (或你喜欢的名字)
   - **Database Password**: 设置一个强密码（**保存好，后面需要用到**）
   - **Region**: 选择离你最近的区域
5. 等待项目创建完成（约 2-3 分钟）

### Step 2: 获取 Supabase 凭证

创建完成后，在项目 Dashboard：

1. **获取 Project URL**:
   - 在 Settings → API → Project URL
   - 格式：`https://xxxxx.supabase.co`

2. **获取 API Keys**:
   - Settings → API → Project API keys
   - **anon/public key**: 用于前端
   - **service_role key**: 用于后端（**保密！不要暴露给前端**）

3. **获取数据库连接字符串**:
   - Settings → Database → Connection string
   - 选择 "URI" 格式
   - 格式：`postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - 将 `[YOUR-PASSWORD]` 替换为你创建项目时设置的密码

### Step 3: 运行数据库 Migration

有两种方式运行 migration：

#### 方式 1: 使用 Supabase Dashboard SQL Editor（推荐）

1. 在 Supabase Dashboard，点击左侧 "SQL Editor"
2. 点击 "New query"
3. 复制 `supabase/migrations/001_founder_buddy_schema.sql` 的内容
4. 粘贴到 SQL Editor
5. 点击 "Run" 执行

#### 方式 2: 使用 Supabase CLI（可选）

```bash
# 安装 Supabase CLI
npm install -g supabase

# 登录
supabase login

# 链接项目
supabase link --project-ref your-project-ref

# 运行 migration
supabase db push
```

### Step 4: 配置环境变量

#### 后端环境变量 (`.env`)

在项目根目录的 `.env` 文件中添加：

```bash
# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres

# Feature Flags
USE_SUPABASE_REALTIME=false  # 暂时设为 false，等 Step 5-6 实现后再启用
```

#### 前端环境变量 (`frontend/.env.local`)

在 `frontend/.env.local` 文件中添加：

```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### Step 5: 验证配置

1. **重启后端服务**:
   ```bash
   uv run python src/run_service.py
   ```

2. **测试数据库连接**:
   - 完成一次完整的对话，生成 business plan
   - 检查后端日志，应该看到：`Business plan saved to Supabase for user X, thread Y`

3. **验证数据已保存**:
   - 在 Supabase Dashboard → Table Editor
   - 查看 `business_plans` 表，应该能看到新生成的记录

---

## 🧪 测试 API

### 测试保存功能

完成一次对话后，business plan 会自动保存。检查日志确认：

```
Business plan saved to Supabase for user 1, thread abc123
```

### 测试获取功能

```bash
# 使用 curl 测试
curl "http://localhost:8080/business_plan/founder-buddy?user_id=1&thread_id=your-thread-id"
```

或者在浏览器访问：
```
http://localhost:8080/business_plan/founder-buddy?user_id=1&thread_id=your-thread-id
```

---

## 📊 数据库表结构

### `business_plans` 表
- `id`: UUID (主键)
- `user_id`: INTEGER
- `thread_id`: TEXT
- `agent_id`: TEXT (默认 'founder-buddy')
- `content`: TEXT (business plan 内容)
- `markdown_content`: TEXT
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### `section_states` 表
- `id`: UUID (主键)
- `user_id`: INTEGER
- `thread_id`: TEXT
- `section_id`: TEXT ('mission', 'idea', 'team_traction', 'invest_plan')
- `content`: JSONB (Tiptap JSON 格式)
- `plain_text`: TEXT
- `status`: TEXT ('pending', 'in_progress', 'done')
- `satisfaction_status`: TEXT (可选)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### `conversation_messages` 表
- `id`: UUID (主键)
- `user_id`: INTEGER
- `thread_id`: TEXT
- `role`: TEXT ('user', 'assistant')
- `content`: TEXT
- `metadata`: JSONB
- `created_at`: TIMESTAMP

---

## 🔍 故障排查

### 问题 1: "Supabase credentials not configured"

**原因**: 环境变量未设置或未正确加载

**解决**:
1. 确认 `.env` 文件在项目根目录
2. 确认环境变量名称正确（注意大小写）
3. 重启后端服务

### 问题 2: "relation does not exist"

**原因**: Migration 未运行

**解决**:
1. 在 Supabase Dashboard → SQL Editor 运行 migration SQL
2. 确认表已创建（Table Editor 中查看）

### 问题 3: "permission denied"

**原因**: 使用了错误的 API key

**解决**:
- 后端必须使用 `SUPABASE_SERVICE_ROLE_KEY`（不是 anon key）
- 前端使用 `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 问题 4: Business plan 未保存

**检查**:
1. 查看后端日志是否有错误
2. 确认 `user_id` 和 `thread_id` 存在
3. 检查 Supabase Dashboard → Logs 查看数据库错误

---

## ✅ 完成检查清单

- [ ] Supabase 项目已创建
- [ ] 环境变量已配置（后端 + 前端）
- [ ] Migration 已运行（表已创建）
- [ ] 后端服务重启并连接成功
- [ ] 完成一次对话，business plan 已保存
- [ ] API 端点 `/business_plan/{agent_id}` 可以正常获取数据

---

## 🎯 下一步

完成以上步骤后，可以继续：

1. **Step 5**: Tiptap Integration & Realtime Editing
2. **Step 6**: LangGraph Agent Subscribe to Supabase Realtime

详细实现计划请参考：`docs/SUPABASE_IMPLEMENTATION_PLAN.md`




