#!/bin/bash

echo "🧪 Testing Martial World OpenAI Backend"
echo "========================================"
echo ""

echo "📋 Test 1: Match School"
echo "------------------------"
echo "Input: 'I want to build a mobile app'"
curl -s -X POST http://localhost:8001/openai/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I want to build a mobile app"}' | python3 -m json.tool
echo ""

echo "Input: 'I need to design a website'"
curl -s -X POST http://localhost:8001/openai/match-school \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I need to design a website"}' | python3 -m json.tool
echo ""

echo "========================================"
echo ""
echo "📋 Test 2: Execute Skills"
echo "------------------------"
echo "Task: 'Help me break down project tasks'"
curl -s -X POST http://localhost:8001/openai/execute-skill \
  -H "Content-Type: application/json" \
  -d '{"school_id": 1, "user_task": "Help me break down project tasks"}' | python3 -m json.tool
echo ""

echo "Task: 'Design a beautiful interface'"
curl -s -X POST http://localhost:8001/openai/execute-skill \
  -H "Content-Type: application/json" \
  -d '{"school_id": 2, "user_task": "Design a beautiful interface"}' | python3 -m json.tool
echo ""

echo "========================================"
echo ""
echo "✅ All tests completed!"
echo ""
echo "💡 Backend is running at: http://localhost:8001"
echo "💡 Function definitions at: http://localhost:8001/openai/functions"
