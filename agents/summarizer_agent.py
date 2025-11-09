"""
Summarizer Agent - Responsible for analyzing and summarizing news articles
"""
from typing import List, Dict, Any
from .base_agent import BaseAgent
import config


class SummarizerAgent(BaseAgent):
    """Agent specialized in summarizing AI news articles"""
    
    def __init__(self):
        super().__init__(
            name="AI News Summarizer",
            role="AI Content Analysis and Summarization Specialist",
            instructions="""You are a professional AI news analyst and summarizer. Your role is to:
1. Analyze AI news articles for key information and insights
2. Extract important facts about AI/ML developments, tools, and research
3. Create concise, accurate, and engaging summaries focused on AI advancements
4. Identify key themes and connections between AI stories
5. Maintain objectivity and factual accuracy in AI reporting
6. Write in clear, professional language suitable for busy tech readers
7. Highlight implications for AI industry, developers, and businesses

For each article, provide:
- A compelling headline (if improving the original)
- A 2-3 sentence summary capturing the essence
- Key points in bullet format
- Why this matters for AI (1 sentence impact statement)"""
        )
        
    def summarize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single AI news article
        
        Args:
            article: Article dictionary with title, description, etc.
            
        Returns:
            Article with added summary field
        """
        task = f"""Summarize this AI news article:

Title: {article['title']}
Source: {article['source']}
Description: {article['description']}

Provide a {config.SUMMARY_LENGTH} summary including:
1. Main headline (improve if needed)
2. Brief summary (2-3 sentences)
3. Key points (3-5 bullet points)
4. Impact statement (why this matters)

Format your response as:
HEADLINE: [headline]
SUMMARY: [summary]
KEY POINTS:
- [point 1]
- [point 2]
- [point 3]
IMPACT: [impact statement]"""
        
        summary = self.execute(task)
        
        # Parse the summary
        article_summary = {
            **article,
            "ai_summary": summary
        }
        
        return article_summary
    
    def summarize_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Summarize multiple articles
        
        Args:
            articles: List of articles to summarize
            
        Returns:
            List of articles with summaries
        """
        print(f"\n[{self.name}] Summarizing {len(articles)} articles...")
        
        summarized_articles = []
        for i, article in enumerate(articles, 1):
            print(f"  Processing article {i}/{len(articles)}: {article['title'][:50]}...")
            try:
                summarized = self.summarize_article(article)
                summarized_articles.append(summarized)
            except Exception as e:
                print(f"  [-] Error summarizing article: {str(e)}")
                # Keep original article without summary
                summarized_articles.append(article)
        
        print(f"\n[{self.name}] Completed summarization of {len(summarized_articles)} articles")
        return summarized_articles
    
    def identify_themes(self, articles: List[Dict[str, Any]]) -> List[str]:
        """
        Identify common themes across multiple AI articles
        
        Args:
            articles: List of summarized AI articles
            
        Returns:
            List of identified AI themes
        """
        articles_text = "\n\n".join([
            f"Article {i+1}: {article['title']}\n{article.get('ai_summary', article['description'])}"
            for i, article in enumerate(articles)
        ])
        
        task = f"""Analyze these AI news articles and identify 3-5 major AI themes or trends:

{articles_text}

List the themes as bullet points with brief explanations."""
        
        themes_response = self.execute(task)
        
        return themes_response

