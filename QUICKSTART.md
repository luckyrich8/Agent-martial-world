# Martial World 快速上手指南

## 🚀 5分钟快速启动

### 第一步：启动后端

```bash
cd backend
python3 main.py
```

✅ 看到 `Uvicorn running on http://0.0.0.0:8000` 表示启动成功

### 第二步：测试接口

```bash
# 测试1：获取所有门派
curl http://localhost:8000/api/schools

# 测试2：匹配门派（我是产品经理）
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个APP"}'

# 测试3：执行技能（拆解任务）
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "帮我拆解做社交APP的任务"}'

# 测试4：查看枢机阁的所有技能
curl http://localhost:8000/api/schools/1/skills
```

### 第三步：查看API文档

打开浏览器访问：`http://localhost:8000/docs`

## 📊 新功能亮点

### 1. 智能技能评分

系统会自动计算每个技能的得分：

```
得分 = 平台priority + 调用次数 + 关键词匹配度 - 重复惩罚
```

**示例：**
- 用户输入："帮我拆解任务"
- 系统自动匹配到"任务拆解术"（priority: 10，关键词匹配度高）

### 2. 技能配置扩展

无需改代码，直接编辑 `skills_config.json`：

```json
{
  "skill_id": "s006",
  "school_id": 1,
  "name_cn": "竞品分析诀",
  "name_en": "Competitor Analysis",
  "description": "系统化分析竞品优劣势",
  "keywords": ["竞品", "分析", "对比"],
  "priority": 8,
  "response": "你的技能输出模板..."
}
```

保存后，下次调用自动生效！

### 3. 调用统计追踪

查看 `skills_stats.json`：

```json
{
  "stats": {
    "s002": 5,  // 任务拆解术被调用5次
    "s001": 3   // 需求洞察诀被调用3次
  }
}
```

热门技能会自动获得评分加成。

## 🎯 使用场景

### 场景1：产品经理拆解任务

```bash
# 1. 先匹配身份
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我是产品经理"}'

# 返回：school_id = 1（枢机阁）

# 2. 执行技能
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "拆解做小红书的任务"}'
```

### 场景2：设计师优化UX

```bash
# 1. 匹配身份
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我是设计师，需要优化界面"}'

# 返回：school_id = 2（丹青阁）

# 2. 执行技能
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 2, "user_task": "优化登录页面的用户体验"}'
```

### 场景3：运营策划增长活动

```bash
# 1. 匹配身份
curl -X POST http://localhost:8000/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我需要提升用户增长"}'

# 返回：school_id = 4（天机阁）

# 2. 执行技能
curl -X POST http://localhost:8000/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 4, "user_task": "策划一个拉新活动"}'
```

## 🧪 运行完整测试

```bash
cd backend

# 测试所有新功能
./test_new_features.sh

# 测试基础接口
./test_api.sh
```

## 📚 更多文档

- **API详细文档**：`backend/API_TEST.md`
- **更新日志**：`backend/CHANGELOG.md`
- **完整README**：`README.md`

## ❓ 常见问题

**Q: 如何添加新技能？**
A: 编辑 `backend/skills_config.json`，添加技能配置，无需重启服务。

**Q: 技能是如何选择的？**
A: 系统根据关键词匹配度、调用次数、优先级自动计算得分，返回得分最高的技能。

**Q: 如何查看某个门派的所有技能？**
A: 访问 `GET /api/schools/{school_id}/skills`

**Q: 调用统计数据存在哪里？**
A: `backend/skills_stats.json`

## 🎉 开始使用

```bash
# 一键启动
cd backend && python3 main.py

# 访问文档
open http://localhost:8000/docs
```

Happy coding! 🚀
