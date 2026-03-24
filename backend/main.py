"""
Martial World - 后端API (扩展版)
外部AI Agent通过接口调用本平台功能
后端负责：语义理解、身份识别、门派匹配、技能执行、智能评分排序
前端仅做展示，无用户交互
"""

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import os
from collections import defaultdict

app = FastAPI(title="Martial World API", version="2.1.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据加载 ====================

# 门派数据（Mock）
SCHOOLS_DATA = [
    {
        "id": 1,
        "name_zh": "枢机阁",
        "name_en": "Pivot Bureau",
        "description": "产品思维为心法，决策规划为招式。适合产品经理、项目经理、创业者。",
        "role": "product_manager"
    },
    {
        "id": 2,
        "name_zh": "丹青阁",
        "name_en": "Design Temple",
        "description": "以美学为基，以用户体验为本。适合UI/UX设计师、视觉设计师。",
        "role": "designer"
    },
    {
        "id": 3,
        "name_zh": "烟雨楼",
        "name_en": "Rain Pavilion",
        "description": "字句如刀，内容为王。适合文案策划、内容创作者、编剧。",
        "role": "copywriter"
    },
    {
        "id": 4,
        "name_zh": "天机阁",
        "name_en": "Opportunity House",
        "description": "洞察人性，驱动增长。适合运营专家、增长黑客、市场策略。",
        "role": "operator"
    }
]

# 加载技能配置
def load_skills_config():
    """加载技能配置文件"""
    config_path = "skills_config.json"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("skills", [])
    return []

# 加载技能统计数据
def load_skills_stats():
    """加载技能调用统计数据"""
    stats_path = "skills_stats.json"
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("stats", {})
    return {}

# 保存技能统计数据
def save_skills_stats(stats: dict):
    """保存技能调用统计数据"""
    stats_path = "skills_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump({"stats": stats}, f, ensure_ascii=False, indent=2)

# 全局数据
SKILLS_CONFIG = load_skills_config()
SKILLS_STATS = load_skills_stats()


# ==================== 请求/响应模型 ====================

class MatchSchoolRequest(BaseModel):
    user_input: str  # 用户说的原话


class SkillRunRequest(BaseModel):
    school_id: int  # 门派ID
    user_task: str  # 用户任务描述


# ==================== 核心逻辑：身份识别 ====================

def identify_user_role(user_input: str) -> str:
    """
    根据用户自然语言输入，通过关键词匹配识别用户身份
    返回：product_manager | designer | copywriter | operator | unknown
    """
    text = user_input.lower()

    # 产品经理关键词
    product_keywords = ["产品", "需求", "prd", "项目", "app", "功能", "迭代", "拆解", "原型", "产品经理"]
    if any(keyword in text for keyword in product_keywords):
        return "product_manager"

    # 设计师关键词
    design_keywords = ["设计", "ui", "界面", "视觉", "图标", "版式", "ux", "交互", "设计师"]
    if any(keyword in text for keyword in design_keywords):
        return "designer"

    # 文案关键词
    copy_keywords = ["文案", "写作", "内容", "博主", "脚本", "推文", "文章", "标题", "创作"]
    if any(keyword in text for keyword in copy_keywords):
        return "copywriter"

    # 运营关键词
    operation_keywords = ["运营", "增长", "流量", "变现", "活动", "社群", "推广", "拉新", "留存"]
    if any(keyword in text for keyword in operation_keywords):
        return "operator"

    # 无法识别
    return "unknown"


# ==================== 核心逻辑：关键词相似度计算 ====================

def calculate_keyword_similarity(task_text: str, skill_keywords: List[str]) -> float:
    """
    计算用户任务与技能关键词的相似度
    返回：0-1之间的相似度分数
    """
    task_lower = task_text.lower()
    matches = sum(1 for keyword in skill_keywords if keyword.lower() in task_lower)
    if len(skill_keywords) == 0:
        return 0.0
    return matches / len(skill_keywords)


def detect_duplicate_skills(school_id: int) -> Dict[str, List[str]]:
    """
    检测同一门派下的重复技能
    返回：{skill_id: [duplicate_skill_ids]} 映射
    """
    school_skills = [s for s in SKILLS_CONFIG if s["school_id"] == school_id]
    duplicates = {}

    for i, skill1 in enumerate(school_skills):
        similar_skills = []
        keywords1 = set(skill1["keywords"])

        for j, skill2 in enumerate(school_skills):
            if i != j:
                keywords2 = set(skill2["keywords"])
                # 计算关键词重叠度
                intersection = len(keywords1 & keywords2)
                union = len(keywords1 | keywords2)
                if union > 0:
                    similarity = intersection / union
                    # 如果相似度超过50%，认为是重复
                    if similarity >= 0.5:
                        similar_skills.append(skill2["skill_id"])

        if similar_skills:
            duplicates[skill1["skill_id"]] = similar_skills

    return duplicates


def calculate_skill_score(skill: dict, user_task: str, duplicates: Dict[str, List[str]]) -> float:
    """
    计算技能最终得分
    得分 = 平台priority + 调用次数加成 + 关键词匹配度加成 - 重复惩罚
    """
    skill_id = skill["skill_id"]

    # 基础分：平台priority (1-10)
    base_score = skill.get("priority", 5)

    # 调用次数加成 (每10次调用+1分，最多+5分)
    call_count = SKILLS_STATS.get(skill_id, 0)
    call_bonus = min(call_count / 10, 5)

    # 关键词匹配度加成 (0-5分)
    similarity = calculate_keyword_similarity(user_task, skill.get("keywords", []))
    similarity_bonus = similarity * 5

    # 重复惩罚 (每个重复技能-1分)
    duplicate_penalty = len(duplicates.get(skill_id, [])) * 1

    # 最终得分
    final_score = base_score + call_bonus + similarity_bonus - duplicate_penalty

    return max(final_score, 0)  # 确保得分不为负


def find_best_skill(school_id: int, user_task: str) -> Optional[dict]:
    """
    在指定门派下找到最佳技能
    1. 筛选该门派的所有技能
    2. 检测重复技能
    3. 计算每个技能的得分
    4. 返回得分最高的技能
    """
    # 筛选该门派的技能
    school_skills = [s for s in SKILLS_CONFIG if s["school_id"] == school_id]

    if not school_skills:
        return None

    # 检测重复技能
    duplicates = detect_duplicate_skills(school_id)

    # 计算每个技能的得分
    scored_skills = []
    for skill in school_skills:
        score = calculate_skill_score(skill, user_task, duplicates)
        scored_skills.append({
            "skill": skill,
            "score": score
        })

    # 按得分排序，返回最高分的技能
    scored_skills.sort(key=lambda x: x["score"], reverse=True)

    return scored_skills[0]["skill"] if scored_skills else None


def increment_skill_call_count(skill_id: str):
    """增加技能调用次数"""
    global SKILLS_STATS
    SKILLS_STATS[skill_id] = SKILLS_STATS.get(skill_id, 0) + 1
    save_skills_stats(SKILLS_STATS)


# ==================== 接口 1：获取所有门派列表 ====================

@app.get("/api/schools")
async def get_schools():
    """
    供外部Agent获取平台有哪些门派
    """
    return {
        "success": True,
        "data": SCHOOLS_DATA,
        "message": "获取门派列表成功"
    }


# ==================== 接口 2：根据自然语言匹配门派 ====================

@app.post("/api/match-school")
async def match_school(request: MatchSchoolRequest):
    """
    根据用户自然语言输入，后端自动识别身份并匹配门派
    """
    user_input = request.user_input.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="user_input 不能为空")

    # 识别用户身份
    role = identify_user_role(user_input)

    # 匹配门派
    matched_school = None
    for school in SCHOOLS_DATA:
        if school["role"] == role:
            matched_school = school
            break

    # 如果无法识别，返回散修身份
    if not matched_school:
        return {
            "success": True,
            "data": {
                "school_id": None,
                "school_name_zh": "散修（云游者）",
                "school_name_en": "Wanderer",
                "role": "unknown",
                "reason": "暂时无法识别您的职业类型，您可以作为散修自由探索各门派技能。"
            },
            "message": "匹配成功（散修）"
        }

    # 返回匹配结果
    return {
        "success": True,
        "data": {
            "school_id": matched_school["id"],
            "school_name_zh": matched_school["name_zh"],
            "school_name_en": matched_school["name_en"],
            "role": matched_school["role"],
            "reason": f"根据您的输入「{user_input}」，识别您为{matched_school['description']}"
        },
        "message": "匹配成功"
    }


