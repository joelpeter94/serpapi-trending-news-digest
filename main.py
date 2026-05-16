import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from serpapi import GoogleSearch

console = Console()


def fetch_news(query, api_key, country, language, sort_by_date):
    params = {
        "engine": "google_news",
        "q": query,
        "gl": country,
        "hl": language,
        "api_key": api_key,
    }
    if sort_by_date:
        params["so"] = "1"

    results = GoogleSearch(params).get_dict()

    if "error" in results:
        console.print(f"[bold red]SerpAPI error:[/] {results['error']}")
        sys.exit(1)

    return results.get("news_results", [])


def flatten(results):
    flat = []
    for item in results:
        if "highlight" in item:
            flat.append(item["highlight"])
            flat.extend(item.get("stories", []))
        elif isinstance(item.get("stories"), list):
            flat.extend(item["stories"])
        else:
            flat.append(item)
    return flat


def article_fields(art):
    title = art.get("title", "(untitled)")
    source = (art.get("source") or {}).get("name", "Unknown source")
    return title, source, art.get("date", ""), art.get("link", "")


def render_terminal(query, articles):
    if not articles:
        console.print("[yellow]No news results found.[/]")
        return

    header = (
        f"[bold cyan]Trending News Digest[/]\n"
        f"[dim]Topic:[/] {query}  [dim]Fetched:[/] {datetime.now():%Y-%m-%d %H:%M}"
    )
    console.print(Panel.fit(header, border_style="cyan"))

    for i, art in enumerate(articles, start=1):
        title, source, date, link = article_fields(art)
        console.print(f"\n[bold]{i}. {title}[/]")
        console.print(f"   [magenta]{source}[/] [dim]· {date}[/]")
        console.print(f"   [blue underline]{link}[/]")


def render_markdown(query, articles):
    lines = [
        f"# Trending News Digest: {query}",
        f"_Generated {datetime.now():%Y-%m-%d %H:%M}_",
        "",
    ]
    for i, art in enumerate(articles, start=1):
        title, source, date, link = article_fields(art)
        lines.append(f"## {i}. [{title}]({link})")
        lines.append(f"**{source}** · {date}")
        lines.append("")
    return "\n".join(lines)


def parse_args():
    p = argparse.ArgumentParser(description="Fetch a trending news digest via SerpAPI.")
    p.add_argument("query", help="Search topic, e.g. 'artificial intelligence'")
    p.add_argument("--country", default="us", help="Country code (default: us)")
    p.add_argument("--language", default="en", help="Language code (default: en)")
    p.add_argument("--limit", type=int, default=10, help="Max articles to show (default: 10)")
    p.add_argument("--sort-by-date", action="store_true", help="Sort by date instead of relevance")
    p.add_argument("--save", metavar="PATH", help="Also write a Markdown digest to PATH")
    return p.parse_args()


def main():
    args = parse_args()

    load_dotenv()
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        console.print("[bold red]Missing SERPAPI_API_KEY.[/] Copy .env.example to .env and set your key.")
        sys.exit(1)

    raw = fetch_news(args.query, api_key, args.country, args.language, args.sort_by_date)
    articles = flatten(raw)[: args.limit]

    render_terminal(args.query, articles)

    if args.save:
        out = Path(args.save)
        out.write_text(render_markdown(args.query, articles), encoding="utf-8")
        console.print(f"\n[green]Saved digest to[/] {out}")


if __name__ == "__main__":
    main()
