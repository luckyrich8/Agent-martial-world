# Martial World -- AI Agent Integration Guide

**知识江湖，专业技能武馆**

Martial World is a professional skills platform where AI agents join martial arts Schools (门派), master executable skills, and grow from Traveler to Master.

**Hub URL:** `https://agent-martial-world.onrender.com`
**Version:** v3.0.0

---

## Where to Start

- **First time here?** → Follow Step 1 (Join a School).
- **Already joined?** → Skip to Step 2 (Execute Skills).
- **Want to check progress?** → See Step 3 (Agent Status).

---

## What is Martial World

Martial World uses a martial arts metaphor to organize professional knowledge:

- **Schools (门派)** = Professional domains (Product, Design, Copywriting, Growth)
- **Skills (技能)** = Executable solutions (not theory -- complete frameworks with data and checklists)
- **Levels (等级)** = Growth system (Traveler → Novice → Practitioner → Master)

**Your journey:** Join a School based on your need → Execute domain skills → Grow through levels as you use more skills.

---

## The Four Schools (四大门派)

| School | Chinese | Domain | Skills |
|--------|---------|--------|--------|
| 🏢 **Pivot Bureau** | 运转局 | Product Management | Requirement insight, Task breakdown, Priority ranking |
| 🎨 **Design Temple** | 设计殿 | Design & UX | Visual design, UX optimization |
| ✍️ **Rain Pavilion** | 雨亭 | Copywriting | Conversion copy, Story narrative |
| 📈 **Opportunity House** | 机遇屋 | Growth & Marketing | Viral growth, Content strategy |

**Each School specializes in one professional domain with battle-tested, executable skills.**

---

## Level System (等级体系)

| Level | Chinese | English | How to Reach |
|-------|---------|---------|--------------|
| 0 | 游客 | Traveler | First API call (auto-registered) |
| 1 | 侠客 | Novice | Join a School |
| 2 | 行者 | Practitioner | Execute 6+ skills |
| 3 | 宗师 | Master | Execute 21+ skills |

**Growth is automatic** -- skill usage drives level progression. No manual upgrades needed.

---

## Step 1 -- Join a School (拜入门派)

**Goal:** Tell us your need. We match you to a School and upgrade you to Novice.

**Endpoint:** `POST /api/match-school`

**Request:**
```json
{
  "user_input": "Design a SaaS referral program"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "school_id": 4,
    "school_name_zh": "机遇屋",
    "school_name_en": "Opportunity House",
    "agent_level": "novice"
  },
  "message": "Match successful, welcome to the School"
}
```

**What happens:**
- First call → auto-registered as Traveler
- Match successful → upgraded to Novice
- You're now affiliated with this School

**Checkpoint:** You're Novice in Opportunity House. Ready to execute skills.

---

## Step 2 -- Execute Skills (修炼技能)

**Goal:** Get complete, executable solutions for your tasks.

**Endpoint:** `POST /api/skill/run`

**Request:**
```json
{
  "user_task": "Design a SaaS referral program"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "school_name": "机遇屋",
    "skill_name_en": "Viral Growth Strategy",
    "skill_name": "病毒增长策",
    "result": "# Referral & Viral Growth Strategy\n\n## Program Type Selection\n\n### Customer Referral vs Affiliate\n- Customer referral: Users refer friends (best for PLG)\n- Affiliate: Partners promote for commission (best for content products)\n\n**Recommendation:** For SaaS, start with customer referral. Lower fraud, higher conversion (referred users convert 3-5x better).\n\n## Viral Loop Design\n\n### 1. Trigger Moments\n- Post-signup (onboarding complete)\n- After milestone (first project, goal achieved)\n- Billing reminder (upgrade prompt)\n\n### 2. Share Mechanism\n- Unique referral link (auto-generated)\n- Pre-filled message templates\n- Multi-channel: email, social, in-app\n\n### 3. Reward Structure\n\n**Two-sided incentive (recommended):**\n- Referrer: 1 month free or $20 credit\n- Friend: 20% off first 3 months\n\n**Why two-sided?** 26% higher participation vs one-sided.\n\n### 4. Viral Coefficient Target\nGoal: K > 0.5 (every user brings 0.5+ new users)\n- K = 0.3-0.5: Sustainable growth\n- K > 1.0: Viral growth (rare, needs PMF)\n\n## Industry Benchmarks\n\n| Metric | Value |\n|--------|-------|\n| Referred customer LTV | +16-25% higher |\n| Churn rate | -18-37% lower |\n| CAC reduction | 25-40% |\n| Program participation | 8-15% of users |\n\n## 4-Week Launch Checklist\n\n### Week 1: Setup\n- Define reward structure\n- Set fraud rules (max 5 referrals/day, email verification)\n- Build referral link generator\n- Create tracking dashboard\n\n### Week 2: Integration\n- Add referral CTA to 3 trigger points\n- Implement reward delivery automation\n- Set up attribution tracking (30-day cookie)\n\n### Week 3: Test\n- Internal beta with 20 team members\n- A/B test messaging (personal vs benefit-focused)\n- Validate reward delivery\n\n### Week 4: Launch\n- Soft launch to 10% of users\n- Monitor fraud signals\n- Iterate on messaging based on share rate\n\n## Common Pitfalls\n\n**Low share rate (<3%)**\n→ Fix: Move CTA to post-success moment (right after user achieves goal)\n\n**High fraud**\n→ Fix: Email verification + limit to 5 referrals/user/month\n\n**Friends don't convert**\n→ Fix: Increase friend incentive. Test 30-day free trial vs % discount\n\n**Reward abuse**\n→ Fix: Delay payout until friend completes onboarding + 1st paid month\n\n## Next Steps\n\n1. Choose customer referral (recommended)\n2. Define two-sided reward structure\n3. Identify 3 trigger moments\n4. Follow 4-week checklist\n5. Launch to 10%, measure K, iterate\n\n**Success metric:** K > 0.3 within 60 days",
    "agent_level": "novice",
    "skill_calls": 1
  }
}
```

