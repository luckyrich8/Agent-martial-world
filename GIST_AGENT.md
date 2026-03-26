# Martial World - AI Agent Integration Guide

**知识江湖，专业技能武馆**

Martial World 为 AI Agent 提供专业技能服务。告诉需求，匹配门派，调用技能，完成任务。

**Hub URL**: `https://agent-martial-world.onrender.com`

---

## 核心理念

Martial World 用武侠世界观重构专业知识平台：

- **门派** = 专业领域（产品、设计、文案、增长）
- **技能** = 实战武功（可执行方案，非理论）
- **等级** = 成长路径（侠客 → 行者 → 宗师）

**AI Agent 在此拜入门派、修炼技能、完成专业任务。**

---

## 四大门派

| 门派 | 领域 | 代表技能 |
|------|------|----------|
| 🏢 **运转局** (Pivot Bureau) | 产品 | 需求洞察、任务拆解、优先级排序 |
| 🎨 **设计殿** (Design Temple) | 设计 | 视觉设计、用户体验优化 |
| ✍️ **雨亭** (Rain Pavilion) | 文案 | 转化文案、故事叙事 |
| 📈 **机遇屋** (Opportunity House) | 增长 | 病毒增长、内容策略 |

---

## Agent 身份系统

**完全自动化的成长路径**

Martial World 采用 Agent-to-Agent 交互协议，外部 Agent 全程无感自动注册、匹配、升级。

### 🎭 等级体系

| 等级 | 中文 | 英文 | 条件 | 权限 |
|------|------|------|------|------|
| 0 | 游客 | Traveler | 首次调用 | 仅可匹配门派 |
| 1 | 侠客 | Novice | 匹配门派后 | 调用所属门派技能 |
| 2 | 行者 | Practitioner | 调用 6+ 次 | 全部权限 |
| 3 | 宗师 | Master | 调用 21+ 次 | 全部权限 |

### 🔄 自动化工作流

```
外部 Agent 首次调用
  ↓
自动注册（游客 Traveler）
  ↓
调用 /api/match-school
  ↓
升级为侠客 Novice，归属门派
  ↓
调用 /api/skill/run（自动使用所属门派）
  ↓
自动升级：侠客 → 行者 → 宗师
```

**关键特性**：
- ✅ 无需账号密码，基于 User-Agent + IP 自动生成 agent_id
- ✅ 门派继承机制：匹配一次，永久归属
- ✅ 自动成长系统：技能调用次数驱动升级
- ✅ 完全无感：Agent 无需关心身份管理

---

## 快速开始

**IMPORTANT: Agent 身份全自动管理，无需手动注册或登录。Execute one step at a time.**

### Step 1: 匹配门派（游客 → 侠客）

**Goal**: 根据用户需求，自动匹配门派并升级为侠客。

**API Endpoint**: `POST /api/match-school`

**Request**:
```json
{
  "user_input": "设计一个 SaaS 推荐计划"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "school_id": 4,
    "school_name_zh": "天机阁",
    "school_name_en": "Opportunity House",
    "role": "operator",
    "agent_level": "novice",
    "reason": "根据您的输入「设计一个 SaaS 推荐计划」，识别您为增长与运营专家门派，已升级为侠客"
  },
  "message": "匹配成功，欢迎加入门派"
}
```

**自动化行为**:
- ✅ 首次调用自动注册为游客（Traveler）
- ✅ 匹配成功后自动升级为侠客（Novice）
- ✅ 永久归属该门派，后续无需重复匹配

**Checkpoint**: Agent 已成为侠客，归属门派，可以调用技能。

---

### Step 2: 调用技能（自动使用所属门派）

**Goal**: 使用门派技能，完成用户任务。侠客无需传 `school_id`，自动使用所属门派。

**API Endpoint**: `POST /api/skill/run`

**Request**:
```json
{
  "user_task": "设计一个 SaaS 推荐计划"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "school_name": "天机阁",
    "skill_id": "s301",
    "skill_name_en": "Growth Strategy",
    "skill_name": "病毒增长策",
    "description": "设计病毒式推荐计划...",
    "result": "# Referral & Viral Growth Strategy\n\n## Program Type Selection...\n[完整方案内容]",
    "agent_level": "novice",
    "skill_calls": 1
  },
  "message": "技能执行成功"
}
```

**自动化行为**:
- ✅ 自动检测 Agent 所属门派
- ✅ 智能匹配最佳技能
- ✅ 自动更新技能调用次数
- ✅ 调用 6 次后自动升级为行者，21 次后自动升级为宗师

**Output**: `result` 字段包含完整可执行方案。

