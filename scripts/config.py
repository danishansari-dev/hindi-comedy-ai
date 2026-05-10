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
    "vflWLItnwfA",
    "sIl8vsWrD8o",
    "kWj8DQ5GTxM",
    "rBCHIdqso3c",
    "5LOR8_H1I2I",
    "wy9IYJxne0E",
    "NVg3bRE8q8U",
    "--YMwaJy5ec",
    "GO1XngB-LS8",
    "XV8eCftsnn0",

    # ── Anubhav Singh Bassi ──
    "IEfBBYmxtIo",
    "ynS6X7kno3E",
    "qkxuFKqJXWY",
    "mbOO0Z6ryO0",
    "Tqsz6fjvhZM",
    "XbiObxjyAkE",
    "wQA68Oqr1qE",
    "0guSWBSO8lo",
    "z12bz7adLKI",
    "tSrjpbFF9Yc",

    # ── Abhishek Upmanyu ──
    "t8HrZTLRCeU",
    "IcAV5qiko8M",
    "c7QYEedjb_o",
    "dtaJzUbQS7E",
    "_fWyWcZB7VA",
    "AyafgNZZees",
    "mPCDQ34S8Rs",
    "Slqo8SHnFaU",
    "E16WhXcIghM",
    "uvqD_VUZI24",
]

# Preferred transcript languages — try Hindi first, fall back to English
TRANSCRIPT_LANGUAGES = ["hi", "en", "hi-Latn"]

# ── Data file names ──
YOUTUBE_COMMENTS_OUTPUT_FILE = RAW_DIR / "youtube_comments.jsonl"
YOUTUBE_OUTPUT_FILE = RAW_DIR / "youtube_transcripts.jsonl"
YOUTUBE_SKIPPED_FILE = LOGS_DIR / "youtube_skipped.txt"
