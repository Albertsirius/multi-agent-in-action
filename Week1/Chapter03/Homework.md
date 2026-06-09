# Week1 - Chapter03

---

## 任务1
### Collector Agent
Collactor提示词：
```markdown
Create .opencode/agents/collector.md, defind a Knowledge Collector Agent

Requirements:
- Role: The collection agent collects data technology trends from GitHub Trending and Hacker News
- Allowed: Read, Grep, Glob, WebFetch (view only, search only, no writing)
- Prohibited: Write, Edit, Bash (and explain why they are prohibited)
- Responsibilities: search and collect, extract titles/links/popularities/summaries, perform initial screening, and sort by popularity
- Output format: JSON array, each entry containing title, URL, source, popularity, and summary
- Quality self-inspection checklist: Items >= 15, complete information, no fabrication
```

Analyzer和Organizer提示词：
```markdown
Referring to the format of .opencode/agents/collector.md, please creat two more Agent definition markdown file:

1. .opencode/agents/analyzer.md - Analysis Agent
    - Permissions are the same as the collector (allowed: Read/Grep/Glob/WebFetch, prohibited: Write/Edit/Bash)
    - Responsibilities: read data from knowledge/raw, write a summary, highlight key points, assign a score (1-10), and give tags
    - Scoring criteria: 9-10 (Changing the landscape), 7-8 (Directly helpful), 5-6 (Worth learning about), 1-4 (Can be ignored)

2. .opencode/agents/organizer.md - Organize Agent
    - Allowed: Read/Grep/Glob/Write/Edit
    - Prohibited: WebFetch/Bash
    - Responsibilities: deduplication check, format as standard JSON, categorize and save in knowledge/articles/
    - File name format: {data}-{source}-{slug}.json

```


## 任务二
### `@mention`和`Task`的区别
通过AI问答：

`@mention` 用于在当前对话中快速调用特定的文件或子代理。

`Task` 则是指的是主代理（Primary Agent）为了完成复杂的模块化工作，委派给专门的子代理（Sub-agent）去独立执行的具体目。

若你想的是ask，使用`@mention`；若想assign，则使用`@assgin`

### 执行结果

![截图](screen_dump.png)



