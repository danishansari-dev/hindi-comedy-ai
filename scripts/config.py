"""
Shared configuration for Phase 0 data collection scripts.

Centralizes paths, subreddit lists, YouTube channel IDs, and labeling
thresholds so scrapers stay consistent and easy to tune.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── Project paths ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist on import
for _dir in [RAW_DIR, PROCESSED_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── YouTube configuration ──
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# YouTube Comment thresholds for auto-labeling
# High likes = funny (proxy), low likes = not funny
YOUTUBE_COMMENT_FUNNY_THRESHOLD = 500
YOUTUBE_COMMENT_NOT_FUNNY_THRESHOLD = 5

# YouTube API settings
YOUTUBE_MAX_COMMENTS_PER_VIDEO = 100


# Video IDs for Hindi stand-up comedians
# Zakir Khan, Anubhav Singh Bassi, Abhishek Upmanyu
YOUTUBE_VIDEO_IDS = [
    # ── Zakir Khan ──
    "GXfnIJcp8lQ",  # Haq Se Single
    "PoEq3m7YXCQ",  # Sakht Launda
    "4zL5JBF-aV8",  # Tathastu
    "9VvnxPgFfxQ",  # Kaksha Gyarvi
    "bwqJFjGJ8KE",  # Mann Pasand
    "BEhg7MZ3YIg",  # Koi Baat Nahi
    "W_v24FrKWZg",  # Bachpan
    "d4dVl8i52cM",  # Naqaab
    "Vxn7tz9t7qU",  # Chai
    "hVH5G9_OkUo",  # Voh Wali Feeling

    # ── Anubhav Singh Bassi ──
    "dh-3pSi7RNM",  # Hostel
    "UrZeH_CpsJ4",  # Cheating
    "c5vRTwjCSYI",  # UPSC
    "wdGZBRRWPGo",  # Ghar Waapsi
    "S71GZX4TMLY",  # Woh Din
    "lZhKEQxd7jY",  # Engineering
    "1oC_3FRNJ2E",  # Interview
    "_2LQnwEcvIQ",  # Airport
    "3L7bexaRmVA",  # Breakup
    "YVnBV3TNWCA",  # CLAT

    # ── Abhishek Upmanyu ──
    "RLSL22gSwVM",  # Family Functions
    "z18Y9VxSbPc",  # Rich People - Poor People
    "59k6DMJMzVU",  # Relatives
    "dEsw6Wm8IcE",  # Friends, Crime, & The Cosmos
    "T9wh6GrO2sI",  # Shaadi, Breakup
    "gZBCBqJRVTw",  # Grocery Store Billing
    "mSd95CSZP-w",  # Gym and Breakup
    "-u3Jvqb32Jk",  # Neighbourhood Aunties
    "oGRR0rFQJOs",  # Summer Vacation
    "AJsPSzMjbIY",  # Gussa aur Sabzi
]

# Preferred transcript languages — try Hindi first, fall back to English
TRANSCRIPT_LANGUAGES = ["hi", "en", "hi-Latn"]

# ── Data file names ──
YOUTUBE_COMMENTS_OUTPUT_FILE = RAW_DIR / "youtube_comments.jsonl"
YOUTUBE_OUTPUT_FILE = RAW_DIR / "youtube_transcripts.jsonl"
YOUTUBE_SKIPPED_FILE = LOGS_DIR / "youtube_skipped.txt"
