---
name: douyin-tracker
description: Track and analyze trending content on Douyin (TikTok China). Use this skill when users ask about Douyin hot lists, trending videos, popular accounts, viral events, or content performance metrics. Supports queries by keyword, account name, category (food, pets, tech, etc.), time range, or engagement data (likes, views). Make sure to use this skill whenever users mention Douyin trending content, hot rankings, viral videos, account analytics, content categories, daily/weekly charts, or ask questions like "what's trending on Douyin", "show me top liked videos", "analyze popular food content", or "track account dynamics".
compatibility: |
  newrank
    - ai_content_rank_dy
    - daily_rank_500_dy
    - daily_rank_dy
    - hot_rank_dy
    - seven_days_grank_dy
---

# Douyin Tracker

Track and analyze trending content, hot events, and account dynamics on Douyin platform.

## MCP Access: Use mcporter

**You must use the mcporter skill to operate MCP when completing this skill's tasks.** Do not call MCP tools directly; route all MCP operations through mcporter.

- **Config**: The global MCP config is in `~/.openclaw/workspace/config/mcporter.json`. Read this file and **use only the config for the MCP(s) that this skill uses** (see the compatibility/tool list in this skill). Do not use other MCPs from the config—only those declared for this skill.
- **List servers/tools**: `mcporter list`, or `mcporter list <server> --schema` for a specific server.
- **Call a tool**: `mcporter call <server.tool> key=value` (e.g. `mcporter call newrank.hot_rank_dy date=2024-03-10`).
- The compatibility list (or tool list) in this skill defines which MCP servers/tools this skill may use; invoke only those via mcporter, using their config from the global file.

---

## Workflow

### Step 1: Understand User Intent

First, analyze what the user is asking for:

- **Hot events tracking**: Looking for trending news, viral events, hot topics
- **Content ranking**: Wants to see top-performing videos by likes, engagement, or growth
- **Category-specific search**: Interested in specific content categories (food, pets, tech, fashion, etc.)
- **Account tracking**: Checking specific account dynamics, recent posts, fan reactions
- **Time-based query**: Looking for content from specific time periods (yesterday, last 7 days, etc.)
- **Data analysis**: Wants to understand performance metrics, trends, and patterns

**Why this matters**: Understanding the user's true intent helps you choose the right tools and query parameters, ensuring you return relevant and actionable insights rather than generic data dumps.

### Step 2: Optimize Query

Transform the user's natural language question into an effective search query:

- Extract key terms (account names, keywords, categories, time references)
- Identify implicit requirements (e.g., "昨天" means you need daily rankings from yesterday)
- Normalize category names to match available options
- Clarify ambiguous requests by inferring from context

**Available categories**: 全部, 剧情演绎, 财经, 二次元, 健身, 居家, 科技, 科普, 旅游, 美食, 萌宠, 明星八卦, 汽车, 亲子, 人文社科, 三农, 时尚, 游戏, 随拍, 体育, 舞蹈, 校园教育, 休闲, 影视, 音乐, 颜值, 医疗健康, 综艺, 个人管理

### Step 3: Fetch Data via mcporter

Based on the user's intent, call the appropriate tools through mcporter:

#### For hot events and news:
```bash
mcporter call newrank.hot_rank_dy date=YYYY-MM-DD
```
Use this when users ask about trending events, hot topics, or viral news on Douyin.

#### For top-performing content (by likes):
```bash
mcporter call newrank.daily_rank_500_dy date=YYYY-MM-DD category=美食
```
Use this for "top 500 by likes" queries. Supports all content categories.

#### For daily growth rankings:
```bash
mcporter call newrank.daily_rank_dy date=YYYY-MM-DD category=科技
```
Use this when users want to see which content is gaining traction rapidly within a single day.

#### For 7-day growth rankings:
```bash
mcporter call newrank.seven_days_grank_dy date=YYYY-MM-DD category=萌宠
```
Use this when users ask about weekly trends or content that's been consistently growing over the past week.

