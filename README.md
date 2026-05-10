# Hindi Comedy AI

Phase 0 foundation for a Hindi/Hinglish comedy AI project — punchline ranking and evaluation system.

## Phase 0 — Data Foundation

**Gate condition**: 2,000+ labeled examples with inter-annotator agreement κ > 0.35

### Data Collection Scripts

| Script | Source | Command |
|--------|--------|---------|
| YouTube comments scraper | Top 100 comments from curated comedy videos | `python -m scripts.scrape_youtube_comments` |
| YouTube transcripts | Zakir Khan, Anubhav Singh Bassi, Abhishek Upmanyu (30 videos) | `python -m scripts.scrape_youtube` |

## Setup

### 1. Create virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure credentials

```powershell
Copy-Item .env.example .env
# Edit .env and ensure your YOUTUBE_API_KEY is set
# Get it at: https://console.cloud.google.com/apis/credentials
```

### 3. Run data collection

```powershell
# Scrape YouTube Comments (requires YOUTUBE_API_KEY in .env)
python -m scripts.scrape_youtube_comments

# Download YouTube transcripts (no auth required)
python -m scripts.scrape_youtube
```

### CLI Options

```powershell
# YouTube: specific videos, disable chunking
python -m scripts.scrape_youtube --video-ids VIDEO_ID_1 VIDEO_ID_2 --chunk-size 0
```

## Project Structure

```
hindi-comedy-ai/
├── scripts/
│   ├── config.py                     # Shared configuration (paths, thresholds, video IDs)
│   ├── scrape_youtube_comments.py    # YouTube comment scraper with auto-labeling
│   └── scrape_youtube.py             # YouTube transcript downloader with chunking
├── data/
│   ├── raw/                   # Scraped data (gitignored)
│   └── processed/             # Cleaned data for annotation (gitignored)
├── docs/
│   ├── research_notes.md      # Research takeaways and design constraints
│   ├── task_spec.md           # Formal task definition
│   ├── annotation_schema.md   # JSONL schemas for pair/preference data
│   └── label_studio_config.xml # Label Studio annotation interface
├── logs/                      # Scraper logs and skipped video lists
├── .env.example               # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

## Phase Roadmap

| Phase | Goal | Gate |
|-------|------|------|
| **0 — Data Foundation** ← current | Collect & label 2,000+ examples | κ > 0.35 inter-annotator agreement |
| 1 — Annotation & Baseline | Human preference data, baseline ranker | Ranker beats random on held-out set |
| 2 — Reward Model | Train punchline scorer from preferences | Reward model agrees with humans >60% |
| 3 — Generation Loop | Generator → scorer → critique → rewrite | Human eval prefers refined over raw |
| 4 — App & Feedback | FastAPI + React UI, feedback collection | Deployed with live feedback loop |
| 5 — Iteration | Continuous improvement from user feedback | Ongoing |

## Current Scope

The first trainable model is a **punchline ranker/scorer** trained from human preference data. Generation uses prompted frontier models initially — the evaluator must exist before the generator matters.

## Architecture Rules (from research)

1. Build the dataset before the model
2. Keep generation, ranking, safety/offense, and audience fit as separate evaluation axes
3. Capture disagreement, not just average ratings
4. Prefer pairwise comparisons for reward modeling
5. Define audience and violation boundaries before scraping at scale
6. Treat Hindi, Hinglish, and English-heavy Hinglish as separate but related distributions
