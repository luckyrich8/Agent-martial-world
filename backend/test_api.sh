#!/bin/bash

# Martial World API 快速测试脚本

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Martial World API 测试"
echo "=========================================="
echo ""

# 测试1：获取门派列表
echo "📋 测试 1：获取所有门派列表"
echo "----------------------------------------"
curl -s -X GET $BASE_URL/api/schools | python3 -m json.tool
echo ""
echo ""

# 测试2：匹配门派 - 产品经理
echo "🎯 测试 2：匹配门派（产品经理）"
echo "----------------------------------------"
echo "输入：我要做一个APP"
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我要做一个APP"}' | python3 -m json.tool
echo ""
echo ""

# 测试3：匹配门派 - 设计师
echo "🎨 测试 3：匹配门派（设计师）"
echo "----------------------------------------"
echo "输入：帮我设计一个登录界面"
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "帮我设计一个登录界面"}' | python3 -m json.tool
echo ""
echo ""

# 测试4：匹配门派 - 文案
echo "✍️  测试 4：匹配门派（文案）"
echo "----------------------------------------"
echo "输入：我需要写一篇公众号文案"
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "我需要写一篇公众号文案"}' | python3 -m json.tool
echo ""
echo ""

# 测试5：匹配门派 - 运营
echo "📈 测试 5：匹配门派（运营）"
echo "----------------------------------------"
echo "输入：如何提升用户留存和增长"
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "如何提升用户留存和增长"}' | python3 -m json.tool
echo ""
echo ""

# 测试6：匹配门派 - 散修
echo "🌟 测试 6：匹配门派（散修 - 无法识别）"
echo "----------------------------------------"
echo "输入：今天天气真好"
curl -s -X POST $BASE_URL/api/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "今天天气真好"}' | python3 -m json.tool
echo ""
echo ""

# 测试7：执行技能 - 任务拆解
echo "🔧 测试 7：执行技能（任务拆解术）"
echo "----------------------------------------"
echo "门派：枢机阁，任务：帮我拆解做社交APP的任务"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "帮我拆解做社交APP的任务"}' | python3 -m json.tool
echo ""
echo ""

# 测试8：执行技能 - 需求洞察
echo "🔍 测试 8：执行技能（需求洞察诀）"
echo "----------------------------------------"
echo "门派：枢机阁，任务：用户想要一个数据分析功能"
curl -s -X POST $BASE_URL/api/skill/run \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "用户想要一个数据分析功能"}' | python3 -m json.tool
echo ""
echo ""

echo "=========================================="
echo "✅ 所有测试完成！"
echo "=========================================="
echo ""
echo "💡 提示："
echo "  - API文档：http://localhost:8000/docs"
echo "  - 根路由：http://localhost:8000"
echo "  - 详细文档：查看 API_TEST.md"
