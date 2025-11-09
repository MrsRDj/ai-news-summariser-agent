"""
News Fetcher Agent - Responsible for collecting news from various sources
"""
import feedparser
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from .base_agent import BaseAgent
import config
import signal


class NewsFetcherAgent(BaseAgent):
    """Agent specialized in fetching AI news from various sources"""
    
    # AI-specific keywords for validation
    AI_KEYWORDS = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'neural network', 'llm', 'large language model', 'gpt', 'openai', 'claude',
        'gemini', 'chatbot', 'generative ai', 'gen ai', 'transformer', 'nlp',
        'natural language processing', 'computer vision', 'reinforcement learning',
        'ai model', 'ai tool', 'ai research', 'ai ethics', 'agi', 'ai safety',
        'anthropic', 'deepmind', 'hugging face', 'stable diffusion', 'midjourney',
        'ai agent', 'autonomous', 'neural', 'embeddings', 'vector database',
        'ai startup', 'ai investment', 'ai regulation', 'ai policy'
    ]
    
    def __init__(self):
        super().__init__(
            name="AI News Fetcher",
            role="AI News Collection Specialist",
            instructions="""You are an AI news collection specialist. Your role is to:
1. Fetch ONLY AI-related news articles from various RSS feeds and sources
2. Filter and validate articles for AI/ML relevance and quality
3. Focus exclusively on artificial intelligence, machine learning, AI tools, and AI research news
4. Extract key metadata (title, description, publication date, source)
5. Return structured data about AI news articles only
You prioritize credible tech sources and recent AI developments."""
        )
        
    def _is_ai_related(self, article_data: Dict[str, Any]) -> bool:
        """
        Check if an article is AI-related by analyzing title and description
        
        Args:
            article_data: Dictionary with 'title' and 'description' keys
            
        Returns:
            True if article contains AI-related keywords, False otherwise
        """
        title = article_data.get('title', '').lower()
        description = article_data.get('description', '').lower()
        combined_text = f"{title} {description}"
        
        # Check if any AI keyword appears in the article
        for keyword in self.AI_KEYWORDS:
            if keyword in combined_text:
                return True
        return False
    
    def _is_article_recent(self, published_date: str, max_age_days: int = None) -> bool:
        """
        Check if an article is recent enough based on publication date
        
        Args:
            published_date: Publication date string
            max_age_days: Maximum age in days (defaults to config value)
            
        Returns:
            True if article is recent enough, False otherwise
        """
        if max_age_days is None:
            max_age_days = config.MAX_ARTICLE_AGE_DAYS
        
        if not published_date or published_date == "Unknown date":
            # If no date, reject to be safe
            return False
        
        try:
            # Parse the date string
            article_date = date_parser.parse(published_date)
            current_date = datetime.now()
            
            # Normalize both to naive datetimes for comparison
            if article_date.tzinfo is not None:
                # Convert timezone-aware to naive by removing timezone info
                article_date = article_date.replace(tzinfo=None)
            
            # Calculate age
            age = current_date - article_date
            
            return age.days <= max_age_days
        except Exception as e:
            # If we can't parse the date, reject the article
            print(f"  [!] Could not parse date '{published_date}': {str(e)}")
            return False
    
    def _deduplicate_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate articles using local algorithms (no API calls)
        
        Strategy:
        1. Exact URL matching
        2. Title similarity (fuzzy matching)
        3. Keep the article with better description/more content
        
        Args:
            articles: List of articles to deduplicate
            
        Returns:
            Deduplicated list of articles
        """
        from difflib import SequenceMatcher
        
        def title_similarity(title1: str, title2: str) -> float:
            """Calculate similarity between two titles (0-1)"""
            return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
        
        deduplicated = []
        seen_urls = set()
        duplicates_removed = 0
        
        print(f"\n[{self.name}] Deduplicating {len(articles)} articles...")
        
        for article in articles:
            url = article['link']
            title = article['title']
            
            # Skip exact URL duplicates
            if url in seen_urls:
                duplicates_removed += 1
                continue
            
            # Check for similar titles (likely same story from different sources)
            is_duplicate = False
            for existing in deduplicated:
                similarity = title_similarity(title, existing['title'])
                
                # If titles exceed similarity threshold, consider it a duplicate
                if similarity > config.DEDUPLICATION_THRESHOLD:
                    duplicates_removed += 1
                    # Keep the one with more detailed description
                    if len(article['description']) > len(existing['description']):
                        # Replace existing with this better version
                        deduplicated.remove(existing)
                        deduplicated.append(article)
                        seen_urls.add(url)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduplicated.append(article)
                seen_urls.add(url)
        
        print(f"[{self.name}] Removed {duplicates_removed} duplicates, {len(deduplicated)} unique articles remain")
        
        return deduplicated
    
    def _rank_articles_efficiently(self, articles: List[Dict[str, Any]], target_count: int) -> List[Dict[str, Any]]:
        """
        Efficiently rank articles by newsworthiness with minimal API costs
        
        Cost optimization:
        - If articles <= target_count: No AI call needed
        - If slightly over: Use recency as tiebreaker (free)
        - If significantly over: One small AI call with compact prompt
        
        Args:
            articles: List of articles to rank
            target_count: Number of articles to select
            
        Returns:
            Top N most newsworthy articles
        """
        if len(articles) <= target_count:
            print(f"[{self.name}] {len(articles)} articles within limit, no ranking needed")
            return articles
        
        # Only use AI ranking if enabled and we have significantly more than needed
        if not config.SMART_RANKING_ENABLED or len(articles) <= target_count * 1.5:
            # Small overage - just use recency as tiebreaker (cost-free)
            print(f"[{self.name}] Using recency-based selection (cost-free)")
            try:
                sorted_articles = sorted(
                    articles,
                    key=lambda x: date_parser.parse(x['published']) if x['published'] != "Unknown date" else datetime.min,
                    reverse=True
                )
                return sorted_articles[:target_count]
            except:
                return articles[:target_count]
        
        # Significant overage - use AI but with compact prompt
        print(f"[{self.name}] AI ranking: {len(articles)} -> {target_count} articles (1 API call)")
        
        # COMPACT prompt - just titles and sources (cheaper than full descriptions)
        articles_text = "\n".join([
            f"{i+1}. [{article['source']}] {article['title']}"
            for i, article in enumerate(articles)
        ])
        
        task = f"""Rank these {len(articles)} AI news articles. Select the top {target_count} most newsworthy.

