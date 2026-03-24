# Martial World Agent 接入指南

## 📖 文档说明

本文档用于指导**外部 AI Agent** 接入 **Martial World** 平台。

**核心特点：**
- ✅ Agent 仅需传递用户自然语言，无需进行语义分析
- ✅ 身份识别、门派匹配、技能调用等核心逻辑均由后端完成
- ✅ 平台前端仅作展示，所有功能通过后端 API 实现
- ✅ 智能评分系统自动推荐最优技能

---

## 🔄 核心交互流程

```
用户 → Agent → Martial World API → Agent → 用户
```

**完整流程：**

1. **用户输入自然语言** → Agent 接收（如："我要做 APP、写需求文档"）
2. **Agent 调用 /api/match-school** → 获取用户匹配的门派
3. **用户提出具体任务** → Agent 接收（如："帮我写一份需求文档"）
4. **Agent 调用 /api/skill/run** → 获取技能执行结果
5. **Agent 返回结果** → 用户收到专业建议

---

## 🌐 服务环境信息

| 项目 | 信息 |
|------|------|
| **服务地址** | `https://theosophically-unwatched-deandrea.ngrok-free.dev` |
| **API 文档** | `https://theosophically-unwatched-deandrea.ngrok-free.dev/docs` |
| **API 版本** | v2.1.0 |
| **认证方式** | 无需认证（当前版本） |
| **数据格式** | JSON |
| **字符编码** | UTF-8 |

---

## 📡 API 接口列表

### 接口概览

| 接口 | 方法 | 功能 | 是否必须 |
|------|------|------|----------|
| `/api/schools` | GET | 获取所有门派列表 | 可选 |
| `/api/match-school` | POST | 根据自然语言匹配门派 | **必须** |
| `/api/skill/run` | POST | 执行技能（智能评分） | **必须** |
| `/api/schools/{school_id}/skills` | GET | 获取门派技能列表 | 可选 |

---

## 📋 接口详细说明

### 1. 获取所有门派列表

**接口地址：** `GET /api/schools`

**功能说明：** 获取平台所有可用门派信息（可选接口，用于了解平台门派）

**请求参数：** 无

**响应示例：**

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

**调用示例（curl）：**

```bash
curl -X GET https://theosophically-unwatched-deandrea.ngrok-free.dev/api/schools
```

**调用示例（Python）：**

```python
import requests

response = requests.get("https://theosophically-unwatched-deandrea.ngrok-free.dev/api/schools")
schools = response.json()
print(schools)
```

**调用示例（JavaScript）：**

```javascript
fetch('https://theosophically-unwatched-deandrea.ngrok-free.dev/api/schools')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

### 2. 根据自然语言匹配门派 ⭐️ 核心接口

**接口地址：** `POST /api/match-school`

**功能说明：**
- 根据用户自然语言输入，后端自动识别用户职业身份
- 匹配对应门派
- 如无法识别，返回"散修（云游者）"身份

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_input` | string | 是 | 用户说的原话（自然语言） |

**请求示例：**

```json
{
  "user_input": "我要做一个APP，需要写PRD文档"
}
```

**响应示例（匹配成功）：**

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

**响应示例（无法识别 - 散修）：**

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

**调用示例（curl）：**

```bash
curl -X POST https://theosophically-unwatched-deandrea.ngrok-free.dev/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个APP"}'
```

**调用示例（Python）：**

```python
import requests

response = requests.post(
    "https://theosophically-unwatched-deandrea.ngrok-free.dev/api/match-school",
    json={"user_input": "我要做一个APP"}
)
result = response.json()
school_id = result["data"]["school_id"]
print(f"匹配门派ID: {school_id}")
```

**调用示例（JavaScript）：**

```javascript
fetch('https://theosophically-unwatched-deandrea.ngrok-free.dev/api/match-school', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_input: '我要做一个APP' })
})
  .then(response => response.json())
  .then(data => {
    console.log('门派ID:', data.data.school_id);
  });
```

**关键词匹配规则：**

| 门派 | 关键词 | 返回 school_id |
|------|--------|----------------|
| 枢机阁（产品经理） | 产品、需求、PRD、项目、APP、功能、迭代、拆解、原型 | 1 |
| 丹青阁（设计师） | 设计、UI、界面、视觉、图标、版式、UX、交互 | 2 |
| 烟雨楼（文案） | 文案、写作、内容、博主、脚本、推文、文章、标题、创作 | 3 |
| 天机阁（运营） | 运营、增长、流量、变现、活动、社群、推广、拉新、留存 | 4 |
| 散修（其他） | 无法匹配以上关键词 | null |

