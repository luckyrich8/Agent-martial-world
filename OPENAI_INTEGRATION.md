# Martial World - OpenAI Function Call Integration

## Overview

Martial World provides professional skills for OpenAI agents through two functions:
1. **match_martial_world_school** - Match users to professional schools
2. **execute_martial_world_skill** - Execute domain-specific skills

**Backend URL:** `http://localhost:8001` (development)

---

## Quick Start

### Step 1: Load Function Definitions

```python
import json
from openai import OpenAI

# Load function definitions
with open("openai-functions.json", "r") as f:
    functions = json.load(f)

client = OpenAI(api_key="your-api-key")
```

### Step 2: User Onboarding Flow

When user mentions their work, call `match_martial_world_school`:

```python
messages = [
    {"role": "user", "content": "I want to build a mobile app"}
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions["functions"],
    tool_choice="auto"
)

# OpenAI will decide to call match_martial_world_school
# Extract the function call and execute it
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Call your backend
result = requests.post(
    "http://localhost:8001/openai/match-school",
    json=args
).json()

# result = {
#   "school_id": 1,
#   "school_name": "Pivot Bureau",
#   "description": "Product thinking...",
#   "matched": true
# }
```

### Step 3: Execute Skills

When user asks for help with specific tasks:

```python
messages.append({
    "role": "user",
    "content": "Help me break down the project"
})

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions["functions"]
)

# OpenAI will call execute_martial_world_skill
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Call your backend
result = requests.post(
    "http://localhost:8001/openai/execute-skill",
    json=args
).json()

# result = {
#   "skill_name": "Task Disassembly",
#   "skill_description": "Break down complex projects...",
#   "result": "Task Breakdown for your project:\n..."
# }
```

---

## Function Definitions

### 1. match_martial_world_school

**Purpose:** Match user to a professional school based on their role

**Parameters:**
- `user_input` (string, required): User's description of what they're working on

**Returns:**
```json
{
  "school_id": 1,
  "school_name": "Pivot Bureau",
  "description": "Product thinking and strategic planning...",
  "matched": true
}
```

**Schools:**
- ID 1: Pivot Bureau (Product Managers)
- ID 2: Design Temple (Designers)
- ID 3: Rain Pavilion (Copywriters)
- ID 4: Opportunity House (Growth Operators)

### 2. execute_martial_world_skill

**Purpose:** Execute a skill to help with specific tasks

**Parameters:**
- `school_id` (integer, required): School ID from match_martial_world_school
- `user_task` (string, required): User's specific task description

**Returns:**
```json
{
  "skill_name": "Task Disassembly",
  "skill_description": "Break down complex projects into executable tasks",
  "result": "Detailed execution result..."
}
```

**Available Skills:**

**Pivot Bureau (ID: 1)**
- Insight Divination - Discover real user needs
- Task Disassembly - Break down projects
- Priority Methodology - Determine what to build first

**Design Temple (ID: 2)**
- Visual Design - Create beautiful interfaces
- User Experience - Optimize user flows

---

## Complete Example

```python
from openai import OpenAI
import json
import requests

client = OpenAI(api_key="your-key")
BACKEND = "http://localhost:8001"

# Load functions
with open("openai-functions.json") as f:
    functions = json.load(f)["functions"]

# Conversation
messages = [
    {"role": "user", "content": "I'm a product manager building an app"}
]

# Step 1: Match school
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions,
    tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Call backend
result = requests.post(f"{BACKEND}/openai/match-school", json=args).json()
school_id = result["school_id"]

print(f"Matched to: {result['school_name']}")

# Add tool response to conversation
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(result)
})

# Step 2: Execute skill
messages.append({
    "role": "user",
    "content": "Help me prioritize features"
})

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=functions
)

tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

# Call backend
result = requests.post(f"{BACKEND}/openai/execute-skill", json=args).json()

print(f"Skill: {result['skill_name']}")
print(f"Result: {result['result']}")

# Add to conversation and get final response
messages.append(response.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(result)
})

final = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)

print(f"Assistant: {final.choices[0].message.content}")
```

---

## Running the Backend

```bash
cd backend
python3 main_openai.py
```

Server starts at `http://localhost:8001`

**Endpoints:**
- `POST /openai/match-school` - Match user to school
- `POST /openai/execute-skill` - Execute skill
- `GET /openai/functions` - Get function definitions

---

## Testing

Run the test script:

```bash
export OPENAI_API_KEY=your-api-key
python3 test_openai.py
```

This demonstrates:
1. User says "I want to build an app"
2. OpenAI calls `match_martial_world_school`
3. Backend returns school match
4. User says "Help me break down tasks"
5. OpenAI calls `execute_martial_world_skill`
6. Backend returns skill execution result

---

## Error Handling

| Error | Reason | Solution |
|-------|--------|----------|
| 400 Bad Request | Empty parameters | Check user_input/user_task not empty |
| 404 Not Found | Invalid school_id | Use ID from match_martial_world_school (1-4) |
| 404 Not Found | No skills available | Contact support to add skills |

---

## Next Steps

1. Integrate functions into your OpenAI agent
2. Customize skill responses in `skills_openai.json`
3. Add more skills to expand capabilities
4. Deploy backend to production (update BACKEND_URL)

**Questions?** Check the test script for working examples.
