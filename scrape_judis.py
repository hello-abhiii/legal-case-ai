import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

print("🔍 Scraping JUDIS - Supreme Court of India...")

BASE_URL = "https://judis.nic.in"
cases = []

SEARCH_TERMS = [
    "theft IPC 379",
    "cheating IPC 420", 
    "assault IPC 323",
    "forgery IPC 468",
    "robbery IPC 392",
    "kidnapping IPC 363",
    "murder IPC 302",
    "fraud IPC 420"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text[:500]

def extract_outcome(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ['acquitted', 'acquittal', 'not guilty', 'discharged']):
        return 'Acquittal'
    elif any(w in text_lower for w in ['convicted', 'conviction', 'guilty', 'sentenced']):
        return 'Conviction'
    return None

def extract_section(text):
    sections = re.findall(r'(?:IPC|I\.P\.C|Section|Sec\.?)\s*(\d+[A-Z]?)', text, re.IGNORECASE)
    if sections:
        return f"IPC {sections[0]}"
    return "IPC"

for term in SEARCH_TERMS:
    print(f"  Searching: {term}...")
    try:
        url = f"https://judis.nic.in/judis/SearchResultsDetails.aspx"
        params = {"txt_keyword": term, "txt_petitioner": "", "txt_respondent": ""}
        res = requests.get(url, params=params, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')

        # Find case links
        links = soup.find_all('a', href=re.compile(r'Casejudis|case|judgment', re.I))[:5]

        for link in links:
            try:
                case_url = link.get('href', '')
                if not case_url.startswith('http'):
                    case_url = BASE_URL + '/' + case_url.lstrip('/')

                case_res = requests.get(case_url, headers=headers, timeout=15)
                case_soup = BeautifulSoup(case_res.text, 'lxml')

                # Extract text
                body = case_soup.get_text(separator=' ')
                body = clean_text(body)

                outcome = extract_outcome(body)
                if not outcome:
                    continue

                title = link.get_text(strip=True) or "Supreme Court Case"
                section = extract_section(body + term)

                cases.append({
                    'title': title[:80],
                    'facts': body[:300],
                    'section': section,
                    'court': 'Supreme Court',
                    'outcome': outcome
                })
                print(f"    ✅ Got case: {title[:40]}... → {outcome}")
                time.sleep(1)

            except Exception as e:
                print(f"    ⚠️ Skipped a case: {e}")
                continue

        time.sleep(2)

    except Exception as e:
        print(f"  ❌ Search failed for '{term}': {e}")
        continue

print(f"\n📊 Total real cases scraped: {len(cases)}")

if cases:
    # Combine with existing data
    existing = pd.read_csv("data/cleaned_cases.csv")
    new_df = pd.DataFrame(cases)
    new_df['case_id'] = range(len(existing) + 1, len(existing) + len(cases) + 1)

    combined = pd.concat([existing, new_df], ignore_index=True)
    combined['case_id'] = range(1, len(combined) + 1)
    combined.to_csv("data/cleaned_cases.csv", index=False)
    print(f"✅ Dataset updated: {len(combined)} total cases saved!")
else:
    print("⚠️ No cases scraped. JUDIS may be blocking requests.")
    print("   Trying fallback: eCourts dataset...")
