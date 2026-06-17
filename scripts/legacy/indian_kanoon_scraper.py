import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = "legal_data"
TARGET_CASES = 4000
DELAY_MIN = 1.5   # seconds between requests (be respectful)
DELAY_MAX = 3.0

SEARCH_QUERIES = [
    # Criminal
    "murder IPC section 302",
    "theft IPC section 379",
    "fraud cheating IPC section 420",
    "kidnapping IPC section 363",
    "rape IPC section 376",
    "dowry death IPC section 304B",
    "assault IPC section 323",
    "robbery IPC section 392",
    # Civil
    "property dispute civil suit",
    "breach of contract damages",
    "divorce Hindu Marriage Act",
    "maintenance alimony family court",
    "landlord tenant eviction",
    "succession inheritance property",
    "defamation civil suit",
    # Constitutional
    "fundamental rights Article 21",
    "PIL public interest litigation",
    "habeas corpus writ petition",
    "right to equality Article 14",
    "freedom of speech Article 19",
    "writ of mandamus High Court",
    # Labour / Service
    "wrongful termination employment",
    "labour dispute industrial tribunal",
    "provident fund gratuity",
    # Tax / Corporate
    "income tax appeal tribunal",
    "GST dispute commercial court",
    "insolvency bankruptcy NCLT",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def search_page(query: str, pagenum: int) -> list[dict]:
    """Return list of {title, url, snippet, court, date} from one search page."""
    url = "https://indiankanoon.org/search/"
    params = {"formInput": query, "pagenum": pagenum}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"  [WARN] search failed ({e})")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for result in soup.select(".result"):
        title_tag = result.select_one(".result_title a")
        if not title_tag:
            continue
        snippet_tag = result.select_one(".snippet")
        meta_tag = result.select_one(".docsource")
        results.append({
            "title": title_tag.get_text(strip=True),
            "url": "https://indiankanoon.org" + title_tag["href"],
            "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
            "court": meta_tag.get_text(strip=True) if meta_tag else "",
            "date": "",
        })
    return results


def fetch_case(url: str) -> dict | None:
    """Fetch full judgment text from a case URL."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"  [WARN] fetch failed for {url} ({e})")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Full judgment text
    judgment_div = soup.select_one("#judgments") or soup.select_one(".judgments")
    text = judgment_div.get_text(separator="\n", strip=True) if judgment_div else ""

    # Date
    date_tag = soup.select_one(".docsource")
    date_str = date_tag.get_text(strip=True) if date_tag else ""

    # Citation / bench info
    citation_tag = soup.select_one(".doc_citation")
    citation = citation_tag.get_text(strip=True) if citation_tag else ""

    if len(text) < 200:   # skip near-empty pages
        return None

    return {
        "url": url,
        "full_text": text,
        "date": date_str,
        "citation": citation,
        "scraped_at": datetime.utcnow().isoformat(),
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_path = os.path.join(OUTPUT_DIR, "cases_index.json")
    full_path  = os.path.join(OUTPUT_DIR, "cases_full.jsonl")

    # Load already-scraped URLs to allow resume
    seen_urls: set[str] = set()
    if os.path.exists(full_path):
        with open(full_path) as f:
            for line in f:
                try:
                    seen_urls.add(json.loads(line)["url"])
                except Exception:
                    pass
        print(f"Resuming — {len(seen_urls)} cases already collected.")

    index_records = []
    total_saved = len(seen_urls)

    with open(full_path, "a", encoding="utf-8") as out_f:
        for query in SEARCH_QUERIES:
            if total_saved >= TARGET_CASES:
                break
            print(f"\n🔍 Query: '{query}'")

            for page in range(0, 10):   # up to 10 pages × ~10 results = 100 per query
                if total_saved >= TARGET_CASES:
                    break

                results = search_page(query, page)
                if not results:
                    break

                for meta in results:
                    if total_saved >= TARGET_CASES:
                        break
                    if meta["url"] in seen_urls:
                        continue

                    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
                    case = fetch_case(meta["url"])
                    if case is None:
                        continue

                    case.update({
                        "title":  meta["title"],
                        "court":  meta["court"],
                        "query":  query,
                    })

                    out_f.write(json.dumps(case, ensure_ascii=False) + "\n")
                    out_f.flush()
                    seen_urls.add(meta["url"])
                    index_records.append({
                        "title": meta["title"],
                        "url":   meta["url"],
                        "court": meta["court"],
                        "date":  case["date"],
                        "query": query,
                        "text_length": len(case["full_text"]),
                    })
                    total_saved += 1
                    print(f"  ✅ [{total_saved}/{TARGET_CASES}] {meta['title'][:70]}")

                time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    # Save index
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_records, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Done! {total_saved} cases saved to '{OUTPUT_DIR}/'")
    print(f"   • Full text : {full_path}")
    print(f"   • Index     : {index_path}")


if __name__ == "__main__":
    main()
