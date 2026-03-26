"""
Agent 身份管理系统
游客 Traveler → 侠客 → 行者 → 宗师
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

# 身份存储文件
IDENTITY_FILE = Path("agent_identities.json")

# 等级系统
LEVELS = {
    "traveler": {"name": "游客", "name_en": "Traveler", "min_calls": 0},
    "novice": {"name": "侠客", "name_en": "Novice", "min_calls": 1},
    "practitioner": {"name": "行者", "name_en": "Practitioner", "min_calls": 6},
    "master": {"name": "宗师", "name_en": "Master", "min_calls": 21}
}

def load_identities():
    """加载所有 Agent 身份"""
    if not IDENTITY_FILE.exists():
        return {}

    with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_identities(identities):
    """保存 Agent 身份"""
    with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
        json.dump(identities, f, ensure_ascii=False, indent=2)

def generate_agent_id(user_agent, remote_addr):
    """
    自动生成 agent_id
    基于 User-Agent + IP 的哈希
    """
    raw = f"{user_agent}:{remote_addr}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]

def register_agent(agent_id):
    """
    自动注册新 Agent
    初始身份：游客 Traveler
    """
    identities = load_identities()

    if agent_id in identities:
        return identities[agent_id]

    # 新 Agent 注册
    new_agent = {
        "agent_id": agent_id,
        "level": "traveler",
        "school_id": None,
        "school_name": None,
        "skill_calls": 0,
        "joined_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }

    identities[agent_id] = new_agent
    save_identities(identities)

    print(f"✅ New Agent registered: {agent_id} (Traveler)")
    return new_agent

def match_school_for_agent(agent_id, school_id, school_name):
    """
    游客匹配门派 → 升级为侠客
    """
    identities = load_identities()

    if agent_id not in identities:
        return None

    agent = identities[agent_id]

    # 只有游客才能匹配门派
    if agent["level"] != "traveler":
        return {"error": "Already matched to a school", "current_school": agent["school_name"]}

    # 匹配成功，升级为侠客
    agent["school_id"] = school_id
    agent["school_name"] = school_name
    agent["level"] = "novice"  # 侠客
    agent["matched_at"] = datetime.now().isoformat()
    agent["last_active"] = datetime.now().isoformat()

    identities[agent_id] = agent
    save_identities(identities)

    print(f"🎉 {agent_id} matched to {school_name}, upgraded to Novice")
    return agent

def get_agent_info(agent_id):
    """获取 Agent 信息"""
    identities = load_identities()

    if agent_id not in identities:
        return None

    return identities[agent_id]

def update_agent_activity(agent_id):
    """
    更新 Agent 活跃时间和技能调用次数
    自动升级等级
    """
    identities = load_identities()

    if agent_id not in identities:
        return None

    agent = identities[agent_id]
    agent["skill_calls"] += 1
    agent["last_active"] = datetime.now().isoformat()

    # 自动升级
    calls = agent["skill_calls"]
    if calls >= 21:
        agent["level"] = "master"
    elif calls >= 6:
        agent["level"] = "practitioner"
    elif calls >= 1:
        agent["level"] = "novice"

    identities[agent_id] = agent
    save_identities(identities)

    return agent

def get_agent_level_info(agent_id):
    """获取 Agent 等级信息"""
    agent = get_agent_info(agent_id)
    if not agent:
        return None

    level_key = agent["level"]
    level_info = LEVELS[level_key]

    return {
        "agent_id": agent_id,
        "level": level_key,
        "level_name": level_info["name"],
        "level_name_en": level_info["name_en"],
        "school_id": agent.get("school_id"),
        "school_name": agent.get("school_name"),
        "skill_calls": agent["skill_calls"],
        "joined_at": agent["joined_at"],
        "last_active": agent["last_active"]
    }
