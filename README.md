# AI News Researcher Agent

Multi-agent system that automatically collates **AI-focused news** from various sources and compiles them into digestible reports. Exclusively focused on Artificial Intelligence, Machine Learning, AI tools, and AI research news.

## Features

- **AI News Exclusive**: Only collects and summarizes AI, ML, and AI research news
- **Source Diversity**: Collects from ALL sources (5 per source) to prevent first-source bias
- **Smart Deduplication**: Automatically removes duplicate articles using local algorithms (no API cost)
- **Intelligent Ranking**: AI-powered selection of most newsworthy articles when over limit
- **Multi-Agent Architecture**: Specialized AI news agents (Fetcher, Summarizer, Compiler) working together
- **Curated AI Sources**: Pre-configured AI news feeds from top tech publications
- **Intelligent Summarization**: GPT-4 powered analysis with key AI insights and implications
- **Built-in Safeguards**: Time limits (5 min max), date filtering (7 days max), volume controls
- **Cost Effective**: Optimized to minimize API calls while maximizing quality
- **Configurable**: Customize AI sources, article limits, summary style, and timeouts

## Quick Start

**Prerequisites**: Python 3.8+, OpenAI API key ([get one here](https://platform.openai.com/api-keys))

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
# Windows PowerShell:
Set-Content -Path .env -Value "OPENAI_API_KEY=sk-your-key-here" -Encoding UTF8 -NoNewline

# Mac/Linux:
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Or manually: Create .env file and add: OPENAI_API_KEY=sk-your-key-here

# Run
python main.py
```

## Usage

```bash
# Default mode (fetches latest AI news)
python main.py

# Interactive mode (customize AI news settings)
python main.py --interactive
```

Output saved to `ai_news_digests/` directory

## Configuration

Edit `config.py` for all settings:

```python
# AI News Sources - Add your preferred AI RSS feeds here
NEWS_SOURCES = {
    "rss_feeds": [
        "https://www.artificialintelligence-news.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        # Add more AI news sources...
    ],
    "categories": ["artificial-intelligence", "machine-learning", "ai-tools", "ai-research"]
}

# Limits
MAX_ARTICLES = 10                      # AI articles to process
MAX_ARTICLE_AGE_DAYS = 7              # Only last 7 days
MAX_EXECUTION_TIME_SECONDS = 300       # 5-minute timeout

# Customization
SUMMARY_LENGTH = "concise"             # brief/concise/detailed
DIGEST_FORMAT = "markdown"             # Output format
```

## Safeguards

Built-in protection against excessive runtime and stale content:

**Time Limits:**
- Overall workflow timeout: 5 minutes (hard limit)
- API call timeout: 30 seconds per call
- AI feed fetch timeout: 10 seconds per feed

**Content Freshness:**
- Only processes AI articles ≤7 days old
- Rejects articles with no/invalid dates
- Reports rejected article count

**Volume Controls:**
- Max 10 AI articles processed
- Max 5 AI RSS feeds checked
- Max 2 retries on failures

All limits configurable in `config.py`.

## Project Structure

```
ai-news-summariser-agent/
├── agents/                    # Agent modules
│   ├── base_agent.py         # Base class
│   ├── news_fetcher_agent.py # News collection
│   ├── summarizer_agent.py   # Summarization
│   └── compiler_agent.py     # Digest compilation
├── .cursorrules              # Coding standards
├── config.py                  # All configuration
├── orchestrator.py            # Workflow coordinator
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Programmatic Usage

```python
from orchestrator import NewsResearchOrchestrator

orchestrator = NewsResearchOrchestrator()
# Filter AI news by specific topics
filepath = orchestrator.run(max_articles=5, filter_criteria="GPT-4, LLMs, OpenAI")
```

See `example_usage.py` for more examples.

## Troubleshooting

- **API key error**: Create `.env` file with `OPENAI_API_KEY=your_key`
- **No AI articles**: Check internet connection and AI RSS feed URLs in config
- **Rate limits**: Reduce `MAX_ARTICLES` in config
- **Want different AI sources**: Edit `NEWS_SOURCES` in `config.py` to add your preferred AI news feeds

## Security

- Never commit `.env` files
- Monitor API usage on OpenAI dashboard
- Keep dependencies updated

