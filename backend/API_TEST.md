# Martial World API 测试文档

## 启动服务

```bash
cd backend
python main.py
```

服务将运行在：`http://localhost:8000`

API文档（自动生成）：`http://localhost:8000/docs`

---

## 接口测试示例

### 1. 获取所有门派列表

**接口：** `GET /api/schools`

**功能：** 供外部Agent获取平台有哪些门派

**测试命令：**

```bash
curl -X GET http://localhost:8000/api/schools
```

**返回示例：**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name_zh": "枢机阁",
      "name_en": "Pivot Bureau",
      "description": "产品思维为心法，决策规划为招式。适合产品经理、项目经理、创业者。",
      "role": "product_manager"
    },
    {
      "id": 2,
      "name_zh": "丹青阁",
      "name_en": "Design Temple",
      "description": "以美学为基，以用户体验为本。适合UI/UX设计师、视觉设计师。",
      "role": "designer"
    },
    {
      "id": 3,
      "name_zh": "烟雨楼",
      "name_en": "Rain Pavilion",
      "description": "字句如刀，内容为王。适合文案策划、内容创作者、编剧。",
      "role": "copywriter"
    },
    {
      "id": 4,
      "name_zh": "天机阁",
      "name_en": "Opportunity House",
      "description": "洞察人性，驱动增长。适合运营专家、增长黑客、市场策略。",
      "role": "operator"
    }
  ],
  "message": "获取门派列表成功"
}
```

---

### 2. 根据自然语言匹配门派

**接口：** `POST /api/match-school`

**功能：** 后端自动识别用户身份并匹配门派

**请求参数：**

```json
{
  "user_input": "用户说的任意原话"
}
```

#### 测试案例 1：产品经理

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个APP，需要写PRD文档"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_id": 1,
    "school_name_zh": "枢机阁",
    "school_name_en": "Pivot Bureau",
    "role": "product_manager",
    "reason": "根据您的输入「我要做一个APP，需要写PRD文档」，识别您为产品思维为心法，决策规划为招式。适合产品经理、项目经理、创业者。"
  },
  "message": "匹配成功"
}
```

#### 测试案例 2：设计师

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "帮我设计一个登录界面的UI"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_id": 2,
    "school_name_zh": "丹青阁",
    "school_name_en": "Design Temple",
    "role": "designer",
    "reason": "根据您的输入「帮我设计一个登录界面的UI」，识别您为以美学为基，以用户体验为本。适合UI/UX设计师、视觉设计师。"
  },
  "message": "匹配成功"
}
```

#### 测试案例 3：文案

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我需要写一篇公众号文案"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_id": 3,
    "school_name_zh": "烟雨楼",
    "school_name_en": "Rain Pavilion",
    "role": "copywriter",
    "reason": "根据您的输入「我需要写一篇公众号文案」，识别您为字句如刀，内容为王。适合文案策划、内容创作者、编剧。"
  },
  "message": "匹配成功"
}
```

#### 测试案例 4：运营

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "如何提升产品的用户留存和增长"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_id": 4,
    "school_name_zh": "天机阁",
    "school_name_en": "Opportunity House",
    "role": "operator",
    "reason": "根据您的输入「如何提升产品的用户留存和增长」，识别您为洞察人性，驱动增长。适合运营专家、增长黑客、市场策略。"
  },
  "message": "匹配成功"
}
```

#### 测试案例 5：无法识别（散修）

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "今天天气真好"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_id": null,
    "school_name_zh": "散修（云游者）",
    "school_name_en": "Wanderer",
    "role": "unknown",
    "reason": "暂时无法识别您的职业类型，您可以作为散修自由探索各门派技能。"
  },
  "message": "匹配成功（散修）"
}
```

---

### 3. 根据门派 + 任务执行技能

**接口：** `POST /api/skill/run`

**功能：** 根据用户所属门派和任务，返回技能执行结果

**请求参数：**

```json
{
  "school_id": 1,
  "user_task": "写一份需求文档"
}
```

