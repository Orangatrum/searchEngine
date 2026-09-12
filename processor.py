import json
import os
import re
import sqlite3

from dotenv import load_dotenv
from exa_py import Exa

load_dotenv()


def get_db_connection():
    conn = sqlite3.connect("cache.db")
    conn.execute("CREATE TABLE IF NOT EXISTS search_cache (cache_key TEXT PRIMARY KEY, response TEXT)")
    return conn


def get_cached_result(cache_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM search_cache WHERE cache_key = ?", (cache_key,))
    row = cursor.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None


def save_to_cache(cache_key, response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO search_cache (cache_key, response) VALUES (?, ?)",
        (cache_key, json.dumps(response, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()


def highlight_matches(text, query):
    if not text or not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(r"**\g<0>**", text)


def process_search(data):
    query = (data.get("query") or "").strip()
    if not query:
        raise ValueError("A search query is required.")

    # Extract filter parameters including publication dates
    include_domains = data.get("include_domains")
    exclude_domains = data.get("exclude_domains")
    category = data.get("category")
    start_published_date = data.get("start_published_date")  # ISO String e.g. "2024-01-01T00:00:00.000Z"
    end_published_date = data.get("end_published_date")      # ISO String e.g. "2026-12-31T23:59:59.999Z"

    normalized_query = query.lower()

    # Build a composite cache key so filtered searches cache independently
    cache_key_data = {
        "query": normalized_query,
        "include_domains": sorted(include_domains) if include_domains else None,
        "exclude_domains": sorted(exclude_domains) if exclude_domains else None,
        "category": category,
        "start_published_date": start_published_date,
        "end_published_date": end_published_date,
    }
    cache_key = json.dumps(cache_key_data, sort_keys=True)

    # Check cache using composite key
    cached = get_cached_result(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment variable not found. Please check your .env file.")

    # Construct search options for Exa
    search_kwargs = {
        "query": query,
        "num_results": 5,
        "contents": {"summary": True},
    }

    if include_domains:
        search_kwargs["include_domains"] = include_domains
    if exclude_domains:
        search_kwargs["exclude_domains"] = exclude_domains
    if category:
        search_kwargs["category"] = category
    if start_published_date:
        search_kwargs["start_published_date"] = start_published_date
    if end_published_date:
        search_kwargs["end_published_date"] = end_published_date

    exa = Exa(api_key=api_key)
    response = exa.search(**search_kwargs)

    normalized_results = [
        {
            "title": getattr(item, "title", "Untitled Result"),
            "url": getattr(item, "url", "#"),
            "summary": highlight_matches(getattr(item, "summary", "No summary available."), query),
            "published_date": getattr(item, "published_date", None),
        }
        for item in response.results
    ]

    save_to_cache(cache_key, normalized_results)
    return {"source": "exa_api", "data": normalized_results}