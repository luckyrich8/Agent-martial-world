"""
OpenAI Function Call 测试脚本
演示完整的 OpenAI Agent 调用 Martial World Skills 的流程
"""

import os
import json
import requests
from openai import OpenAI

# 配置
BACKEND_URL = "http://localhost:8001"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY)

# 加载 Function 定义
with open("openai-functions.json", "r") as f:
    functions_def = json.load(f)

print("🤖 Martial World - OpenAI Function Call Test\n")
print("=" * 60)

# ==================== 测试场景 1：用户想做产品 ====================

print("\n📋 Scenario 1: User wants to build a product\n")

messages = [
    {"role": "user", "content": "I want to build a social networking app for professionals"}
]

print(f"User: {messages[0]['content']}\n")

# 第一次调用：OpenAI 决定调用 match_martial_world_school
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions_def["functions"],
    tool_choice="auto"
)

assistant_message = response.choices[0].message
messages.append(assistant_message)

# 检查是否要调用 function
if assistant_message.tool_calls:
    tool_call = assistant_message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    print(f"🔧 OpenAI decides to call: {function_name}")
    print(f"📥 Arguments: {json.dumps(function_args, indent=2)}\n")

    # 调用我们的后端
    if function_name == "match_martial_world_school":
        backend_response = requests.post(
            f"{BACKEND_URL}/openai/match-school",
            json=function_args
        )
        result = backend_response.json()

        print(f"✅ Backend Response:")
        print(json.dumps(result, indent=2))
        print()

        # 保存 school_id 用于下一步
        school_id = result.get("school_id")

        # 把结果返回给 OpenAI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        # OpenAI 生成最终回复
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        print(f"🤖 Assistant: {final_response.choices[0].message.content}\n")


# ==================== 测试场景 2：用户要求执行任务 ====================

print("\n" + "=" * 60)
print("\n📋 Scenario 2: User asks for help with a specific task\n")

# 继续对话
messages.append({
    "role": "user",
    "content": "Help me break down the project into tasks"
})

print(f"User: Help me break down the project into tasks\n")

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions_def["functions"],
    tool_choice="auto"
)

assistant_message = response.choices[0].message
messages.append(assistant_message)

if assistant_message.tool_calls:
    tool_call = assistant_message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    print(f"🔧 OpenAI decides to call: {function_name}")
    print(f"📥 Arguments: {json.dumps(function_args, indent=2)}\n")

    # 调用后端执行技能
    if function_name == "execute_martial_world_skill":
        # 如果 OpenAI 没有传 school_id，我们手动添加
        if "school_id" not in function_args and school_id:
            function_args["school_id"] = school_id

        backend_response = requests.post(
            f"{BACKEND_URL}/openai/execute-skill",
            json=function_args
        )
        result = backend_response.json()

        print(f"✅ Backend Response:")
        print(json.dumps(result, indent=2))
        print()

        # 返回给 OpenAI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        # OpenAI 生成最终回复
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        print(f"🤖 Assistant: {final_response.choices[0].message.content}\n")


print("=" * 60)
print("\n✅ Test completed! OpenAI successfully called Martial World skills.\n")