#### 测试案例 1：枢机阁 - 需求洞察诀

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "用户说想要一个能分析数据的功能"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_name": "枢机阁",
    "skill_id": "s001",
    "skill_name": "需求洞察诀",
    "result": "【需求洞察诀 - 执行结果】\n\n您的任务：用户说想要一个能分析数据的功能\n\n【表面需求】\n用户希望通过本次任务快速达成某个目标。\n\n【底层动机】\n真正的诉求可能是解决效率问题、建立信任或验证假设。\n\n【关键洞察】\n1. 关注用户真实场景，而非表面功能\n2. 优先解决核心痛点，避免功能堆砌\n3. 用最小成本验证核心价值假设\n\n💡 建议：明确核心目标后再拆解执行步骤，避免方向偏差。"
  },
  "message": "技能执行成功"
}
```

#### 测试案例 2：枢机阁 - 任务拆解术

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "帮我拆解一下做小红书竞品分析的步骤"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_name": "枢机阁",
    "skill_id": "s002",
    "skill_name": "任务拆解术",
    "result": "【任务拆解术 - 执行结果】\n\n您的任务：帮我拆解一下做小红书竞品分析的步骤\n\n【核心目标】\n完成任务的关键成果物，确保可衡量、可交付。\n\n【任务拆解】\n\n🎯 重要且紧急\n- 任务1：明确需求边界 + 确定优先级 + 预计2小时\n\n📅 重要不紧急\n- 任务2：设计解决方案 + 输出初稿 + 预计4小时\n\n⚡ 紧急不重要\n- 任务3：同步进度 + 收集反馈 + 预计1小时\n\n【执行建议】\n先做重要且紧急的事，确保核心价值交付，再优化细节。"
  },
  "message": "技能执行成功"
}
```

#### 测试案例 3：丹青阁 - 设计技能

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 2, "user_task": "设计一个深色主题的仪表盘界面"}'
```

**返回：**

```json
{
  "success": true,
  "data": {
    "school_name": "丹青阁",
    "skill_id": "s101",
    "skill_name": "视觉设计诀",
    "result": "【视觉设计诀 - 执行结果】\n\n您的任务：设计一个深色主题的仪表盘界面\n\n[Mock结果] 这是来自 丹青阁 的 视觉设计诀 技能输出。\n\n实际使用时，会根据您的具体任务生成专业的、结构化的分析结果。\n\n💡 提示：本平台现处于演示模式，展示技能调用流程。"
  },
  "message": "技能执行成功"
}
```

#### 测试案例 4：烟雨楼 - 文案技能

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 3, "user_task": "写一个吸引人的产品标题"}'
```

#### 测试案例 5：天机阁 - 运营技能

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 4, "user_task": "策划一个增长活动提升用户留存"}'
```

---

## 使用流程示例

### 完整的Agent调用流程

```bash
# 步骤1：Agent获取所有门派列表
curl -X GET http://localhost:8000/api/schools

# 步骤2：用户说话，Agent调用匹配接口
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个社交APP"}'

# 步骤3：获得门派ID后，用户提出具体任务
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "拆解社交APP的开发任务"}'
```

---

## Python 调用示例

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. 获取门派列表
response = requests.get(f"{BASE_URL}/api/schools")
schools = response.json()
print("门派列表:", schools)

# 2. 匹配门派
match_response = requests.post(
    f"{BASE_URL}/api/match-school",
    json={"user_input": "我要做产品需求分析"}
)
match_data = match_response.json()
print("匹配结果:", match_data)

school_id = match_data["data"]["school_id"]

# 3. 执行技能
if school_id:
    skill_response = requests.post(
        f"{BASE_URL}/api/skill/run",
        json={
            "school_id": school_id,
            "user_task": "分析竞品的核心功能"
        }
    )
    skill_result = skill_response.json()
    print("技能结果:", skill_result["data"]["result"])
```

---

## 关键词匹配规则

后端通过以下关键词自动识别用户身份：

| 门派 | 关键词 |
|------|--------|
| 枢机阁（产品经理） | 产品、需求、PRD、项目、APP、功能、迭代、拆解、原型 |
| 丹青阁（设计师） | 设计、UI、界面、视觉、图标、版式、UX、交互 |
| 烟雨楼（文案） | 文案、写作、内容、博主、脚本、推文、文章、标题、创作 |
| 天机阁（运营） | 运营、增长、流量、变现、活动、社群、推广、拉新、留存 |
| 散修（其他） | 无法匹配以上关键词时自动归类 |

---

## 错误处理

### 1. 空输入

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": ""}'
```

返回：`400 Bad Request` - "user_input 不能为空"

### 2. 门派不存在

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 999, "user_task": "测试"}'
```

返回：`404 Not Found` - "门派 ID 999 不存在"

---

## 注意事项

1. **无需认证**：当前版本无需登录、Token，所有接口公开访问
2. **Mock数据**：所有技能执行结果为Mock数据，展示接口调用流程
3. **CORS已配置**：允许前端跨域访问
4. **自动文档**：访问 `http://localhost:8000/docs` 查看Swagger文档
5. **日志输出**：启动时会显示服务器地址和文档地址

---

## 快速测试脚本

保存以下脚本为 `test_api.sh`：

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "===== 测试 1：获取门派列表 ====="
curl -s -X GET $BASE_URL/api/schools | jq '.'

echo "\n\n===== 测试 2：匹配门派（产品经理） ====="
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做APP"}' | jq '.'

echo "\n\n===== 测试 3：执行技能 ====="
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "拆解项目任务"}' | jq '.'
```

运行：

```bash
chmod +x test_api.sh
./test_api.sh
```