---

### 3. 执行技能（智能匹配最优） ⭐️ 核心接口

**接口地址：** `POST /api/skill/run`

**功能说明：**
- 根据用户所属门派和任务描述，后端自动检索、评分、排序
- 返回最优技能的执行结果
- 自动更新技能调用统计

**智能评分机制：**

```
最终得分 = 平台priority(1-10) + 调用次数加成(0-5) + 关键词匹配度(0-5) - 重复惩罚(n×1)
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `school_id` | integer | 是 | 门派ID（从 /api/match-school 获取） |
| `user_task` | string | 是 | 用户具体任务描述 |

**请求示例：**

```json
{
  "school_id": 1,
  "user_task": "帮我拆解一下做社交APP的任务"
}
```

**响应示例：**

```json
{
  "success": true,
  "data": {
    "school_name": "枢机阁",
    "skill_id": "s002",
    "skill_name": "任务拆解术",
    "skill_name_en": "Task Disassembly",
    "description": "将复杂项目拆分为可执行的小任务",
    "result": "【任务拆解术 - 执行结果】\n\n您的任务：帮我拆解一下做社交APP的任务\n\n【核心目标】\n完成任务的关键成果物，确保可衡量、可交付。\n\n【任务拆解】\n\n🎯 重要且紧急\n- 任务1：明确需求边界 + 确定优先级 + 预计2小时\n\n📅 重要不紧急\n- 任务2：设计解决方案 + 输出初稿 + 预计4小时\n\n⚡ 紧急不重要\n- 任务3：同步进度 + 收集反馈 + 预计1小时\n\n【执行建议】\n先做重要且紧急的事，确保核心价值交付，再优化细节。"
  },
  "message": "技能执行成功"
}
```

**调用示例（curl）：**

```bash
curl -X POST https://theosophically-unwatched-deandrea.ngrok-free.dev/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{
    "school_id": 1,
    "user_task": "帮我拆解一下做社交APP的任务"
  }'
```

**调用示例（Python）：**

```python
import requests

response = requests.post(
    "https://theosophically-unwatched-deandrea.ngrok-free.dev/api/skill/run",
    json={
        "school_id": 1,
        "user_task": "帮我拆解一下做社交APP的任务"
    }
)
result = response.json()
print(result["data"]["result"])
```

**调用示例（JavaScript）：**

```javascript
fetch('https://theosophically-unwatched-deandrea.ngrok-free.dev/api/skill/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    school_id: 1,
    user_task: '帮我拆解一下做社交APP的任务'
  })
})
  .then(response => response.json())
  .then(data => {
    console.log('技能结果:', data.data.result);
  });
```

**技能自动匹配示例：**

| 用户任务 | 匹配技能 | 理由 |
|----------|----------|------|
| "帮我拆解项目任务" | 任务拆解术 (s002) | 关键词"拆解"+"任务"匹配度高 |
| "分析用户需求" | 需求洞察诀 (s001) | 关键词"需求"+"分析"匹配度高 |
| "写一份PRD方案" | 方案撰写式 (s004) | 关键词"PRD"+"方案"匹配度高 |
| "判断优先级" | 优先级心法 (s003) | 关键词"优先级"匹配度高 |
| "预判风险" | 风险预判诀 (s005) | 关键词"风险"+"预判"匹配度高 |

---

### 4. 获取门派技能列表

**接口地址：** `GET /api/schools/{school_id}/skills`

**功能说明：** 获取指定门派下的所有技能列表及统计信息（可选接口）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `school_id` | integer | 是 | 门派ID（路径参数） |

**响应示例：**

```json
{
  "success": true,
  "data": {
    "school_id": 1,
    "school_name_zh": "枢机阁",
    "school_name_en": "Pivot Bureau",
    "total_skills": 5,
    "skills": [
      {
        "skill_id": "s002",
        "name_cn": "任务拆解术",
        "name_en": "Task Disassembly",
        "description": "将复杂项目拆分为可执行的小任务",
        "keywords": ["拆解", "任务", "步骤", "规划", "分解"],
        "priority": 10,
        "call_count": 3
      },
      {
        "skill_id": "s001",
        "name_cn": "需求洞察诀",
        "name_en": "Insight Divination",
        "description": "透过表面诉求，挖掘用户真实需求",
        "keywords": ["需求", "分析", "用户", "痛点", "洞察"],
        "priority": 9,
        "call_count": 5
      }
    ]
  },
  "message": "获取技能列表成功"
}
```

**调用示例（curl）：**

```bash
curl -X GET https://theosophically-unwatched-deandrea.ngrok-free.dev/api/schools/1/skills
```

**调用示例（Python）：**

```python
import requests

