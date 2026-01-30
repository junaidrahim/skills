---
name: exa
description: Deep web research using Exa AI semantic search API.
---

# Exa Web Search

Exa (exa.ai) provides embeddings-based semantic search for finding exactly what you need on the web.

## Setup

**API Key required.** Set in environment:
```bash
export EXA_API_KEY="your-key-here"
```

Get your key at: https://dashboard.exa.ai/api-keys

## Core Functions

### Search
Find webpages using semantic search:
```bash
curl -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best practices for distributed systems",
    "numResults": 10,
    "type": "auto"
  }'
```

**Search types:**
- `auto` — Let Exa choose (recommended)
- `keyword` — Traditional keyword search
- `neural` — Pure embeddings-based

### Search + Contents
Get search results with full page content:
```bash
curl -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "apache iceberg architecture deep dive",
    "numResults": 5,
    "contents": {
      "text": true
    }
  }'
```

### Find Similar
Find pages similar to a given URL:
```bash
curl -X POST "https://api.exa.ai/findSimilar" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/great-article",
    "numResults": 10
  }'
```

### Get Contents
Get clean content from specific URLs:
```bash
curl -X POST "https://api.exa.ai/contents" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["result-id-1", "result-id-2"],
    "text": true
  }'
```

### Answer (Direct Answers)
Get a direct answer with citations:
```bash
curl -X POST "https://api.exa.ai/answer" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the CAP theorem?",
    "text": true
  }'
```

## Filters

Add to any search request:
```json
{
  "query": "...",
  "includeDomains": ["arxiv.org", "github.com"],
  "excludeDomains": ["pinterest.com"],
  "startPublishedDate": "2024-01-01",
  "category": "research paper"
}
```

**Categories:** `company`, `research paper`, `news`, `pdf`, `github`, `tweet`, `personal site`, `linkedin profile`

## Deep Research Workflow

1. **Broad search** — Get landscape of a topic
2. **Find similar** — Expand from best results
3. **Get contents** — Pull full text for analysis
4. **Answer** — Get specific answers with citations
5. **Synthesize** — Combine into structured notes

## Tips

- Use natural language queries (Exa understands intent)
- `numResults: 5-10` for deep dives, `3-5` for quick lookups
- Use `includeDomains` for authoritative sources
- `startPublishedDate` for recent content only
