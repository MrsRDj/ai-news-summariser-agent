"""
Main entry point for AI News Researcher Agent
"""
from orchestrator import NewsResearchOrchestrator
import config
import sys


def main():
    """Main function to run the AI News Researcher Agent"""
    
    # Check if OpenAI API key is configured
    if not config.OPENAI_API_KEY:
        print("\n" + "="*70)
        print("ERROR: OPENAI_API_KEY not configured")
        print("="*70)
        print("\nPlease set your OpenAI API key in a .env file:")
        print("  1. Create a file named '.env' in the project root")
        print("  2. Add the line: OPENAI_API_KEY=your_api_key_here")
        print("\nYou can get an API key from: https://platform.openai.com/api-keys")
        print("="*70 + "\n")
        sys.exit(1)
    
    # Create orchestrator and run
    orchestrator = NewsResearchOrchestrator()
    
    # Check if interactive mode is requested
    if "--interactive" in sys.argv or "-i" in sys.argv:
        orchestrator.run_interactive()
    else:
        # Run with default configuration
        orchestrator.run()


if __name__ == "__main__":
    main()

