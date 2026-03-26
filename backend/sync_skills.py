#!/usr/bin/env python3
"""
Sync skills from open source repositories to Martial World
All skills are MIT Licensed - attribution required
"""

import json
import urllib.request

# Skill source mapping
SKILL_SOURCES = {
    "s301": {
        "name_en": "Growth Strategy",
        "name_cn": "增长策略诀",
        "description": "Design viral referral programs that leverage customers for exponential growth",
        "keywords": ["growth", "referral", "viral", "acquisition", "CAC"],
        "source_repo": "coreyhaines31/marketingskills",
        "source_skill": "referral-program",
        "license": "MIT",
        "attribution": "Corey Haines (coreyhaines31)"
    },
    "s302": {
        "name_en": "Content Strategy",
        "name_cn": "运营规划术",
        "description": "Plan searchable and shareable content that drives traffic and builds authority",
        "keywords": ["content", "SEO", "blog", "editorial", "strategy"],
        "source_repo": "coreyhaines31/marketingskills",
        "source_skill": "content-strategy",
        "license": "MIT",
        "attribution": "Corey Haines (coreyhaines31)"
    },
    "s303": {
        "name_en": "SEO Audit",
        "name_cn": "SEO 审计术",
        "description": "Comprehensive SEO audit framework with actionable fixes",
        "keywords": ["SEO", "audit", "search", "ranking", "optimization"],
        "source_repo": "coreyhaines31/marketingskills",
        "source_skill": "seo-audit",
        "license": "MIT",
        "attribution": "Corey Haines (coreyhaines31)"
    }
}

def fetch_skill_content(repo, skill_name):
    """Fetch skill content from GitHub"""
    url = f"https://raw.githubusercontent.com/{repo}/main/skills/{skill_name}/SKILL.md"
    print(f"Fetching: {url}")

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {skill_name}: {e}")
        return None

def sync_all_skills():
    """Sync all skills from sources"""

    # Load existing config
    with open("skills_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    skills = config["skills"]

    # Update skills with fetched content
    for skill_id, meta in SKILL_SOURCES.items():
        print(f"\n📥 Syncing {skill_id} - {meta['name_en']}...")

        content = fetch_skill_content(meta["source_repo"], meta["source_skill"])

        if not content:
            print(f"⚠️  Skipped {skill_id} (fetch failed)")
            continue

        # Find and update skill in config
        for skill in skills:
            if skill["skill_id"] == skill_id:
                # Update skill response with fetched content
                skill["response"] = f"# {meta['name_en']}\n\n{content}\n\n---\n*Source: {meta['source_repo']} | License: {meta['license']} | Attribution: {meta['attribution']}*"
                skill["description"] = meta["description"]
                skill["keywords"] = meta["keywords"]
                print(f"✅ Updated {skill_id}")
                break

    # Save updated config
    with open("skills_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print("\n🎉 All skills synced successfully!")
    print("📝 Updated: skills_config.json")

if __name__ == "__main__":
    sync_all_skills()