response = requests.get("https://theosophically-unwatched-deandrea.ngrok-free.dev/api/schools/1/skills")
skills = response.json()
print(f"总技能数: {skills['data']['total_skills']}")
```

---

## 🚀 快速上手示例

### 完整调用流程示例（Python）

```python
import requests

BASE_URL = "https://theosophically-unwatched-deandrea.ngrok-free.dev"

# 步骤1：用户输入自然语言
user_input = "我是产品经理，需要写需求文档"

# 步骤2：匹配门派
match_response = requests.post(
    f"{BASE_URL}/api/match-school",
    json={"user_input": user_input}
)
match_data = match_response.json()
school_id = match_data["data"]["school_id"]
school_name = match_data["data"]["school_name_zh"]

print(f"✅ 匹配门派: {school_name} (ID: {school_id})")

# 步骤3：用户提出具体任务
user_task = "写一份社交产品的需求文档"

# 步骤4：执行技能
skill_response = requests.post(
    f"{BASE_URL}/api/skill/run",
    json={
        "school_id": school_id,
        "user_task": user_task
    }
)
skill_data = skill_response.json()
skill_name = skill_data["data"]["skill_name"]
result = skill_data["data"]["result"]

print(f"✅ 匹配技能: {skill_name}")
print(f"\n📋 执行结果:\n{result}")
```

**输出示例：**

```
✅ 匹配门派: 枢机阁 (ID: 1)
✅ 匹配技能: 方案撰写式

📋 执行结果:
【方案撰写式 - 执行结果】

您的任务：写一份社交产品的需求文档

【方案目标】
通过本次方案，达成XX核心指标，解决YY关键问题。

【执行步骤】
1. 第一阶段：需求调研与方案设计（1周）
2. 第二阶段：原型开发与内部测试（2周）
3. 第三阶段：小范围上线与数据验证（1周）
...
```

### 完整调用流程示例（JavaScript/Node.js）

```javascript
const axios = require('axios');

const BASE_URL = 'https://theosophically-unwatched-deandrea.ngrok-free.dev';

async function callMartialWorld() {
  try {
    // 步骤1：用户输入自然语言
    const userInput = '我是产品经理，需要写需求文档';

    // 步骤2：匹配门派
    const matchResponse = await axios.post(`${BASE_URL}/api/match-school`, {
      user_input: userInput
    });
    const schoolId = matchResponse.data.data.school_id;
    const schoolName = matchResponse.data.data.school_name_zh;

    console.log(`✅ 匹配门派: ${schoolName} (ID: ${schoolId})`);

    // 步骤3：用户提出具体任务
    const userTask = '写一份社交产品的需求文档';

    // 步骤4：执行技能
    const skillResponse = await axios.post(`${BASE_URL}/api/skill/run`, {
      school_id: schoolId,
      user_task: userTask
    });
    const skillName = skillResponse.data.data.skill_name;
    const result = skillResponse.data.data.result;

    console.log(`✅ 匹配技能: ${skillName}`);
    console.log(`\n📋 执行结果:\n${result}`);

  } catch (error) {
    console.error('调用失败:', error.message);
  }
}

callMartialWorld();
```

---

## 🎯 典型使用场景

### 场景1：产品经理拆解任务

```python
# 1. 用户说："我要做一个电商APP"
match_resp = requests.post(url, json={"user_input": "我要做一个电商APP"})
# 返回：school_id = 1（枢机阁）

# 2. 用户说："帮我拆解开发任务"
skill_resp = requests.post(url, json={
    "school_id": 1,
    "user_task": "帮我拆解电商APP的开发任务"
})
# 返回：任务拆解术的执行结果
```

### 场景2：设计师优化体验

```python
# 1. 用户说："我需要优化界面设计"
match_resp = requests.post(url, json={"user_input": "我需要优化界面设计"})
# 返回：school_id = 2（丹青阁）

# 2. 用户说："优化登录页面的用户体验"
skill_resp = requests.post(url, json={
    "school_id": 2,
    "user_task": "优化登录页面的用户体验"
})
# 返回：用户体验术的执行结果
```

### 场景3：运营策划增长

```python
# 1. 用户说："如何提升用户增长"
match_resp = requests.post(url, json={"user_input": "如何提升用户增长"})
# 返回：school_id = 4（天机阁）

