#!/bin/bash

# Martial World API v2.1 新功能测试脚本

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Martial World API v2.1 新功能测试"
echo "=========================================="
echo ""

# 测试1：获取枢机阁的技能列表
echo "📋 测试 1：获取枢机阁（产品经理门派）的所有技能"
echo "----------------------------------------"
curl -s -X GET $BASE_URL/api/schools/1/skills | python3 -m json.tool
echo ""
echo ""

# 测试2：智能技能匹配 - 拆解任务
echo "🎯 测试 2：智能技能匹配（关键词：拆解）"
echo "----------------------------------------"
echo "任务：帮我拆解一下做社交APP的任务"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "帮我拆解一下做社交APP的任务"}' | python3 -m json.tool
echo ""
echo ""

# 测试3：智能技能匹配 - 需求分析
echo "🔍 测试 3：智能技能匹配（关键词：需求、分析）"
echo "----------------------------------------"
echo "任务：用户想要一个数据分析功能，帮我分析需求"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "用户想要一个数据分析功能，帮我分析需求"}' | python3 -m json.tool
echo ""
echo ""

# 测试4：智能技能匹配 - 优先级
echo "📊 测试 4：智能技能匹配（关键词：优先级）"
echo "----------------------------------------"
echo "任务：这三个功能的优先级怎么排"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "这三个功能的优先级怎么排"}' | python3 -m json.tool
echo ""
echo ""

# 测试5：智能技能匹配 - 方案
echo "📝 测试 5：智能技能匹配（关键词：方案、PRD）"
echo "----------------------------------------"
echo "任务：写一份产品PRD方案"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "写一份产品PRD方案"}' | python3 -m json.tool
echo ""
echo ""

# 测试6：智能技能匹配 - 风险
echo "⚠️ 测试 6：智能技能匹配（关键词：风险、应对）"
echo "----------------------------------------"
echo "任务：这个项目有什么风险需要预判"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "这个项目有什么风险需要预判"}' | python3 -m json.tool
echo ""
echo ""

# 测试7：获取丹青阁的技能列表
echo "🎨 测试 7：获取丹青阁（设计师门派）的所有技能"
echo "----------------------------------------"
curl -s -X GET $BASE_URL/api/schools/2/skills | python3 -m json.tool
echo ""
echo ""

# 测试8：设计师门派技能匹配
echo "🖌️ 测试 8：设计师门派 - 智能匹配UI设计技能"
echo "----------------------------------------"
echo "任务：设计一个登录界面"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 2, "user_task": "设计一个登录界面"}' | python3 -m json.tool
echo ""
echo ""

# 测试9：获取烟雨楼的技能列表
echo "✍️  测试 9：获取烟雨楼（文案门派）的所有技能"
echo "----------------------------------------"
curl -s -X GET $BASE_URL/api/schools/3/skills | python3 -m json.tool
echo ""
echo ""

# 测试10：文案门派技能匹配
echo "📝 测试 10：文案门派 - 智能匹配文案创作技能"
echo "----------------------------------------"
echo "任务：写一个吸引人的产品文案"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 3, "user_task": "写一个吸引人的产品文案"}' | python3 -m json.tool
echo ""
echo ""

# 测试11：获取天机阁的技能列表
echo "📈 测试 11：获取天机阁（运营门派）的所有技能"
echo "----------------------------------------"
curl -s -X GET $BASE_URL/api/schools/4/skills | python3 -m json.tool
echo ""
echo ""

# 测试12：运营门派技能匹配
echo "🚀 测试 12：运营门派 - 智能匹配增长策略技能"
echo "----------------------------------------"
echo "任务：如何提升用户增长和转化"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 4, "user_task": "如何提升用户增长和转化"}' | python3 -m json.tool
echo ""
echo ""

# 测试13：查看调用统计
echo "📊 测试 13：查看技能调用统计数据"
echo "----------------------------------------"
echo "查看 skills_stats.json 文件："
cat skills_stats.json | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "✅ 所有新功能测试完成！"
echo "=========================================="
echo ""
echo "💡 新功能说明："
echo "  1. ✨ 技能配置系统 - skills_config.json 存储所有技能"
echo "  2. 📊 智能评分排序 - priority + 调用次数 + 关键词匹配 - 重复惩罚"
echo "  3. 🔍 关键词相似度匹配 - 自动选择最佳技能"
echo "  4. 🎯 重复技能检测 - 关键词重叠度>50%自动识别"
echo "  5. 📈 调用统计追踪 - skills_stats.json 记录使用频次"
echo "  6. 🆕 新接口：GET /api/schools/{school_id}/skills - 获取门派技能列表"
echo ""
echo "🔧 如何扩展技能："
echo "  直接编辑 skills_config.json，添加新技能配置即可，无需改代码"
echo ""