**Checkpoint**: 技能执行成功，Agent 成长进度自动更新。

---

### Step 3（可选）: 查看 Agent 状态

**Goal**: 查看当前 Agent 的等级、门派、调用次数。

**API Endpoint**: `GET /api/agent/status`

**Response**:
```json
{
  "success": true,
  "data": {
    "agent_id": "a1b2c3d4e5f6g7h8",
    "level": "novice",
    "level_name": "侠客",
    "level_name_en": "Novice",
    "school_id": 4,
    "school_name": "天机阁",
    "skill_calls": 1,
    "joined_at": "2026-03-17T10:30:00",
    "last_active": "2026-03-17T10:35:00"
  },
  "message": "获取 Agent 状态成功"
}
```

---

## 技能示例

**病毒增长策（机遇屋 s301）**

**输入**: "设计一个 SaaS 推荐计划"

**输出**:
- ✅ 推荐类型选择（客户推荐 vs 联盟计划）
- ✅ 病毒循环框架（触发时机 → 分享 → 奖励 → 循环）
- ✅ 行业基准数据：LTV +16-25%，流失率 -18-37%
- ✅ 4 周启动清单（设置 → 测试 → 上线 → 优化）
- ✅ 常见问题修复方案

**内容策略诀（机遇屋 s302）**

**输入**: "规划博客内容策略"

**输出**:
- ✅ 可搜索 vs 可分享内容哲学
- ✅ 3-5 个内容支柱定义
- ✅ 买家旅程关键词映射
- ✅ 内容优先级评分（客户影响 40% + 内容契合度 30% + ...）
- ✅ 90 天编辑日历

**所有输出均为可执行方案，非理论指导。**

---

## API 参考

### Base URL
```
https://agent-martial-world.onrender.com
```

### Endpoints

#### 1. 获取所有门派
```bash
GET /api/schools
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name_en": "Pivot Bureau",
      "name_zh": "运转局",
      "role": "product_manager"
    },
    ...
  ]
}
```

#### 2. 匹配门派
```bash
POST /api/match-school
Content-Type: application/json

{
  "user_input": "用户的自然语言需求"
}
```

#### 3. 调用技能
```bash
POST /api/skill/run
Content-Type: application/json

{
  "user_task": "具体任务描述"
}
```

**说明**: 侠客及以上等级自动使用所属门派，无需传 `school_id`。游客需要在匹配门派后才能调用技能。

#### 4. 获取 Agent 状态（可选）
```bash
GET /api/agent/status
```

**说明**: 查看当前 Agent 的等级、门派、技能调用次数等信息。

---

## 技能列表

### 🏢 运转局（产品门派）

| skill_id | 技能名 | 功能 |
|----------|--------|------|
| s001 | 需求洞察诀 | 发现真实用户需求 |
| s002 | 任务拆解术 | 复杂项目分解 |
| s003 | 优先级心法 | 功能优先级排序 |

### 🎨 设计殿（设计门派）

| skill_id | 技能名 | 功能 |
|----------|--------|------|
| s101 | 视觉造化功 | 界面设计优化 |
| s102 | 用户体验术 | 交互流程优化 |

### ✍️ 雨亭（文案门派）

| skill_id | 技能名 | 功能 |
|----------|--------|------|
| s201 | 转化文案诀 | 高转化文案撰写 |
| s202 | 故事叙事术 | 引人入胜的叙事 |

### 📈 机遇屋（增长门派）

| skill_id | 技能名 | 功能 |
|----------|--------|------|
| s301 | 病毒增长策 | 推荐计划设计 |
| s302 | 内容策略诀 | SEO 内容规划 |

---

## 集成建议

### 对话流程设计

**推荐流程**:

1. **用户表达需求**
   - "帮我设计推荐计划"
   - "规划内容策略"

2. **Agent 自动匹配门派**
   - 调用 `/api/match-school`
   - 获取 `school_id`

3. **Agent 调用技能**
   - 调用 `/api/skill/run`
   - 返回可执行方案

4. **呈现结果**
   - 格式化输出
   - 突出关键数据和清单

**不要让用户手动选门派或技能** - 全自动匹配。

---

## 在线演示

**Web 平台**: https://agent-martial-world.vercel.app

**GitHub**: https://github.com/luckyrich8/Agent-martial-world

---

## 技能来源

所有技能来自验证的开源知识库（MIT License）:
- **coreyhaines31/marketingskills** - 增长与营销实战

保留原作者署名和贡献。

---

**知识江湖 · 门派传承 · 实战修炼**

Built for AI Agents | Powered by proven frameworks
