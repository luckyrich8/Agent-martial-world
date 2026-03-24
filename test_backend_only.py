"""
Martial World Backend 测试（不需要 OpenAI API Key）
直接测试后端接口是否正常工作
"""

import requests
import json

BACKEND_URL = "http://localhost:8001"

print("🧪 Testing Martial World OpenAI Backend\n")
print("=" * 60)

# ==================== 测试 1：匹配门派 ====================

print("\n📋 Test 1: Match School\n")

test_inputs = [
    "I want to build a mobile app",
    "I'm a designer working on UI",
    "I need to write marketing copy",
    "I want to grow my user base"
]

for user_input in test_inputs:
    print(f"Input: {user_input}")

    response = requests.post(
        f"{BACKEND_URL}/openai/match-school",
        json={"user_input": user_input}
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Matched: {result['school_name']} (ID: {result['school_id']})")
        print(f"   {result['description']}\n")
    else:
        print(f"❌ Error: {response.status_code}\n")


# ==================== 测试 2：执行技能 ====================

print("\n" + "=" * 60)
print("\n📋 Test 2: Execute Skills\n")

test_cases = [
    {
        "school_id": 1,
        "user_task": "Help me break down project tasks"
    },
    {
        "school_id": 1,
        "user_task": "Analyze user requirements"
    },
    {
        "school_id": 2,
        "user_task": "Design a beautiful interface"
    }
]

for test in test_cases:
    print(f"School ID: {test['school_id']}")
    print(f"Task: {test['user_task']}")

    response = requests.post(
        f"{BACKEND_URL}/openai/execute-skill",
        json=test
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Skill: {result['skill_name']}")
        print(f"📋 Result Preview:")
        print(result['result'][:200] + "...\n")
    else:
        print(f"❌ Error: {response.status_code}\n")


# ==================== 测试 3：获取 Function 定义 ====================

print("\n" + "=" * 60)
print("\n📋 Test 3: Get Function Definitions\n")

response = requests.get(f"{BACKEND_URL}/openai/functions")

if response.status_code == 200:
    functions = response.json()
    print(f"✅ Found {len(functions['functions'])} functions:")
    for func in functions['functions']:
        print(f"   - {func['function']['name']}")
    print()
else:
    print(f"❌ Error: {response.status_code}\n")


print("=" * 60)
print("\n✅ All tests completed!\n")
print("💡 To test with real OpenAI integration, run:")
print("   export OPENAI_API_KEY=your-key")
print("   python3 test_openai.py\n")
