# AGENTS.md — AI Knowledge Base Assistant

## 1. Project Overview

An automated pipeline that collects trending content in AI/LLM/Agent fields from GitHub Trending and Hacker News, analyzes and structures the data via Chinese LLM, stores it as JSON, and distributes curated knowledge entries to multiple channels (Telegram, Feishu/Lark).

## 2. Technology Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Python 3.13 |
| AI Orchestration | OpenCode + Chinese LLM |
| Workflow Engine | LangGraph |
| Multi-Channel Distribution | OpenClaw (Telegram + Feishu bot) |

## 3. Coding Standards

- **Style Guide**: [PEP 8](https://peps.python.org/pep-0008/)
- **Naming Convention**: `snake_case` for variables, functions, and files
- **Docstrings**: [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) (Args/Returns/Raises)
- **Logging**: Use the `logging` module exclusively — **裸 `print()` calls are strictly forbidden**
- **Type Hints**: All public functions must have type annotations
- **Imports Order**: standard library → third-party → local modules, each group separated by a blank line

## 4. Project Structure

```
ai-knowledge-base/
├── .opencode/
│   ├── agents/         # Agent role definitions (Collector / Analyzer / Organizer)
│   ├── skills/         # OpenCode skill modules
│   ├── package.json
│   └── .gitignore
├── knowledge/
│   ├── raw/            # Raw crawled data (intermediate)
│   └── articles/       # Analyzed & structured final JSON articles
├── AGENTS.md
└── ...
```

## 5. Knowledge Entry JSON Schema

Each article/knowledge entry stored under `knowledge/articles/` MUST conform to the following schema:

```json
{
  "id": "uuid-v4-string",
  "title": "Article Title (original language or translated)",
  "source": "github-trending | hacker-news",
  "source_url": "https://original.url/article",
  "summary": "AI-generated summary in Chinese (2–5 sentences)",
  "tags": ["llm", "agent", "rag", "..."],
  "status": "draft | published | archived",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z",
  "channels": ["telegram", "feishu"]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | UUID v4 |
| `title` | `string` | yes | Article title |
| `source` | `string` | yes | Origin platform (`github-trending` or `hacker-news`) |
| `source_url` | `string` | yes | Direct URL to the source |
| `summary` | `string` | yes | AI-generated Chinese summary |
| `tags` | `string[]` | yes | Classification tags |
| `status` | `string` | yes | Workflow status: `draft`, `published`, or `archived` |
| `created_at` | `string` | yes | ISO 8601 creation timestamp |
| `updated_at` | `string` | yes | ISO 8601 last update timestamp |
| `channels` | `string[]` | yes | Target distribution channels |

## 6. Agent Roles Overview

| Role | Agent ID | Responsibility | Triggers |
|------|----------|----------------|----------|
| **Collector** | `collector` | Crawls GitHub Trending & Hacker News; saves raw data to `knowledge/raw/` | Scheduled (cron) or manual trigger |
| **Analyzer** | `analyzer` | Reads raw data, invokes Chinese LLM for summarization & tagging, produces structured JSON entry with `status: "draft"` | On new raw data ingested |
| **Organizer** | `organizer` | Curates drafts, approves (`status: "published"`), pushes to configured channels via OpenClaw, archives stale entries | On draft ready / scheduled cleanup |

### Workflow (LangGraph)

```
[Collector] → raw/*.json → [Analyzer] → articles/*.json (draft)
                                          → [Organizer] → published → Telegram / Feishu
```

## 7. Red Lines (Strictly Prohibited Operations)

1. **Never commit secrets, API keys, or tokens** — use environment variables (`.env`) that are git-ignored
2. **Never use bare `print()`** — always use `logging.getLogger(__name__)` for output
3. **Never modify files under `knowledge/raw/` or `knowledge/articles/` manually outside the agent pipeline** — all writes must go through the respective agent
4. **Never hardcode URLs, channel configs, or model names** — use a config module or environment variables
5. **Never push to `main` directly** — work on feature branches; PR review required
6. **Never delete or truncate `knowledge/articles/` entries** — only status transitions (draft → published → archived) are allowed; physical deletion is forbidden
7. **Never bypass the LangGraph workflow** — all data must flow through Collector → Analyzer → Organizer
