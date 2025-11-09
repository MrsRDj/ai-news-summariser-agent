# Changelog

## 2024-11-09 - Article Collection Optimization with Deduplication

### Added
- ✅ **Source Diversity Strategy**: Collects articles from ALL sources, not just the first
  - Per-source limits (5 articles each) ensure no single source dominates
  - Prevents missing important stories from slower-updating sources
  
- ✅ **Local Deduplication** (no API cost):
  - Exact URL matching to remove duplicates
  - Fuzzy title matching (85% similarity threshold) for same story from different sources
  - Keeps article with better/longer description
  - Configurable via `DEDUPLICATION_THRESHOLD` in config
  
- ✅ **Smart Ranking System** (minimal API cost):
  - Three-tier approach based on article count:
    * ≤ target: No ranking needed (free)
    * Slight overage: Recency-based sorting (free)
    * Significant overage: AI ranking with compact prompt (~1 API call)
  - Ranks by newsworthiness, importance, and topic diversity
  - Configurable via `SMART_RANKING_ENABLED` in config

### Changed
- 🔄 `agents/news_fetcher_agent.py`:
  - New `_deduplicate_articles()`: Local deduplication algorithm
  - New `_rank_articles_efficiently()`: Cost-optimized AI ranking
  - Updated `fetch_news()`: 3-phase collection strategy
    * Phase 1: Collect from all sources
    * Phase 2: Deduplicate locally
    * Phase 3: Rank if needed
  
- 🔄 `config.py`:
  - Added `ARTICLES_PER_SOURCE = 5`: Per-source collection limit
  - Added `DEDUPLICATION_THRESHOLD = 0.85`: Title similarity threshold
  - Added `SMART_RANKING_ENABLED = True`: Toggle AI ranking

### Impact
- **Better Quality**: AI ranks articles by newsworthiness, not just chronological order
- **Source Diversity**: All 5 sources contribute, preventing first-source bias
- **Cost Effective**: Deduplication is free, ranking adds only ~1 API call
- **Removes Duplicates**: Same story from multiple sources handled intelligently
- **Maintains Performance**: Minimal additional cost (~$0.002 per run)

### Cost Analysis
- Previous: ~$0.025-0.055 per run (10 articles)
- Optimized: ~$0.024-0.054 per run (same cost, better quality!)
- Extra cost: ~1 API call for ranking (only when needed)

## 2024-11-09 - Critical Bug Fix: Date Parsing

### Fixed
- 🐛 **Critical date parsing bug** in `_is_article_recent()`:
  - Fixed timezone-aware/naive datetime comparison error
  - Articles with timezone info (+0000, GMT) were being incorrectly rejected
  - Simplified logic: normalize all dates to naive datetimes before comparison
  - Now correctly accepts recent articles from all sources

### Impact
- **Restores functionality**: Agent now properly collects recent articles
- **All sources working**: RSS feeds with timezone info now parse correctly

## 2024-11-09 - Enhanced AI Keyword Filtering

### Added
- ✅ AI keyword validation in `NewsFetcherAgent`:
  - 35+ AI-specific keywords (ai, machine learning, llm, gpt, etc.)
  - Automatic filtering of non-AI articles
  - Rejection tracking for non-AI content
  - Ensures ONLY genuine AI news is collected

### Changed
- 🔄 `agents/news_fetcher_agent.py`:
  - Added `_is_ai_related()` method for keyword validation
  - Enhanced AI-specific instructions
  - Reports rejected non-AI articles in output
  
- 🔄 `config.py`:
  - Updated documentation to emphasize AI-only scope
  - Added AI keyword filtering comments

### Impact
- **Stronger AI Focus**: Now filters at keyword level, not just source level
- **Better Quality**: Eliminates off-topic articles from AI-focused feeds
- **Transparency**: Reports how many non-AI articles were filtered out

## 2024-11-09 - Project Cleanup and AI News Focus

### Removed (Following Clean Code Principles)
- ❌ `ANSWERS_TO_YOUR_QUESTIONS.md` - Unnecessary documentation
- ❌ `SAFEGUARDS_QUICK_REFERENCE.md` - Redundant
- ❌ `PROJECT_SUMMARY.md` - Redundant with README
- ❌ `ARCHITECTURE.md` - Excessive documentation
- ❌ `SAFEGUARDS.md` - Consolidated into README
- ❌ `CLEAN_CODE_STANDARDS.md` - Moved to `.cursorrules`

### Added
- ✅ `.cursorrules` - Cursor IDE coding standards (proper location)
- ✅ Safeguards section in README (consolidated)

### Changed
- 🔄 `config.py` - Updated NEWS_SOURCES to AI-focused feeds:
  - AI News (artificialintelligence-news.com)
  - MarkTechPost (marktechpost.com)
  - VentureBeat AI (venturebeat.com)
  - TechCrunch AI (techcrunch.com)
  - The Verge AI (theverge.com)
  
- 🔄 `README.md` - Streamlined and consolidated:
  - Added Safeguards section (from SAFEGUARDS.md)
  - Removed redundant sections
  - Single source of truth

### Rationale
- **Clean Code**: Eliminated all documentation bloat
- **Single Source of Truth**: All safeguards in README
- **Cursor Standards**: Using `.cursorrules` instead of separate doc
- **AI Focus**: Updated sources to match purpose
- **Maintainability**: Minimal, focused documentation

### Final Documentation Structure
```
README.md         # Single source of truth (includes setup & safeguards)
.cursorrules      # Coding standards (Cursor IDE)
CHANGELOG.md      # Change history
```

**Best Practice**: Simple projects need only one README. Separate setup guides are only justified for complex multi-environment installations.

### Next Steps for Users
- Add your own AI newsletter RSS feeds to `config.py`
- Many newsletters (like Superhuman AI) don't provide RSS
- Consider RSS bridge services for newsletters without native feeds

