"""
Configuration file for AI News Researcher Agent

This agent is EXCLUSIVELY designed to collect and summarize AI-related news.
All sources and settings are strictly focused on:
- Artificial Intelligence
- Machine Learning
- AI Tools and Applications
- AI Research and Development
- AI Ethics and Policy

The system automatically filters out non-AI articles using keyword validation.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"  # Using the latest efficient model

# News Sources Configuration - AI-Focused
NEWS_SOURCES = {
    "rss_feeds": [
        # AI-Focused News Sources
        "https://www.artificialintelligence-news.com/feed/",
        "https://www.marktechpost.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        
        # Alternative: Add your own AI newsletter RSS feeds here
        # Many newsletters (like Superhuman AI) don't provide RSS feeds
        # but you can add any RSS-enabled AI news sources below:
    ],
    "categories": ["artificial-intelligence", "machine-learning", "ai-tools", "ai-research"]
}

# Agent Configuration - AI News Only
MAX_ARTICLES = 10  # Maximum number of AI articles to process
SUMMARY_LENGTH = "concise"  # Options: "concise", "detailed", "brief"
DIGEST_FORMAT = "markdown"  # Options: "markdown", "html", "plain"

# Article Collection Strategy
# Ensures diversity across sources and prevents first source from dominating
ARTICLES_PER_SOURCE = 5  # Collect this many from each source before ranking
DEDUPLICATION_THRESHOLD = 0.85  # Title similarity threshold for duplicates (0-1)
SMART_RANKING_ENABLED = True  # Use AI ranking when articles exceed threshold

# AI Keyword Filtering
# Articles must contain AI-related keywords to be included
# This ensures only genuine AI news is collected and summarized

# Time and Rate Limiting Configuration
MAX_ARTICLE_AGE_DAYS = 7  # Only process AI articles from the last 7 days
MAX_EXECUTION_TIME_SECONDS = 300  # Maximum 5 minutes total execution time
MAX_FEEDS_TO_PROCESS = 5  # Limit number of AI RSS feeds to process
FEED_FETCH_TIMEOUT_SECONDS = 10  # Timeout for each feed fetch
API_CALL_TIMEOUT_SECONDS = 30  # Timeout for each OpenAI API call
MAX_RETRIES = 2  # Maximum retries for failed operations

# Output Configuration
OUTPUT_DIRECTORY = "ai_news_digests"
OUTPUT_FILENAME_PREFIX = "ai_news_digest_"

