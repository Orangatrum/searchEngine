import json
import os
import re
import sqlite3

from dotenv import load_dotenv
from exa_py import Exa

load_dotenv()


def get_db_connection():
    conn = sqlite3.connect("cache.db")
    conn.execute("CREATE TABLE IF NOT EXISTS search_cache (query TEXT PRIMARY KEY, response TEXT)")
    return conn


def get_cached_result(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM search_cache WHERE query = ?", (query,))
    row = cursor.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None


def save_to_cache(query, response):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO search_cache (query, response) VALUES (?, ?)",
        (query, json.dumps(response, ensure_ascii=False)),
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

    normalized_query = query.lower()
    cached = get_cached_result(normalized_query)
    if cached:
        return {"source": "cache", "data": cached}

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment variable not found. Please check your .env file.")

    exa = Exa(api_key=api_key)
    response = exa.search(
        query=query,
        num_results=5,
        contents={"summary": True},
    )

    normalized_results = [
        {
            "title": getattr(item, "title", "Untitled Result"),
            "url": getattr(item, "url", "#"),
            "summary": highlight_matches(getattr(item, "summary", "No summary available."), query),
        }
        for item in response.results
    ]

    save_to_cache(normalized_query, normalized_results)
    return {"source": "exa_api", "data": normalized_results}
