"""
Multi-Agent System for AI News Researcher
"""
from .base_agent import BaseAgent
from .news_fetcher_agent import NewsFetcherAgent
from .summarizer_agent import SummarizerAgent
from .compiler_agent import DigestCompilerAgent

__all__ = [
    'BaseAgent',
    'NewsFetcherAgent',
    'SummarizerAgent',
    'DigestCompilerAgent'
]