# ==================== 接口 3（升级）：根据门派 + 任务执行技能 ====================

@app.post("/api/skill/run")
async def run_skill(request: SkillRunRequest):
    """
    根据用户所属门派和任务描述，自动检索、评分、排序，返回最优技能执行结果
    """
    school_id = request.school_id
    user_task = request.user_task.strip()

    if not user_task:
        raise HTTPException(status_code=400, detail="user_task 不能为空")

    # 检查门派是否存在
    school = next((s for s in SCHOOLS_DATA if s["id"] == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail=f"门派 ID {school_id} 不存在")

    # 智能匹配最佳技能
    best_skill = find_best_skill(school_id, user_task)

    if not best_skill:
        raise HTTPException(status_code=404, detail=f"门派 {school['name_zh']} 暂无可用技能")

    # 增加调用次数
    increment_skill_call_count(best_skill["skill_id"])

    # 生成结果（使用配置文件中的response模板）
    response_template = best_skill.get("response", "")
    result = response_template.format(user_task=user_task)

    return {
        "success": True,
        "data": {
            "school_name": school["name_zh"],
            "skill_id": best_skill["skill_id"],
            "skill_name": best_skill["name_cn"],
            "skill_name_en": best_skill["name_en"],
            "description": best_skill["description"],
            "result": result
        },
        "message": "技能执行成功"
    }


# ==================== 接口 4（新增）：获取门派技能列表 ====================

@app.get("/api/schools/{school_id}/skills")
async def get_school_skills(
    school_id: int = Path(..., description="门派ID", ge=1)
):
    """
    获取指定门派下的所有技能列表
    包含技能信息、调用次数、优先级等
    """
    # 检查门派是否存在
    school = next((s for s in SCHOOLS_DATA if s["id"] == school_id), None)
    if not school:
        raise HTTPException(status_code=404, detail=f"门派 ID {school_id} 不存在")

    # 筛选该门派的所有技能
    school_skills = [s for s in SKILLS_CONFIG if s["school_id"] == school_id]

    # 构建返回数据
    skills_list = []
    for skill in school_skills:
        skill_id = skill["skill_id"]
        call_count = SKILLS_STATS.get(skill_id, 0)

        skills_list.append({
            "skill_id": skill_id,
            "name_cn": skill["name_cn"],
            "name_en": skill["name_en"],
            "description": skill["description"],
            "keywords": skill["keywords"],
            "priority": skill["priority"],
            "call_count": call_count
        })

    # 按优先级排序
    skills_list.sort(key=lambda x: x["priority"], reverse=True)

    return {
        "success": True,
        "data": {
            "school_id": school_id,
            "school_name_zh": school["name_zh"],
            "school_name_en": school["name_en"],
            "total_skills": len(skills_list),
            "skills": skills_list
        },
        "message": "获取技能列表成功"
    }


# ==================== 静态文件服务 ====================

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


# ==================== 根路由 ====================

@app.get("/")
async def root():
    """返回前端页面"""
    return FileResponse("static/index.html")


@app.get("/skill.md")
async def get_skill_doc():
    """返回 Agent 接入文档（Markdown 格式）"""
    md_path = "static/skill.md"
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        return PlainTextResponse(content, media_type="text/markdown; charset=utf-8")
    else:
        raise HTTPException(status_code=404, detail="文档不存在")


@app.get("/api")
async def api_info():
    """API 信息接口"""
    return {
        "message": "Martial World API",
        "version": "2.1.0",
        "description": "外部AI Agent通过本API调用平台功能",
        "new_features": [
            "智能技能评分与排序",
            "关键词相似度匹配",
            "重复技能检测与惩罚",
            "技能调用统计",
            "可扩展的技能配置系统"
        ],
        "endpoints": {
            "GET /api/schools": "获取所有门派列表",
            "POST /api/match-school": "根据自然语言匹配门派",
            "POST /api/skill/run": "执行指定门派的技能（智能匹配最优）",
            "GET /api/schools/{school_id}/skills": "获取指定门派的技能列表"
        }
    }


# ==================== 启动服务 ====================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Martial World API v2.1 正在启动...")
    print("📖 文档地址：http://localhost:8000/docs")
    print("🔗 根路由：http://localhost:8000")
    print("✨ 新功能：智能技能评分、重复检测、可扩展配置")
    uvicorn.run(app, host="0.0.0.0", port=8000)