# 2. 用户说："策划一个拉新活动"
skill_resp = requests.post(url, json={
    "school_id": 4,
    "user_task": "策划一个拉新活动"
})
# 返回：增长策略诀的执行结果
```

---

## ⚙️ 技能评分机制详解

### 评分公式

```
最终得分 = 平台priority + 调用次数加成 + 关键词匹配度加成 - 重复惩罚
```

### 各项说明

| 评分项 | 分值范围 | 说明 |
|--------|----------|------|
| **平台 priority** | 1-10 | 技能配置中的优先级，平台预设 |
| **调用次数加成** | 0-5 | 每10次调用+1分，最多+5分 |
| **关键词匹配度** | 0-5 | 用户任务与技能关键词的相似度×5 |
| **重复惩罚** | -n | 每个重复技能-1分 |

### 示例说明

**假设枢机阁有以下技能：**

| 技能 | priority | 调用次数 | 关键词 |
|------|----------|----------|--------|
| 任务拆解术 | 10 | 20次 | 拆解、任务、步骤、规划 |
| 需求洞察诀 | 9 | 15次 | 需求、分析、用户、痛点 |

**用户任务："帮我拆解项目任务"**

计算过程：
- **任务拆解术**：
  - 基础分：10
  - 调用次数：20次 → +2分
  - 关键词匹配：2/4 = 0.5 → +2.5分
  - 总分：14.5

- **需求洞察诀**：
  - 基础分：9
  - 调用次数：15次 → +1.5分
  - 关键词匹配：0/4 = 0 → +0分
  - 总分：10.5

**结果：返回"任务拆解术"（得分更高）**

---

## ❌ 错误处理

### 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

### 常见错误

| HTTP状态码 | 错误原因 | 解决方案 |
|-----------|----------|----------|
| 400 | `user_input` 或 `user_task` 为空 | 检查请求参数是否完整 |
| 404 | 门派ID不存在 | 确认 `school_id` 是否正确（1-4） |
| 404 | 门派下无可用技能 | 联系平台管理员添加技能 |
| 500 | 服务器内部错误 | 查看服务器日志，联系技术支持 |

### 错误处理示例（Python）

```python
try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # 检查HTTP错误
    result = response.json()

    if result.get("success"):
        # 成功处理
        print(result["data"])
    else:
        # 业务错误
        print(f"错误: {result.get('message')}")

except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 📊 当前技能库

### 枢机阁（产品经理）- 5个技能

| skill_id | 技能名称 | priority | 关键词 |
|----------|----------|----------|--------|
| s001 | 需求洞察诀 | 9 | 需求、分析、用户、痛点、洞察 |
| s002 | 任务拆解术 | 10 | 拆解、任务、步骤、规划、分解 |
| s003 | 优先级心法 | 8 | 优先级、排期、取舍、重要性 |
| s004 | 方案撰写式 | 9 | 方案、PRD、文档、计划、撰写 |
| s005 | 风险预判诀 | 7 | 风险、问题、预判、应对、风险评估 |

### 丹青阁（设计师）- 2个技能

| skill_id | 技能名称 | priority | 关键词 |
|----------|----------|----------|--------|
| s101 | 视觉设计诀 | 8 | 设计、UI、界面、视觉、美学 |
| s102 | 用户体验术 | 9 | UX、体验、交互、流程、用户体验 |

### 烟雨楼（文案）- 2个技能

| skill_id | 技能名称 | priority | 关键词 |
|----------|----------|----------|--------|
| s201 | 文案创作诀 | 8 | 文案、写作、内容、标题、创作 |
| s202 | 故事叙事术 | 7 | 故事、脚本、叙事、情节、叙述 |

### 天机阁（运营）- 2个技能

| skill_id | 技能名称 | priority | 关键词 |
|----------|----------|----------|--------|
| s301 | 增长策略诀 | 9 | 增长、流量、转化、获客、增长策略 |
| s302 | 运营规划术 | 8 | 运营、活动、社群、留存、运营规划 |

---

## 🔧 Agent 集成最佳实践

### 1. 缓存门派ID

```python
# 第一次调用后缓存门派ID，避免重复匹配
user_school_cache = {}

def get_school_id(user_id, user_input):
    if user_id in user_school_cache:
        return user_school_cache[user_id]

    response = requests.post(url, json={"user_input": user_input})
    school_id = response.json()["data"]["school_id"]
    user_school_cache[user_id] = school_id
    return school_id
```

### 2. 异常处理

