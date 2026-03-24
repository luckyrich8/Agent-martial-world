"""
Martial World - OpenAI Function Call Backend
为 OpenAI GPT 提供专业技能调用服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="Martial World - OpenAI Functions",
    version="1.0.0",
    description="Professional skills platform for OpenAI agents"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据加载 ====================

# 门派数据
SCHOOLS_DATA = [
    {
        "id": 1,
        "name_en": "Pivot Bureau",
        "description": "Product thinking and strategic planning. For Product Managers, Project Managers, Entrepreneurs.",
        "role": "product_manager"
    },
    {
        "id": 2,
        "name_en": "Design Temple",
        "description": "Aesthetics and user experience. For UI/UX Designers, Visual Designers.",
        "role": "designer"
    },
    {
        "id": 3,
        "name_en": "Rain Pavilion",
        "description": "Content and storytelling. For Copywriters, Content Creators, Scriptwriters.",
        "role": "copywriter"
    },
    {
        "id": 4,
        "name_en": "Opportunity House",
        "description": "Growth and operations. For Growth Operators, Growth Hackers, Marketing Strategists.",
        "role": "operator"
    }
]

# 技能数据（假数据，从配置文件加载）
def load_skills_config():
    """加载技能配置"""
    config_path = "skills_openai.json"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

SKILLS_CONFIG = load_skills_config()


# ==================== 请求模型 ====================

class MatchSchoolRequest(BaseModel):
    user_input: str


class ExecuteSkillRequest(BaseModel):
    school_id: int
    user_task: str


# ==================== 核心逻辑 ====================

def identify_user_role(user_input: str) -> str:
    """识别用户职业角色"""
    text = user_input.lower()

    # 产品经理关键词
    if any(kw in text for kw in ["product", "requirement", "prd", "project", "app", "feature", "iteration", "prototype"]):
        return "product_manager"

    # 设计师关键词
    if any(kw in text for kw in ["design", "ui", "interface", "visual", "icon", "layout", "ux", "interaction"]):
        return "designer"

    # 文案关键词
    if any(kw in text for kw in ["copy", "writing", "content", "blog", "script", "article", "headline", "creative"]):
        return "copywriter"

    # 运营关键词
    if any(kw in text for kw in ["operation", "growth", "traffic", "monetization", "campaign", "community", "promotion", "acquisition"]):
        return "operator"

    return "unknown"


def calculate_keyword_similarity(task_text: str, skill_keywords: list) -> float:
    """计算关键词相似度"""
    task_lower = task_text.lower()
    matches = sum(1 for keyword in skill_keywords if keyword.lower() in task_lower)
    return matches / len(skill_keywords) if skill_keywords else 0.0


def find_best_skill(school_id: int, user_task: str) -> dict:
    """找到最佳技能"""
    school_skills = [s for s in SKILLS_CONFIG.get("skills", []) if s["school_id"] == school_id]

    if not school_skills:
        return None

    # 计算每个技能的得分
    scored_skills = []
    for skill in school_skills:
        similarity = calculate_keyword_similarity(user_task, skill.get("keywords", []))
        score = skill.get("priority", 5) + (similarity * 5)
        scored_skills.append({"skill": skill, "score": score})

    # 返回得分最高的
    scored_skills.sort(key=lambda x: x["score"], reverse=True)
    return scored_skills[0]["skill"] if scored_skills else None


# ==================== OpenAI Function 端点 ====================

@app.post("/openai/match-school")
async def match_school(request: MatchSchoolRequest):
    """
    OpenAI Function: match_martial_world_school
    匹配用户到门派
    """
    user_input = request.user_input.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="user_input cannot be empty")

    # 识别用户角色
    role = identify_user_role(user_input)

    # 匹配门派
    matched_school = next((s for s in SCHOOLS_DATA if s["role"] == role), None)

    if not matched_school:
        # 返回散修（未匹配）
        return {
            "school_id": None,
            "school_name": "Wanderer",
            "description": "Unable to identify your professional type. You can explore all schools.",
            "matched": False
        }

    # 返回匹配结果（简化格式，适合 OpenAI）
    return {
        "school_id": matched_school["id"],
        "school_name": matched_school["name_en"],
        "description": matched_school["description"],
        "matched": True
    }


@app.post("/openai/execute-skill")
async def execute_skill(request: ExecuteSkillRequest):
    """
    OpenAI Function: execute_martial_world_skill
    执行技能
    """
    school_id = request.school_id
    user_task = request.user_task.strip()

    if not user_task:
        raise HTTPException(status_code=400, detail="user_task cannot be empty")

    # 检查门派是否存在
    school = next((s for s in SCHOOLS_DATA if s["id"] == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail=f"School ID {school_id} does not exist")

    # 找到最佳技能
    best_skill = find_best_skill(school_id, user_task)

    if not best_skill:
        raise HTTPException(status_code=404, detail=f"No skills available for {school['name_en']}")

    # 返回结果（简化格式）
    return {
        "skill_name": best_skill["name_en"],
        "skill_description": best_skill["description"],
        "result": best_skill.get("mock_response", "Skill executed successfully")
    }


@app.get("/openai/functions")
async def get_functions():
    """返回 OpenAI Function 定义"""
    with open("../openai-functions.json", "r") as f:
        return json.load(f)


@app.get("/")
async def root():
    """根路由"""
    return {
        "service": "Martial World - OpenAI Functions",
        "version": "1.0.0",
        "endpoints": {
            "POST /openai/match-school": "Match user to a school",
            "POST /openai/execute-skill": "Execute a skill",
            "GET /openai/functions": "Get OpenAI function definitions"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Martial World OpenAI Backend starting...")
    print("📖 OpenAI Functions available at: http://localhost:8001/openai/functions")
    uvicorn.run(app, host="0.0.0.0", port=8001)