#### For AI-related content:
```bash
mcporter call newrank.ai_content_rank_dy date=YYYY-MM-DD
```
Use this specifically when users ask about AI-related trending content on Douyin.

**Date format**: Always use `YYYY-MM-DD` format. For relative time references like "yesterday" or "last week", calculate the actual date first.

**Why mcporter**: Using mcporter ensures consistent authentication, error handling, and proper parameter formatting when accessing the newrank MCP tools.

### Step 4: Analyze and Process Data

After fetching data, apply the user's specific requirements:

1. **Extract ranking data**: Identify position, title, account name, engagement metrics
2. **Filter by criteria**: Apply filters for category, time range, or performance thresholds
3. **Sort and prioritize**: Arrange results by likes, views, growth rate, or relevance
4. **Identify patterns**: Look for common themes, trending topics, or standout performers
5. **Account-specific analysis**: If querying by account, focus on that account's content and fan engagement
6. **Cross-reference events**: For hot events, use search to understand the full story and development timeline

**Why analysis matters**: Raw data isn't actionable. By extracting insights, identifying trends, and contextualizing metrics, you help users make informed content and marketing decisions.

### Step 5: Format Output

Present results in a rich Markdown format:

#### Structure:
```markdown
# [Main Title in Large Bold]
## [Subtitle in Bold]

### Overview
[Brief summary of findings]

### Top Rankings
[Use tables for structured data]

| Rank | Title | Account | Likes | Link |
|------|-------|---------|-------|------|
| 1 | ... | ... | ... | [原文链接](url) |

### Key Insights
- **Pattern 1**: [Observation with supporting data]
- **Pattern 2**: [Trend analysis]

### Featured Content
[Include images where available]
![Content thumbnail](image_url)

**Title**: [Video title]  
**Account**: [Account name]  
**Performance**: [Key metrics]  
**Link**: [原文链接](url)

### Recommendations
[Actionable suggestions based on data]
```

#### Requirements:
- **Images**: Include thumbnails or cover images when available
- **Links**: Always provide original content links with text "原文链接"
- **Tables**: Use for ranking data, metrics comparison
- **Bold headers**: Make titles prominent and scannable
- **Data visualization**: Present numbers clearly (use thousands separators, percentages)
- **Context**: Don't just list data—explain what it means

**Visual hierarchy**: Use larger headers, bold text, and clear sections to make the report easy to scan. Users should be able to quickly find what they're looking for.

---

## Common Query Patterns

### "Show me yesterday's top 10 videos"
- Use `daily_rank_500_dy` or `daily_rank_dy` with yesterday's date
- Extract top 10 entries
- Present with ranking, engagement metrics, and links

### "What's trending in food content this week?"
- Use `seven_days_grank_dy` with `category=美食`
- Analyze common themes (recipe types, presentation styles, etc.)
- Highlight standout performers

### "Track [account name]'s recent activity"
- Search for the account in relevant rankings
- List recent posts with performance data
- Analyze fan engagement patterns (if comment data available)

### "What AI content went viral yesterday?"
- Use `ai_content_rank_dy` with yesterday's date
- Focus on top performers
- Explain why they resonated (if context available)

### "Hot events on Douyin right now"
- Use `hot_rank_dy` with today's or latest date
- Provide event context and development timeline
- Link to related content if available

---

## Important Notes

- **Date handling**: Always calculate actual dates for relative time references (today, yesterday, last week)
- **Category matching**: Use exact category names from the available list
- **Link preservation**: Never omit original content links—they're essential for verification
- **Data freshness**: Note the data date in your output so users understand the timeframe
- **Empty results**: If a query returns no results, suggest alternative queries or categories
- **Rate limits**: If multiple queries are needed, execute them sequentially through mcporter
- **Image quality**: When embedding images, ensure they're properly sized and relevant

**User experience**: Your goal is to deliver insights, not just data. Always connect the numbers to meaningful takeaways that users can act on.
