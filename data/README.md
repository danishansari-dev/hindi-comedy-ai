# Data Directory

## Structure

```
data/
├── raw/                    # Auto-scraped, unreviewed content (gitignored)
│   ├── youtube_comments.jsonl    # YouTube comments scraper output
│   └── youtube_transcripts.jsonl # YouTube transcript output
├── processed/              # Cleaned, deduplicated, ready for annotation (gitignored)
│   ├── candidates.jsonl         # Merged & deduplicated from all sources
│   └── stats.json               # Collection statistics
└── README.md               # This file
```

## Phase 0 Gate Condition

**Target**: 2,000+ labeled examples with inter-annotator agreement κ > 0.35

### Data Sources

| Source | Expected Yield | Label Method |
|--------|---------------|-------------|
| YouTube Comments (100 top comments per video) | ~800-1,500 labeled | Auto-label by likes (≥500 = funny, <5 = not funny) |
| YouTube transcripts (30+ videos) | ~1,500 candidate segments | Manual review required |
| Khandelwal 2018 corpus | 3,543 tweets | Pre-labeled (classifier seed only) |

### Auto-labeling Rules

- YouTube Comment likes ≥ 500 → `label: 1` (funny proxy)
- YouTube Comment likes < 5 → `label: 0` (not funny proxy)
- YouTube Comment likes 5-499 → **excluded** (ambiguous)
- YouTube transcripts → no auto-label (requires manual annotation)

## Important Rules

1. **Do NOT train from `raw/`**. Every example must pass manual review first.
2. **Preserve per-annotator labels** — don't collapse to averages too early.
3. **Track disagreement** — high-variance items are signal, not noise.
4. **YouTube transcripts need chunking** — full 30-min transcripts are too long for annotation.
