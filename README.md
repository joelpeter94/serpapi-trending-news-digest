# trending-news-digest

A small CLI that fetches Google News results for a topic via [SerpAPI](https://serpapi.com/) and prints a digest to the terminal. Can also save the digest as Markdown.

## Setup

Uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env   # then paste your SerpAPI key
```

Get a key from https://serpapi.com/manage-api-key (free tier: 100 searches/month).

## Usage

```bash
uv run main.py "artificial intelligence"
uv run main.py "climate change" --sort-by-date --limit 5 --save digest.md
uv run main.py "elections" --country uk --language en
```

## Options

| Flag | Default | Description |
|---|---|---|
| `query` | required | Topic to search |
| `--country` | `us` | Country code (`gl`) |
| `--language` | `en` | Language code (`hl`) |
| `--limit` | `10` | Max articles to show |
| `--sort-by-date` | off | Sort by date instead of relevance |
| `--save PATH` | - | Also write a Markdown digest to `PATH` |