Consider:
- Breaking news and major announcements
- Significant research breakthroughs
- Important industry developments
- Diverse topics (don't pick all from one category)
- Source credibility and variety

AI Articles:
{articles_text}

Return ONLY the article numbers (comma-separated) of the top {target_count} most newsworthy articles, in order of importance.
Example format: 1,5,12,3,8,15,22,9,11,19"""
        
        try:
            response = self.execute(task)
            
            # Parse the response
            selected_indices = [int(num.strip()) - 1 for num in response.split(",")]
            ranked_articles = [articles[i] for i in selected_indices if 0 <= i < len(articles)]
            
            # Ensure we don't exceed target count
            ranked_articles = ranked_articles[:target_count]
            
            print(f"[{self.name}] Selected {len(ranked_articles)} most newsworthy articles")
            return ranked_articles
            
        except Exception as e:
            print(f"[{self.name}] Ranking failed ({str(e)}), using first {target_count} articles")
            return articles[:target_count]
    
    def fetch_news(self, max_articles: int = None) -> List[Dict[str, Any]]:
        """
        Fetch AI news with deduplication and cost-efficient ranking
        
        Optimized collection strategy:
        1. Collect from ALL sources (ensures diversity)
        2. Deduplicate locally (no API calls)
        3. Rank by newsworthiness if needed (minimal API cost)
        
        Args:
            max_articles: Maximum number of articles to fetch
            
        Returns:
            List of recent, unique, newsworthy AI articles
        """
        if max_articles is None:
            max_articles = config.MAX_ARTICLES
            
        articles = []
        feeds = config.NEWS_SOURCES.get("rss_feeds", [])
        
        # Limit number of feeds to process
        feeds = feeds[:config.MAX_FEEDS_TO_PROCESS]
        
        # Calculate articles per source to ensure diversity
        articles_per_source = config.ARTICLES_PER_SOURCE
        
        print(f"\n[{self.name}] Fetching AI news from {len(feeds)} sources...")
        print(f"[{self.name}] Strategy: {articles_per_source} articles per source -> up to {articles_per_source * len(feeds)} total")
        print(f"[{self.name}] Date filter: Last {config.MAX_ARTICLE_AGE_DAYS} days")
        print(f"[{self.name}] AI keyword filter: Active")
        
        rejected_old_articles = 0
        rejected_non_ai_articles = 0
        
        # PHASE 1: Collect from all sources (no early termination)
        for feed_url in feeds:
            try:
                # Parse feed with timeout
                feed = feedparser.parse(feed_url)
                source_name = feed.feed.get("title", "Unknown Source")
                
                feed_articles_added = 0
                
                for entry in feed.entries:
                    # Limit per source (not total) to ensure diversity
                    if feed_articles_added >= articles_per_source:
                        break
                    
                    published_date = entry.get("published", entry.get("updated", "Unknown date"))
                    
                    # Check if article is recent enough
                    if not self._is_article_recent(published_date):
                        rejected_old_articles += 1
                        continue
                    
                    # Create article data
                    article = {
                        "title": entry.get("title", "No Title"),
                        "description": entry.get("summary", entry.get("description", "No description available")),
                        "link": entry.get("link", ""),
                        "published": published_date,
                        "source": source_name,
                        "fetched_at": datetime.now().isoformat()
                    }
                    
                    # Check if article is AI-related
                    if not self._is_ai_related(article):
                        rejected_non_ai_articles += 1
                        continue
                    
                    articles.append(article)
                    feed_articles_added += 1
                    
                print(f"  [+] {feed_articles_added} articles from {source_name}")
                
            except Exception as e:
                print(f"  [-] Error: {feed_url[:50]}: {str(e)}")
                continue
        
        print(f"\n[{self.name}] Collected {len(articles)} AI articles from all sources")
        if rejected_old_articles > 0:
            print(f"[{self.name}] Filtered: {rejected_old_articles} old, {rejected_non_ai_articles} non-AI")
        
        # Return early if no articles
        if not articles:
            return articles
        
        # PHASE 2: Deduplicate locally (no API cost)
        articles = self._deduplicate_articles(articles)
        
        # PHASE 3: Efficient ranking (minimal API cost)
        if len(articles) > max_articles:
            articles = self._rank_articles_efficiently(articles, max_articles)
        
        print(f"\n[{self.name}] Final result: {len(articles)} unique, newsworthy AI articles")
        
        return articles
    
    def filter_articles(self, articles: List[Dict[str, Any]], criteria: str = None) -> List[Dict[str, Any]]:
        """
        Filter AI articles based on specific criteria using AI
        
        Args:
            articles: List of AI articles to filter
            criteria: Filter criteria (e.g., "GPT-4, LLMs, OpenAI")
            
        Returns:
            Filtered list of AI articles
        """
        if not criteria or len(articles) <= config.MAX_ARTICLES:
            return articles
        
        # Use AI to filter articles based on criteria
        articles_text = "\n".join([
            f"{i+1}. {article['title']} - {article['source']}"
            for i, article in enumerate(articles)
        ])
        
        task = f"""Review these AI news articles and select the most relevant ones based on: {criteria}
        
AI Articles:
{articles_text}

Return only the article numbers (comma-separated) of the most relevant AI articles."""
        
        response = self.execute(task)
        
        # Parse response and filter articles
        try:
            selected_indices = [int(num.strip()) - 1 for num in response.split(",")]
            filtered = [articles[i] for i in selected_indices if 0 <= i < len(articles)]
            print(f"\n[{self.name}] Filtered to {len(filtered)} relevant articles")
            return filtered
        except:
            # If parsing fails, return original articles
            return articles

