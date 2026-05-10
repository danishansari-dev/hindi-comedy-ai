"""
YouTube Comment scraper for Hindi stand-up comedy.

Collects top comments from curated Hindi stand-up comedy videos as a replacement
for Reddit data. Comments with high like counts on comedy videos are often
quotes of the best punchlines or original funny riffs.

High-like comments (>= 500) get label=1 (funny proxy).
Low-like comments (< 5) get label=0 (not funny proxy).
Middle band is excluded.

Usage:
    python -m scripts.scrape_youtube_comments
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from scripts.config import (
    YOUTUBE_API_KEY,
    YOUTUBE_VIDEO_IDS,
    YOUTUBE_COMMENT_FUNNY_THRESHOLD,
    YOUTUBE_COMMENT_NOT_FUNNY_THRESHOLD,
    YOUTUBE_MAX_COMMENTS_PER_VIDEO,
    YOUTUBE_COMMENTS_OUTPUT_FILE,
    LOGS_DIR,
)

# ── Logging setup ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "youtube_comments_scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

def assign_label(like_count: int) -> int | None:
    """
    Auto-label a comment based on its like count.
    """
    if like_count >= YOUTUBE_COMMENT_FUNNY_THRESHOLD:
        return 1
    elif like_count < YOUTUBE_COMMENT_NOT_FUNNY_THRESHOLD:
        return 0
    return None

def fetch_top_comments(youtube, video_id: str, max_results: int = 100) -> list[dict]:
    """
    Fetch top comments for a given video ID using YouTube Data API.
    """
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance",
            textFormat="plainText"
        )
        response = request.execute()
        
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            text = snippet["textDisplay"]
            like_count = snippet["likeCount"]
            
            label = assign_label(like_count)
            if label is None:
                continue
                
            comments.append({
                "text": text.strip(),
                "label": label,
                "source": f"youtube_comment/{video_id}",
                "score": like_count,
                "video_id": video_id,
                "author": snippet.get("authorDisplayName", "unknown"),
                "published_at": snippet["publishedAt"],
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })
            
    except HttpError as e:
        logger.error(f"HTTP error occurred while fetching comments for {video_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error for {video_id}: {e}")
        
    return comments

def save_comments(comments: list[dict], output_path: Path) -> None:
    """
    Append comments to JSONL file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        for comment in comments:
            f.write(json.dumps(comment, ensure_ascii=False) + "\n")
    logger.info(f"Saved {len(comments)} comments to {output_path}")

def main():
    """Entry point for the YouTube comment scraper."""
    if not YOUTUBE_API_KEY:
        logger.error("YOUTUBE_API_KEY is not set in the environment.")
        return

    logger.info(f"Downloading comments for {len(YOUTUBE_VIDEO_IDS)} videos...")
    
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    all_comments = []
    for i, video_id in enumerate(YOUTUBE_VIDEO_IDS, 1):
        logger.info(f"[{i}/{len(YOUTUBE_VIDEO_IDS)}] Fetching comments for {video_id}")
        comments = fetch_top_comments(youtube, video_id, max_results=YOUTUBE_MAX_COMMENTS_PER_VIDEO)
        all_comments.extend(comments)
        logger.info(f"  Found {len(comments)} usable comments (labeled).")
        
    if all_comments:
        save_comments(all_comments, YOUTUBE_COMMENTS_OUTPUT_FILE)

    funny_count = sum(1 for c in all_comments if c["label"] == 1)
    not_funny_count = sum(1 for c in all_comments if c["label"] == 0)

    logger.info(
        f"\n{'='*50}\n"
        f"COMMENT SCRAPE COMPLETE\n"
        f"  Total comments saved: {len(all_comments)}\n"
        f"  Funny (label=1): {funny_count}\n"
        f"  Not funny (label=0): {not_funny_count}\n"
        f"  Output: {YOUTUBE_COMMENTS_OUTPUT_FILE}\n"
        f"{'='*50}"
    )

if __name__ == "__main__":
    main()
