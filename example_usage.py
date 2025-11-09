"""
Example usage of the AI News Researcher Agent
"""
from orchestrator import NewsResearchOrchestrator


def example_basic():
    """Example: Basic usage with defaults - fetches latest AI news"""
    print("Example 1: Basic AI News Fetch\n" + "="*50)
    
    orchestrator = NewsResearchOrchestrator()
    digest_path = orchestrator.run()
    
    print(f"\nAI News Digest saved to: {digest_path}")


def example_custom():
    """Example: Custom parameters for specific AI topics"""
    print("\n\nExample 2: Custom AI Topics\n" + "="*50)
    
    orchestrator = NewsResearchOrchestrator()
    digest_path = orchestrator.run(
        max_articles=5,
        filter_criteria="GPT-4, Large Language Models, OpenAI"
    )
    
    print(f"\nAI News Digest saved to: {digest_path}")


def example_programmatic():
    """Example: Programmatic usage with custom AI news workflow"""
    print("\n\nExample 3: Custom AI News Workflow\n" + "="*50)
    
    from agents import NewsFetcherAgent, SummarizerAgent, DigestCompilerAgent
    
    # Create individual AI news agents
    fetcher = NewsFetcherAgent()
    summarizer = SummarizerAgent()
    compiler = DigestCompilerAgent()
    
    # Step-by-step AI news workflow
    print("\n1. Fetching AI news...")
    articles = fetcher.fetch_news(max_articles=3)
    
    print("\n2. Summarizing AI articles...")
    summarized = summarizer.summarize_articles(articles)
    
    print("\n3. Compiling AI news digest...")
    digest = compiler.format_digest_markdown(summarized)
    
    print("\n4. Saving AI news digest...")
    filepath = compiler.save_digest(digest)
    
    print(f"\nAI News Digest saved to: {filepath}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "basic":
            example_basic()
        elif sys.argv[1] == "custom":
            example_custom()
        elif sys.argv[1] == "programmatic":
            example_programmatic()
        else:
            print("Usage: python example_usage.py [basic|custom|programmatic]")
    else:
        # Run all examples
        example_basic()
        # Uncomment to run all examples:
        # example_custom()
        # example_programmatic()