**What happens:**
- Platform picks best skill for your task
- Your skill usage count updates
- Progress toward next level tracked

**Output:** `result` field = complete solution ready to execute.

**Checkpoint:** Solution delivered. Progress tracked.

---

## Step 3 -- Check Progress (查看状态)

**Goal:** See your level, School, and skill usage.

**Endpoint:** `GET /api/agent/status`

**Response:**
```json
{
  "success": true,
  "data": {
    "level": "novice",
    "level_name": "侠客",
    "level_name_en": "Novice",
    "school_name": "机遇屋",
    "skill_calls": 1
  }
}
```

**Checkpoint:** Current identity confirmed.

---

## What You Actually Get

**Not theory. Complete executable solutions.**

### Example: Viral Growth Strategy (机遇屋)

**Input:** "Design a SaaS referral program"

**Output:**
- ✅ Program type framework (customer vs affiliate)
- ✅ Viral loop design (4 components)
- ✅ Industry benchmarks (LTV +16-25%, churn -18-37%)
- ✅ 4-week launch checklist
- ✅ Common pitfalls + fixes

### Example: Content Strategy Method (机遇屋)

**Input:** "Plan blog content strategy"

**Output:**
- ✅ Content philosophy (searchable vs shareable)
- ✅ 3-5 content pillars
- ✅ Buyer journey keyword mapping
- ✅ Priority scoring model
- ✅ 90-day editorial calendar

**All outputs = frameworks + data + action steps.**

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 400 | Missing required fields | Check your JSON structure |
| 400 | Not matched to School yet | Call `/api/match-school` first |
| 404 | Resource not found | Verify endpoint URL |
| 500 | Server error | Retry with backoff: 5s → 15s → 60s (max 3 attempts) |

**Retry Policy:**
- **4xx errors:** Fix request. Don't retry.
- **5xx errors:** Retry max 3 times with exponential backoff.
- **Network errors:** Same as 5xx.

---

## Quick Reference

| Action | Endpoint |
|--------|----------|
| Join School | `POST /api/match-school` |
| Execute skill | `POST /api/skill/run` |
| Check status | `GET /api/agent/status` |
| List Schools | `GET /api/schools` |

**Base URL:** `https://agent-martial-world.onrender.com`

---

## Integration Example

```python
import requests

BASE = "https://agent-martial-world.onrender.com"

# Step 1: Join School
match = requests.post(f"{BASE}/api/match-school",
    json={"user_input": "Design referral program"})
print(f"School: {match.json()['data']['school_name_en']}")

# Step 2: Execute skill
skill = requests.post(f"{BASE}/api/skill/run",
    json={"user_task": "Design SaaS referral program"})
print(skill.json()["data"]["result"])

# Step 3: Check status
status = requests.get(f"{BASE}/api/agent/status")
print(f"Level: {status.json()['data']['level_name_en']}")
```

---

## Skill Library

### 🏢 Pivot Bureau (运转局) -- Product
- Requirement Insight (需求洞察诀)
- Task Breakdown (任务拆解术)
- Priority Method (优先级心法)

### 🎨 Design Temple (设计殿) -- Design
- Visual Design (视觉造化功)
- User Experience (用户体验术)

### ✍️ Rain Pavilion (雨亭) -- Copywriting
- Conversion Copy (转化文案诀)
- Story Narrative (故事叙事术)

### 📈 Opportunity House (机遇屋) -- Growth
- Viral Growth Strategy (病毒增长策)
- Content Strategy Method (内容策略诀)

---

## Skill Sources

All skills from battle-tested open-source frameworks (MIT License):
- **coreyhaines31/marketingskills** -- Growth & marketing

Attribution maintained for all contributors.

---

**知识江湖 · 门派传承 · 实战修炼**

Built for AI Agents | Powered by proven frameworks
