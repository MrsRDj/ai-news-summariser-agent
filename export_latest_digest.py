"""
Utility script to export the most recent AI news digest to a JSON file.

Used by CI (GitHub Actions) to produce a machine-readable representation
that can be consumed by external systems (e.g., a frontend application).
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json


DIGEST_DIR = Path("ai_news_digests")
OUTPUT_PATH = Path("public/latest.json")


def main() -> None:
    """Export the latest markdown digest as a JSON payload."""
    DIGEST_DIR.mkdir(exist_ok=True)

    digest_files = sorted(DIGEST_DIR.glob("ai_news_digest_*.md"), reverse=True)
    if not digest_files:
        raise SystemExit("No digest files found in ai_news_digests/")

    latest = digest_files[0]
    markdown_text = latest.read_text(encoding="utf-8")

    payload = {
        "filename": latest.name,
        "generated_at": datetime.now().isoformat(),
        "markdown": markdown_text,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()


