# Martial World - Agent Integration Guide

## 📖 What is Martial World?

**Martial World** is an AI-powered skill platform that matches professionals with specialized expertise frameworks. Tell us your role or goal, and we'll match you to a "school" (domain expertise) with ready-to-use skills.

Think of it as a **knowledge martial arts academy** - each school represents a professional domain (Product, Design, Content, Growth), and each skill is a proven framework you can invoke instantly.

---

## 🔑 Core Concepts

### 🏛️ Schools (门派)

Four professional domains, each with specialized skills:

| School | English Name | Role | Skills |
|--------|-------------|------|---------|
| 🏢 运转局 | Pivot Bureau | Product Manager | 5 skills |
| 🎨 设计殿 | Design Temple | Designer | 2 skills |
| ✍️ 雨亭 | Rain Pavilion | Copywriter | 2 skills |
| 📈 机遇屋 | Opportunity House | Growth/Operations | 2 skills |

### ⚡ Skills (技能)

Each skill is a **ready-to-use framework** (not generic advice):
- **Growth Strategy**: Viral referral program design with industry benchmarks
- **Content Strategy**: SEO-driven content planning with prioritization scoring
- **UX Design**: User flow optimization with concrete improvements

Skills return **actionable frameworks**, not philosophies.

### 🥋 User Levels (等级)

As you use skills, you progress through ranks:
- 🌱 **Wanderer** (初入江湖): 0-5 skill invocations
- ⚔️ **Practitioner** (小有所成): 6-20 invocations
- 🏆 **Master** (登峰造极): 21+ invocations

---

## 🎮 How to Play

### Step 1: Tell Us Your Role or Goal

Simply describe what you do or want to accomplish:
- "I'm building a SaaS product"
- "I need to grow user acquisition"
- "I want to improve my landing page UX"

### Step 2: Get Matched to a School

The API automatically matches you to the best school based on your input:
- Product/startup keywords → **Pivot Bureau** (Product school)
- Design/UX keywords → **Design Temple**
- Content/copywriting keywords → **Rain Pavilion**
- Growth/marketing keywords → **Opportunity House**

### Step 3: Invoke Skills

Once matched, invoke specific skills to get expert frameworks:
- Each skill returns a **structured framework** (not generic tips)
- Frameworks include industry data, checklists, and next steps
- All content is **actionable** and **production-ready**

---

## 🚀 Quick Start

### For AI Agents

**Step 1: Match User to School**

```bash
POST https://agent-martial-world.onrender.com/api/match-school
Content-Type: application/json

{
  "user_input": "I want to grow my SaaS product"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "school_id": 4,
    "school_name": "Opportunity House",
    "description": "Growth and operations expertise",
    "role": "growth_manager"
  }
}
```

**Step 2: Invoke a Skill**

```bash
POST https://agent-martial-world.onrender.com/api/skill/run
Content-Type: application/json

{
  "school_id": 4,
  "skill_id": "s301",
  "user_task": "Design a referral program for my product"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "skill_name_en": "Growth Strategy",
    "result": "# Referral & Viral Growth Strategy\n\n## Program Type Selection...\n[Full framework with benchmarks, checklists, metrics]"
  }
}
```

---

## 🏛️ The Four Schools

### 🏢 Pivot Bureau (运转局) - Product Thinking
**For**: Product managers, founders, project managers

**Skills**:
- Insight Divination: Discover real user needs
- Task Disassembly: Break down complex projects
- Priority Methodology: Decide what to build first

---

### 🎨 Design Temple (设计殿) - Design Mastery
**For**: UI/UX designers, visual designers

**Skills**:
- Visual Design: Beautiful and functional interfaces
- User Experience: Optimize user flows and interactions

---

### ✍️ Rain Pavilion (雨亭) - Content Craft
**For**: Copywriters, content creators, marketers

**Skills**:
- Copywriting Creation: Write compelling copy that converts
- Story Narrative: Craft engaging stories that resonate

---

### 📈 Opportunity House (机遇屋) - Growth Engines
**For**: Growth marketers, operations managers

**Skills**:
- **Growth Strategy**: Design viral referral programs (industry data: 16-25% higher LTV, 18-37% lower churn)
- **Content Strategy**: Plan SEO-driven content with prioritization frameworks

---

## 📡 API Reference

### Base URL
```
https://agent-martial-world.onrender.com
```

### Endpoints

#### 1. Match School
`POST /api/match-school`

**Request:**
```json
{
  "user_input": "Natural language description of role/goal"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "school_id": 1,
    "school_name": "Pivot Bureau",
    "description": "Product thinking and strategic planning",
    "role": "product_manager"
  }
}
```

#### 2. Get All Schools
`GET /api/schools`

Returns list of all 4 schools with metadata.

#### 3. Run Skill
`POST /api/skill/run`

**Request:**
```json
{
  "school_id": 4,
  "skill_id": "s301",
  "user_task": "Describe what you want to accomplish"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "school_name": "Opportunity House",
    "skill_id": "s301",
    "skill_name_en": "Growth Strategy",
    "description": "Design viral referral programs",
    "result": "[Full framework content]"
  }
}
```

---

## 💡 Integration Tips

### For Agent Developers

**1. Let users speak naturally**
- Don't ask "Which school do you want?" - just ask "What do you want to do?"
- The matching API handles role detection automatically

**2. Present frameworks cleanly**
- Skills return markdown-formatted frameworks
- Render them with proper formatting for best UX

**3. Progressive disclosure**
- Start with school matching
- Show available skills after match
- Invoke skills on demand

**4. Track user progression**
- Use the level system to gamify engagement
- Celebrate milestones (first skill use, 10th use, etc.)

---

## 🔗 Resources

- **Live Platform**: https://agent-martial-world.vercel.app
- **API Base URL**: https://agent-martial-world.onrender.com
- **GitHub**: https://github.com/luckyrich8/Agent-martial-world

---

**Built for AI Agents** | Powered by proven professional frameworks
