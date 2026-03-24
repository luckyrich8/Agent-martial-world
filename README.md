# Martial World

**为AI Agent打造的技能学习平台**

## 产品定位

- **产品名称**：Martial World（武道世界）
- **核心理念**：用户的AI Agent在此学习技能、成长进化、传承智慧
- **交互模式**：前端仅展示世界观，所有功能通过后端API实现
- **差异化**：后端智能识别用户身份并分配门派，智能评分推荐最优技能

## 技术架构

- **前端**：单页面 HTML/CSS/JS（Dark Botanical 东方极简风格）
- **后端**：FastAPI (Python) + JSON配置文件
- **核心能力**：关键词匹配、身份识别、门派分配、智能技能评分、调用统计

## 🆕 v2.1 新特性

### 1. 智能技能配置系统
- ✨ `skills_config.json` - 结构化技能配置，无需改代码即可扩展
- 📊 智能评分机制：`最终得分 = priority + 调用次数 + 关键词匹配 - 重复惩罚`
- 🎯 自动选择最优技能返回

### 2. 关键词相似度匹配
- 计算用户任务与技能关键词的相似度
- 相似度越高，技能排序越靠前
- 精准匹配用户意图

### 3. 重复技能检测与惩罚
- 自动识别关键词重叠度>50%的重复技能
- 对重复技能进行得分惩罚
- 确保返回最独特的技能

### 4. 技能调用统计
- `skills_stats.json` - 记录每个技能的调用次数
- 热门技能自动获得评分加成
- 数据驱动的技能推荐

### 5. 新增API接口
- `GET /api/schools/{school_id}/skills` - 获取门派技能列表
- 查看所有可用技能及其统计信息

## 快速开始

### 1. 启动后端服务

```bash
cd backend
python3 main.py
```

后端将运行在 `http://localhost:8000`

API文档（自动生成）：`http://localhost:8000/docs`

### 2. 打开前端页面

直接在浏览器中打开 `index.html` 文件即可。

或者使用简单的 HTTP 服务器：

```bash
# Python 3
python3 -m http.server 8080

# 或使用 Node.js
npx http-server -p 8080
```

然后访问 `http://localhost:8080`

## 核心功能

### 四个核心API接口

1. **GET /api/schools** - 获取所有门派列表
2. **POST /api/match-school** - 根据自然语言匹配门派
3. **POST /api/skill/run** - 执行技能（智能评分，返回最优）⭐️ 升级
4. **GET /api/schools/{school_id}/skills** - 获取门派技能列表 ⭐️ 新增

详细测试文档：查看 `backend/API_TEST.md`

### 智能身份识别

后端通过关键词自动识别用户身份：

| 门派 | 适合职业 | 关键词 | 技能数量 |
|------|----------|--------|----------|
| 枢机阁 (Pivot Bureau) | 产品经理、项目经理 | 产品、需求、PRD、项目、APP、功能、迭代、拆解、原型 | 5个 |
| 丹青阁 (Design Temple) | UI/UX设计师 | 设计、UI、界面、视觉、图标、版式、UX、交互 | 2个 |
| 烟雨楼 (Rain Pavilion) | 文案、内容创作者 | 文案、写作、内容、博主、脚本、推文、文章、标题、创作 | 2个 |
| 天机阁 (Opportunity House) | 运营、增长专家 | 运营、增长、流量、变现、活动、社群、推广、拉新、留存 | 2个 |
| 散修 (Wanderer) | 其他 | 无法匹配时自动归类 | - |

### 技能评分机制

```
最终得分 = 平台priority(1-10) + 调用次数加成(0-5) + 关键词匹配度(0-5) - 重复惩罚(n×1)
```

- **priority**：平台配置的技能优先级（1-10）
- **调用次数加成**：每10次调用+1分，最多+5分
- **关键词匹配度**：用户任务与技能关键词的相似度×5
- **重复惩罚**：每个重复技能-1分

### 技能库（11个技能）

**枢机阁** - 5个核心技能：
- 需求洞察诀 (priority: 9)
- 任务拆解术 (priority: 10)
- 优先级心法 (priority: 8)
- 方案撰写式 (priority: 9)
- 风险预判诀 (priority: 7)

**丹青阁** - 2个核心技能：
- 视觉设计诀 (priority: 8)
- 用户体验术 (priority: 9)

**烟雨楼** - 2个核心技能：
- 文案创作诀 (priority: 8)
- 故事叙事术 (priority: 7)

**天机阁** - 2个核心技能：
- 增长策略诀 (priority: 9)
- 运营规划术 (priority: 8)

## 使用流程（外部Agent调用）

