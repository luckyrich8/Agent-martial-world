"""
动态技能加载器 - 实时从 GitHub 拉取最新技能内容
类似 skills.sh 的工作方式
"""

import json
import urllib.request
from functools import lru_cache
from datetime import datetime

# 内存缓存（10 分钟过期）
CACHE = {}
CACHE_DURATION = 600  # 秒

def load_skills_registry():
    """加载技能注册表（只有元数据，没有内容）"""
    with open("skills_registry.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_skill_from_github(repo, skill_name):
    """从 GitHub 实时拉取技能内容"""
    url = f"https://raw.githubusercontent.com/{repo}/main/skills/{skill_name}/SKILL.md"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')
            return content
    except Exception as e:
        print(f"Error fetching {skill_name}: {e}")
        return None

def get_skill_content(skill_id):
    """
    获取技能内容（带缓存）
    - 优先从缓存读取
    - 缓存过期则重新从 GitHub 拉取
    """

    # 检查缓存
    if skill_id in CACHE:
        cached_data, cached_time = CACHE[skill_id]
        if (datetime.now() - cached_time).seconds < CACHE_DURATION:
            print(f"✅ Using cached content for {skill_id}")
            return cached_data

    # 从注册表获取技能信息
    registry = load_skills_registry()
    skill = next((s for s in registry["skills"] if s["skill_id"] == skill_id), None)

    if not skill:
        return None

    # 从 GitHub 拉取最新内容
    print(f"📥 Fetching latest content for {skill_id} from GitHub...")
    content = fetch_skill_from_github(skill["source_repo"], skill["source_skill"])

    if content:
        # 添加归属信息
        full_content = f"{content}\n\n---\n*Source: {skill['source_repo']} | License: MIT*"

        # 更新缓存
        CACHE[skill_id] = (full_content, datetime.now())

        return full_content

    return None

def get_skill_metadata(skill_id):
    """获取技能元数据（不含内容）"""
    registry = load_skills_registry()
    return next((s for s in registry["skills"] if s["skill_id"] == skill_id), None)

def list_all_skills():
    """列出所有可用技能"""
    registry = load_skills_registry()
    return registry["skills"]
