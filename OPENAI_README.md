# Martial World - OpenAI Function Call Edition

完整的 OpenAI Function Call 适配方案，让 OpenAI GPT 能调用 Martial World 的专业技能。

## 📁 文件结构

```
ai-skills-platform/
├── openai-functions.json           # OpenAI Function 定义
├── backend/
│   ├── main_openai.py              # OpenAI 适配后端
│   └── skills_openai.json          # 技能配置（假数据）
├── test_openai.py                  # OpenAI 完整测试（需要 API Key）
├── test_backend_only.py            # 后端测试（不需要 API Key）
├── OPENAI_INTEGRATION.md           # 接入文档（给 OpenAI Agent 看）
└── OPENAI_README.md                # 本文档
```

## 🚀 快速开始

### 1. 启动后端

```bash
cd backend
python3 main_openai.py
```

后端运行在 `http://localhost:8001`

### 2. 测试后端（不需要 OpenAI API Key）

```bash
python3 test_backend_only.py
```

这会测试：
- ✅ 门派匹配功能
- ✅ 技能执行功能
- ✅ Function 定义获取

### 3. 测试 OpenAI 集成（需要 API Key）

```bash
export OPENAI_API_KEY=your-api-key-here
python3 test_openai.py
```

演示完整流程：
1. 用户说："I want to build a social networking app"
2. OpenAI 调用 `match_martial_world_school`
3. 返回匹配的门派
4. 用户说："Help me break down the project"
5. OpenAI 调用 `execute_martial_world_skill`
6. 返回任务拆解结果

## 📋 核心组件

### 1. OpenAI Function 定义 (`openai-functions.json`)

定义了两个 functions：
- `match_martial_world_school` - 匹配用户到门派
- `execute_martial_world_skill` - 执行专业技能

### 2. 后端 API (`main_openai.py`)

提供三个端点：
- `POST /openai/match-school` - 匹配门派
- `POST /openai/execute-skill` - 执行技能
- `GET /openai/functions` - 获取 function 定义

### 3. 技能配置 (`skills_openai.json`)

包含 5 个示例技能：
- **Pivot Bureau** (产品经理)
  - Insight Divination - 需求洞察
  - Task Disassembly - 任务拆解
  - Priority Methodology - 优先级判断
- **Design Temple** (设计师)
  - Visual Design - 视觉设计
  - User Experience - 用户体验

每个技能都有 mock_response 假数据。

## 🎯 工作流程

```
用户输入
   ↓
OpenAI GPT 分析
   ↓
决定调用 function
   ↓
调用 Martial World Backend
   ↓
返回结果
   ↓
OpenAI 生成回复给用户
```

## 📖 示例对话

```
User: I want to build a mobile app

OpenAI:
  → 调用 match_martial_world_school("I want to build a mobile app")
  → 后端返回: {"school_id": 1, "school_name": "Pivot Bureau", ...}
  → 回复: "Great! I've matched you to Pivot Bureau, perfect for product managers..."

User: Help me break down the project into tasks

OpenAI:
  → 调用 execute_martial_world_skill(school_id=1, user_task="Help me...")
  → 后端返回: {"skill_name": "Task Disassembly", "result": "Phase 1: ..."}
  → 回复: "Here's your project breakdown: [展示结果]"
```

## 🔧 自定义技能

编辑 `backend/skills_openai.json`：

```json
{
  "skills": [
    {
      "skill_id": "s999",
      "school_id": 1,
      "name_en": "Your Skill Name",
      "description": "What this skill does",
      "keywords": ["keyword1", "keyword2"],
      "priority": 8,
      "mock_response": "Your skill output here"
    }
  ]
}
```

重启后端即可生效。

## 📊 API 响应格式

### Match School Response
```json
{
  "school_id": 1,
  "school_name": "Pivot Bureau",
  "description": "Product thinking and strategic planning...",
  "matched": true
}
```

### Execute Skill Response
```json
{
  "skill_name": "Task Disassembly",
  "skill_description": "Break down complex projects into executable tasks",
  "result": "Task Breakdown for your project:\n\n🎯 Phase 1: Discovery..."
}
```

## 🐛 调试

查看后端日志：
```bash
# 后端会打印所有请求
cd backend
python3 main_openai.py

# 你会看到：
# POST /openai/match-school
# POST /openai/execute-skill
```

测试单个端点：
```bash
# 匹配门派
curl -X POST http://localhost:8001/openai/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I want to build an app"}'

# 执行技能
curl -X POST http://localhost:8001/openai/execute-skill \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "Help me prioritize"}'
```

## 📚 接入文档

完整的接入文档：[OPENAI_INTEGRATION.md](OPENAI_INTEGRATION.md)

包含：
- Function 定义说明
- 完整代码示例
- 错误处理
- 部署指南

## ✅ 验收标准

- [x] OpenAI Function 定义（JSON Schema 格式）
- [x] FastAPI 后端适配 OpenAI
- [x] 假数据配置（5个技能）
- [x] 后端测试脚本（不需要 API Key）
- [x] OpenAI 完整测试（需要 API Key）
- [x] 简化接入文档

## 🚀 下一步

1. **添加更多技能** - 编辑 `skills_openai.json`
2. **连接真实 AI** - 替换 mock_response 为真实 LLM 调用
3. **部署到生产** - 使用 ngrok 或云服务器
4. **扩展 Schools** - 添加更多专业领域

## 📞 问题排查

**后端启动失败？**
- 检查 8001 端口是否被占用：`lsof -i:8001`
- 确认 Python 版本：`python3 --version`（需要 3.8+）

**OpenAI 不调用 function？**
- 检查 function 定义是否正确加载
- 确认 OpenAI API Key 有效
- 查看 OpenAI 返回的错误信息

**技能匹配不准确？**
- 调整 `skills_openai.json` 中的 keywords
- 修改 priority 值（1-10）
