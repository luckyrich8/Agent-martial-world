# Martial World API 更新日志

## v2.1.0 (2025-01-XX) - 智能技能系统

### 🆕 新增功能

1. **技能配置系统**
   - 新增 `skills_config.json` - 结构化技能配置文件
   - 支持无代码扩展，直接编辑配置即可添加新技能
   - 技能字段：skill_id, school_id, name_cn/name_en, description, keywords, priority, response

2. **智能技能评分与排序**
   - 评分公式：`最终得分 = 平台priority + 调用次数加成 + 关键词匹配度 - 重复惩罚`
   - 自动选择得分最高的技能返回给用户
   - 动态调整，越常用的技能得分越高

3. **关键词相似度匹配**
   - 计算用户任务与技能关键词的相似度（0-1）
   - 相似度越高，技能得分越高
   - 实现函数：`calculate_keyword_similarity()`

4. **重复技能检测**
   - 自动识别同门派下关键词重叠度>50%的重复技能
   - 重复技能会受到得分惩罚
   - 实现函数：`detect_duplicate_skills()`

5. **技能调用统计**
   - 新增 `skills_stats.json` - 记录每个技能的调用次数
   - 自动更新，每次调用技能后+1
   - 调用次数影响技能评分（每10次调用+1分，最多+5分）

### 🔄 升级接口

#### POST /api/skill/run（升级）
- **原功能**：简单的关键词匹配返回技能
- **新功能**：智能检索、评分、排序，返回最优技能
- **内部逻辑**：
  1. 筛选该门派的所有技能
  2. 检测重复技能
  3. 计算每个技能的得分
  4. 返回得分最高的技能
  5. 更新调用统计
- **返回字段新增**：
  - `skill_name_en` - 技能英文名
  - `description` - 技能描述

### ➕ 新增接口

#### GET /api/schools/{school_id}/skills
- **功能**：获取指定门派的所有技能列表
- **参数**：
  - `school_id` (路径参数) - 门派ID，必填
- **返回**：
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
          "keywords": ["拆解", "任务", "步骤", "规划"],
          "priority": 10,
          "call_count": 0
        }
      ]
    },
    "message": "获取技能列表成功"
  }
  ```

### 📁 新增文件

- `skills_config.json` - 技能配置文件（11个技能，覆盖4个门派）
- `skills_stats.json` - 技能调用统计数据
- `test_new_features.sh` - 新功能测试脚本
- `CHANGELOG.md` - 本文件

### 🔧 技术改进

1. **代码重构**
   - 从硬编码技能数据迁移到配置文件
   - 添加 `load_skills_config()` 和 `load_skills_stats()` 函数
   - 实现智能评分系统的核心算法

2. **可扩展性**
   - 新增技能：直接编辑 `skills_config.json`
   - 无需重启服务（下次请求时自动加载）
   - 支持无限扩展技能

3. **数据持久化**
   - 技能调用统计自动保存到 `skills_stats.json`
   - 服务重启后统计数据不丢失

### 📊 当前技能库

- **枢机阁（产品经理）**：5个技能
  - 需求洞察诀 (priority: 9)
  - 任务拆解术 (priority: 10)
  - 优先级心法 (priority: 8)
  - 方案撰写式 (priority: 9)
  - 风险预判诀 (priority: 7)

- **丹青阁（设计师）**：2个技能
  - 视觉设计诀 (priority: 8)
  - 用户体验术 (priority: 9)

- **烟雨楼（文案）**：2个技能
  - 文案创作诀 (priority: 8)
  - 故事叙事术 (priority: 7)

- **天机阁（运营）**：2个技能
  - 增长策略诀 (priority: 9)
  - 运营规划术 (priority: 8)

### 🧪 测试方法

运行新功能测试脚本：
```bash
cd backend
./test_new_features.sh
```

### 🔮 后续计划

- [ ] 支持用户自定义技能上传
- [ ] 技能评价与反馈机制
- [ ] 技能推荐系统
- [ ] 接入真实AI模型（Claude API）
- [ ] 技能使用分析与报表

---

## v2.0.0 (2025-01-XX) - 初始版本

### 核心功能

1. GET /api/schools - 获取所有门派列表
2. POST /api/match-school - 根据自然语言匹配门派
3. POST /api/skill/run - 执行指定门派的技能

### 基础能力

- 关键词匹配识别用户身份
- Mock数据演示
- 四大门派：枢机阁、丹青阁、烟雨楼、天机阁
- 散修身份（无法识别时）