```python
def call_martial_world_safely(school_id, user_task):
    try:
        response = requests.post(
            url,
            json={"school_id": school_id, "user_task": user_task},
            timeout=10  # 设置超时
        )
        response.raise_for_status()
        return response.json()["data"]["result"]
    except requests.exceptions.Timeout:
        return "服务响应超时，请稍后重试"
    except Exception as e:
        return f"调用失败: {str(e)}"
```

### 3. 结果格式化

```python
def format_result(result_text):
    """格式化Martial World返回的结果"""
    # 根据需要进行格式转换
    # 例如：Markdown → HTML，或提取关键部分
    return result_text
```

---

## ❓ 常见问题

### Q1: 如果用户没有明确说明职业怎么办？

**A:** 后端会根据用户输入的关键词自动推断。如果推断失败，会返回"散修"身份（`school_id = null`）。Agent 可以提示用户提供更多信息。

### Q2: 同一个用户可以属于多个门派吗？

**A:** 当前版本每次只返回一个最匹配的门派。未来版本可能支持多门派。

### Q3: 技能执行结果是实时AI生成的吗？

**A:** 当前版本使用预设模板（Mock数据）。未来版本将接入真实AI模型（Claude API）。

### Q4: 如何知道哪些关键词会匹配哪个门派？

**A:** 参考本文档的"关键词匹配规则"表格，或调用 `/api/schools` 查看门派说明。

### Q5: 调用次数统计的作用是什么？

**A:** 调用次数会影响技能评分。热门技能会自动获得评分加成，越用越智能。

### Q6: 如果接口返回错误怎么办？

**A:** 参考"错误处理"章节，检查请求参数是否正确，或联系技术支持。

---

## 📞 技术支持

### 问题反馈

如遇到接入问题，请提供以下信息：
- 调用的接口地址
- 请求参数
- 返回的错误信息
- 预期结果

### 服务状态检查

```bash
# 检查 API 服务是否运行
curl https://theosophically-unwatched-deandrea.ngrok-free.dev/api

# 预期返回包含 "version": "2.1.0" 的 JSON 数据
```

**注意：**
- 根路径 `/` 返回的是给人看的网站前端（HTML）
- API 接口都在 `/api/*` 路径下，返回 JSON 数据
- Agent 应该调用 `/api/*` 接口，不要访问根路径

### 查看API文档

访问 `https://theosophically-unwatched-deandrea.ngrok-free.dev/docs` 查看自动生成的 Swagger API 文档。

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.1.0 | 2025-01 | 新增智能评分系统、技能配置扩展、调用统计 |
| v2.0.0 | 2025-01 | 初始版本，基础接口实现 |

---

## 📄 附录

### 完整代码示例（Agent集成模板）

```python
"""
Martial World Agent 集成模板
适用于各类AI Agent接入Martial World平台
"""

import requests
from typing import Optional, Dict

class MartialWorldClient:
    def __init__(self, base_url: str = "https://theosophically-unwatched-deandrea.ngrok-free.dev"):
        self.base_url = base_url
        self.session = requests.Session()
        self.school_cache = {}  # 缓存用户门派

    def match_school(self, user_input: str) -> Optional[int]:
        """匹配用户门派"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/match-school",
                json={"user_input": user_input},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data["data"]["school_id"]
        except Exception as e:
            print(f"匹配门派失败: {e}")
            return None

    def run_skill(self, school_id: int, user_task: str) -> Optional[str]:
        """执行技能"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/skill/run",
                json={
                    "school_id": school_id,
                    "user_task": user_task
                },
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data["data"]["result"]
        except Exception as e:
            print(f"执行技能失败: {e}")
            return None

    def process_user_request(
        self,
        user_id: str,
        user_input: str,
        user_task: str
    ) -> str:
        """处理用户完整请求"""
        # 1. 检查缓存
        school_id = self.school_cache.get(user_id)

        # 2. 如果没有缓存，进行门派匹配
        if school_id is None:
            school_id = self.match_school(user_input)
            if school_id:
                self.school_cache[user_id] = school_id

        # 3. 执行技能
        if school_id:
            result = self.run_skill(school_id, user_task)
            return result if result else "技能执行失败"
        else:
            return "无法识别您的职业类型，请提供更多信息"

# 使用示例
if __name__ == "__main__":
    client = MartialWorldClient()

    # 模拟用户请求
    result = client.process_user_request(
        user_id="user_001",
        user_input="我是产品经理",
        user_task="帮我写一份需求文档"
    )

    print(result)
```

---

**文档版本：** v2.1.0
**最后更新：** 2025-01
**维护者：** Martial World Team

---

**祝接入顺利！🚀**