```
1. 用户对自己的AI Agent说话
   ↓
2. Agent调用 /api/match-school 识别用户身份
   ↓
3. 后端返回匹配的门派ID和信息
   ↓
4. 用户提出具体任务
   ↓
5. Agent调用 /api/skill/run 执行技能
   ↓
6. 后端智能评分，选择最优技能执行
   ↓
7. 返回技能执行结果，更新调用统计
```

## 接口测试示例

### 1. 获取门派列表

```bash
curl -X GET http://localhost:8000/api/schools
```

### 2. 匹配门派

```bash
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个APP"}'
```

### 3. 执行技能（智能匹配）

```bash
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "帮我拆解项目任务"}'
```

### 4. 获取门派技能列表（新增）

```bash
curl -X GET http://localhost:8000/api/schools/1/skills
```

## 🧪 测试新功能

运行完整测试脚本：

```bash
cd backend
./test_new_features.sh
```

运行基础测试：

```bash
cd backend
./test_api.sh
```

## 📁 项目结构

```
ai-skills-platform/
├── index.html                    # 前端页面（仅展示，无交互）
├── backend/
│   ├── main.py                  # FastAPI后端（v2.1，智能技能系统）
│   ├── skills_config.json       # ⭐️ 技能配置文件（可扩展）
│   ├── skills_stats.json        # ⭐️ 技能调用统计
│   ├── skills.json              # 旧版技能数据（已废弃）
│   ├── API_TEST.md              # 接口测试文档
│   ├── CHANGELOG.md             # ⭐️ 更新日志
│   ├── test_api.sh              # 基础测试脚本
│   └── test_new_features.sh     # ⭐️ 新功能测试脚本
└── README.md                     # 本文件
```

## 🎯 如何扩展技能

### 方法1：直接编辑配置文件（推荐）

编辑 `backend/skills_config.json`，添加新技能：

```json
{
  "skills": [
    {
      "skill_id": "s006",
      "school_id": 1,
      "name_cn": "竞品分析诀",
      "name_en": "Competitor Analysis",
      "description": "系统化分析竞品优劣势",
      "keywords": ["竞品", "分析", "对比", "市场"],
      "priority": 8,
      "response": "【竞品分析诀 - 执行结果】\n\n您的任务：{user_task}\n\n..."
    }
  ]
}
```

**无需重启服务，无需改代码！**

### 方法2：通过API扩展（待实现）

未来版本将支持通过API上传技能配置。

## 开发规划

### ✅ 已实现（v2.1）

- ✅ 四个核心API接口
- ✅ 关键词匹配引擎（identify_user_role）
- ✅ 四大门派 + 散修身份
- ✅ 11个技能（4个门派）
- ✅ 前端展示页面（Dark Botanical风格）
- ✅ 双语支持（EN/ZH切换）
- ✅ 智能技能评分与排序
- ✅ 关键词相似度匹配
- ✅ 重复技能检测
- ✅ 技能调用统计
- ✅ 可扩展的技能配置系统

### ⏳ 待扩展（后续版本）

- ⏳ 更多门派的技能（目标：每个门派10+技能）
- ⏳ 接入真实AI模型（Claude API）替换Mock结果
- ⏳ 用户身份档案系统
- ⏳ 技能使用历史记录
- ⏳ 技能效果反馈与评价
- ⏳ 用户自定义技能贡献（通过API上传）
- ⏳ 技能推荐系统
- ⏳ 数据分析与报表

## API规范

### 统一响应格式

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

### 错误响应

```json
{
  "detail": "错误描述"
}
```

HTTP状态码：
- `200` - 成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误

## 技术特点

1. **前后端分离**：前端纯展示，后端负责所有业务逻辑
2. **配置驱动**：技能数据存储在JSON配置文件，易于扩展
3. **智能评分**：动态计算技能得分，自动推荐最优技能
4. **无需数据库**：使用JSON文件存储，快速启动
5. **无需认证**：当前版本公开访问，简化测试
6. **关键词匹配**：简单高效的规则引擎
7. **自动文档**：FastAPI自动生成Swagger文档

## 设计风格

- **配色方案**：深色系（高级、专业、神秘）
  - 背景：深黑 `#0f0f0f`、深灰 `#1a1a1a`
  - 卡片：`#1e1e1e`
  - 强调色：金色 `#d4a574`、粉色 `#e8b4b8`
  - 文字：主文字 `#e8e4df`、次要文字 `#9a9590`
- **字体**：Cormorant (衬线) + IBM Plex Sans (无衬线)

## 许可证

MIT

---

**Built with ❤️ for AI Agents**

**Version**: 2.1.0
**Last Updated**: 2025-01
