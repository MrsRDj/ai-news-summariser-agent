"""
Orchestrator - Coordinates all agents in the news research system
"""
from agents import NewsFetcherAgent, SummarizerAgent, DigestCompilerAgent
import config
from typing import Optional
from datetime import datetime
import time


class NewsResearchOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        """Initialize all agents"""
        print("\n" + "="*70)
        print("AI NEWS RESEARCHER AGENT - Multi-Agent System")
        print("Focused exclusively on AI, ML, and AI Research news")
        print("="*70)
        
        self.fetcher = NewsFetcherAgent()
        self.summarizer = SummarizerAgent()
        self.compiler = DigestCompilerAgent()
        
        print(f"\n[+] Initialized {self.fetcher}")
        print(f"[+] Initialized {self.summarizer}")
        print(f"[+] Initialized {self.compiler}")
        
    def run(self, max_articles: Optional[int] = None, filter_criteria: Optional[str] = None) -> str:
        """
        Run the complete AI news research and digest compilation workflow with execution time limit
        
        Args:
            max_articles: Maximum number of AI articles to process
            filter_criteria: Optional criteria to filter AI articles
            
        Returns:
            Path to the generated AI news digest file
        """
        # Start timing the execution
        start_time = time.time()
        max_execution_time = config.MAX_EXECUTION_TIME_SECONDS
        
        print("\n" + "="*70)
        print("STARTING AI NEWS RESEARCH WORKFLOW")
        print("="*70)
        print(f"[TIME] Maximum execution time: {max_execution_time} seconds ({max_execution_time/60:.1f} minutes)")
        print(f"[DATE] Article age limit: {config.MAX_ARTICLE_AGE_DAYS} days")
        print(f"[NEWS] Maximum AI articles: {max_articles or config.MAX_ARTICLES}")
        
        # Step 1: Fetch AI news articles
        print("\n>>> PHASE 1: AI News Collection")
        articles = self.fetcher.fetch_news(max_articles=max_articles)
        
        # Check execution time
        elapsed_time = time.time() - start_time
        if elapsed_time > max_execution_time:
            print(f"\n[!] Execution time limit exceeded ({elapsed_time:.1f}s). Stopping workflow.")
            return None
        
        if not articles:
            print("\n[-] No AI articles fetched. Exiting.")
            return None
        
        # Step 2: Filter articles if criteria provided
        if filter_criteria:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_execution_time:
                print(f"\n[!] Execution time limit exceeded ({elapsed_time:.1f}s). Stopping workflow.")
                return None
                
            print(f"\n>>> PHASE 2: AI Article Filtering (Criteria: {filter_criteria})")
            articles = self.fetcher.filter_articles(articles, filter_criteria)
        
        # Step 3: Summarize AI articles
        elapsed_time = time.time() - start_time
        if elapsed_time > max_execution_time:
            print(f"\n[!] Execution time limit exceeded ({elapsed_time:.1f}s). Stopping workflow.")
            return None
            
        print("\n>>> PHASE 3: AI Article Summarization")
        summarized_articles = self.summarizer.summarize_articles(articles)
        
        # Step 4: Identify AI themes
        elapsed_time = time.time() - start_time
        if elapsed_time > max_execution_time:
            print(f"\n[!] Execution time limit exceeded ({elapsed_time:.1f}s). Stopping workflow.")
            return None
            
        print("\n>>> PHASE 4: AI Theme Identification")
        themes = self.summarizer.identify_themes(summarized_articles)
        print(f"\n{themes}")
        
        # Step 5: Compile AI news digest
        elapsed_time = time.time() - start_time
        if elapsed_time > max_execution_time:
            print(f"\n[!] Execution time limit exceeded ({elapsed_time:.1f}s). Stopping workflow.")
            return None
            
        print("\n>>> PHASE 5: AI News Digest Compilation")
        
        if config.DIGEST_FORMAT == "markdown":
            # Use structured markdown format
            digest = self.compiler.format_digest_markdown(summarized_articles, themes)
        else:
            # Use AI to compile in desired format
            digest = self.compiler.compile_digest(summarized_articles, themes)
        
        # Step 6: Save AI news digest
        print("\n>>> PHASE 6: Saving AI News Digest")
        filepath = self.compiler.save_digest(digest)
        
        # Summary
        total_time = time.time() - start_time
        print("\n" + "="*70)
        print("AI NEWS RESEARCH WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"\n[+] Processed {len(articles)} AI articles")
        print(f"[+] Generated AI summaries and insights")
        print(f"[+] Compiled AI news digest saved to: {filepath}")
        print(f"[TIME] Total execution time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print("\n" + "="*70)
        
        return filepath
    
    def run_interactive(self):
        """Run in interactive mode with user prompts"""
        print("\n" + "="*70)
        print("INTERACTIVE MODE")
        print("="*70)
        
        # Get user preferences
        try:
            max_articles = input(f"\nMaximum articles to process (default {config.MAX_ARTICLES}): ").strip()
            max_articles = int(max_articles) if max_articles else config.MAX_ARTICLES
        except ValueError:
            max_articles = config.MAX_ARTICLES
        
        filter_criteria = input("\nFilter criteria (e.g., 'GPT-4, LLMs, OpenAI' or press Enter to skip): ").strip()
        filter_criteria = filter_criteria if filter_criteria else None
        
        # Run workflow
        return self.run(max_articles=max_articles, filter_criteria=filter_criteria)


def main():
    """Main entry point"""
    import sys
    
    orchestrator = NewsResearchOrchestrator()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        orchestrator.run_interactive()
    else:
        # Run with defaults
        orchestrator.run()


if __name__ == "__main__":
    main()

