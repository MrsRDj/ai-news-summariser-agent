"""
Digest Compiler Agent - Responsible for compiling summaries into a formatted digest
"""
from typing import List, Dict, Any
from datetime import datetime
from .base_agent import BaseAgent
import config


class DigestCompilerAgent(BaseAgent):
    """Agent specialized in compiling AI news summaries into a digest format"""
    
    def __init__(self):
        super().__init__(
            name="AI Digest Compiler",
            role="AI Content Organization and Formatting Specialist",
            instructions="""You are a professional AI news editor and content organizer. Your role is to:
1. Organize AI news summaries into a coherent, easy-to-read digest
2. Create engaging introductions highlighting key AI developments
3. Group related AI stories together by theme (e.g., LLMs, tools, research, ethics)
4. Format content for optimal readability for tech professionals
5. Add editorial touches that make AI insights compelling
6. Maintain a professional yet accessible tone for AI enthusiasts

Create AI news digests that busy tech professionals and AI enthusiasts will actually want to read."""
        )
        
    def compile_digest(self, articles: List[Dict[str, Any]], themes: str = None) -> str:
        """
        Compile AI articles into a formatted digest
        
        Args:
            articles: List of summarized AI articles
            themes: Optional identified AI themes
            
        Returns:
            Formatted AI news digest as a string
        """
        print(f"\n[{self.name}] Compiling AI news digest from {len(articles)} articles...")
        
        # Prepare articles text
        articles_content = []
        for i, article in enumerate(articles, 1):
            article_text = f"""
Article {i}:
Title: {article['title']}
Source: {article['source']}
Link: {article['link']}
Summary: {article.get('ai_summary', article['description'])}
"""
            articles_content.append(article_text)
        
        # Create compilation task
        task = f"""Compile these AI news articles into a professional, engaging AI news digest.

Format: {config.DIGEST_FORMAT}

Articles:
{''.join(articles_content)}

{f"Identified Themes: {themes}" if themes else ""}

Create a digest with:
1. An engaging title for today's AI news digest
2. A brief introduction (2-3 sentences) highlighting key AI stories
3. Well-organized AI article summaries with clear headers
4. Smooth transitions between AI topics
5. A brief conclusion with key AI takeaways

Make it informative, scannable, and engaging for AI enthusiasts and tech professionals."""
        
        digest = self.execute(task)
        
        print(f"[{self.name}] AI news digest compiled successfully!")
        return digest
    
    def format_digest_markdown(self, articles: List[Dict[str, Any]], themes: str = None) -> str:
        """
        Format AI news digest in Markdown
        
        Args:
            articles: List of summarized AI articles
            themes: Optional identified AI themes
            
        Returns:
            Markdown formatted AI news digest
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Header
        markdown = f"""# AI News Digest
## {current_date}

---

"""
        
        # Introduction
        if themes:
            markdown += f"""### Today's Key Themes
{themes}

---

"""
        
        # Articles
        markdown += "## Top Stories\n\n"
        
        for i, article in enumerate(articles, 1):
            summary = article.get('ai_summary', '')
            
            markdown += f"""### {i}. {article['title']}

**Source:** {article['source']}  
**Link:** [{article['link']}]({article['link']})

{summary}

---

"""
        
        # Footer
        markdown += f"""
*This digest was compiled by AI News Researcher Agent*  
*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        return markdown
    
    def save_digest(self, digest: str, filename: str = None) -> str:
        """
        Save digest to file
        
        Args:
            digest: The digest content
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
        
        # Generate filename
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{config.OUTPUT_FILENAME_PREFIX}{timestamp}.md"
        
        filepath = os.path.join(config.OUTPUT_DIRECTORY, filename)
        
        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(digest)
        
        print(f"\n[{self.name}] Digest saved to: {filepath}")
        return filepath

