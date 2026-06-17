import pandas as pd
import re

# ── Load existing 66 cases ───────────────────────────────────────────────────
existing = pd.read_csv('data/cleaned_cases.csv')
print(f"✅ Existing cases: {len(existing)}")

# ── Load new 7030 cases ──────────────────────────────────────────────────────
new_data = pd.read_csv('data/indian_legal_7000cases.csv')
print(f"✅ New cases loaded: {len(new_data)}")

# ── Extract outcome from text using keyword matching ─────────────────────────
def extract_outcome(text):
    if not isinstance(text, str):
        return None
    text_lower = text.lower()

    # Acquittal signals
    acquittal_keywords = [
        "acquitted", "acquittal", "not guilty", "discharged",
        "appeal allowed", "conviction set aside", "benefit of doubt",
        "prosecution failed", "released", "no evidence"
    ]
    # Conviction signals
    conviction_keywords = [
        "convicted", "conviction", "found guilty", "guilty",
        "appeal dismissed", "sentence upheld", "imprisonment",
        "sentenced to", "rigorous imprisonment", "fine imposed",
        "upheld the conviction"
    ]

    acquittal_score = sum(1 for kw in acquittal_keywords if kw in text_lower)
    conviction_score = sum(1 for kw in conviction_keywords if kw in text_lower)

    if conviction_score > acquittal_score:
        return "Conviction"
    elif acquittal_score > conviction_score:
        return "Acquittal"
    else:
        return None  # ambiguous — will be dropped

# ── Extract IPC section from text ────────────────────────────────────────────
def extract_section(text):
    if not isinstance(text, str):
        return "IPC General"
    match = re.search(r'(section|s\.)\s*(\d+[A-Z]?)', text, re.IGNORECASE)
    if match:
        return f"IPC {match.group(2)}"
    match2 = re.search(r'IPC\s+(\d+[A-Z]?)', text, re.IGNORECASE)
    if match2:
        return f"IPC {match2.group(1)}"
    return "IPC General"

# ── Extract court from text ───────────────────────────────────────────────────
def extract_court(text):
    if not isinstance(text, str):
        return "High Court"
    text_lower = text.lower()
    if "supreme court" in text_lower:
        return "Supreme Court"
    elif "high court" in text_lower:
        return "High Court"
    elif "sessions court" in text_lower or "sessions judge" in text_lower:
        return "Sessions Court"
    elif "district court" in text_lower or "district judge" in text_lower:
        return "District Court"
    elif "magistrate" in text_lower:
        return "Magistrate Court"
    return "High Court"

# ── Process new cases ─────────────────────────────────────────────────────────
print("\n⏳ Extracting outcomes from 7030 cases...")
new_data['outcome']  = new_data['Text'].apply(extract_outcome)
new_data['section']  = new_data['Text'].apply(extract_section)
new_data['court']    = new_data['Text'].apply(extract_court)

# Drop ambiguous cases
before = len(new_data)
new_data = new_data.dropna(subset=['outcome'])
after = len(new_data)
print(f"✅ Clear outcomes found: {after} (dropped {before - after} ambiguous)")
print(f"   Convictions : {(new_data['outcome']=='Conviction').sum()}")
print(f"   Acquittals  : {(new_data['outcome']=='Acquittal').sum()}")

# ── Format new cases to match existing schema ─────────────────────────────────
new_formatted = pd.DataFrame({
    'case_id' : range(67, 67 + len(new_data)),
    'title'   : [f"Case {i+67}" for i in range(len(new_data))],
    'facts'   : new_data['Summary'].fillna(new_data['Text'].str[:500]).values,
    'section' : new_data['section'].values,
    'court'   : new_data['court'].values,
    'outcome' : new_data['outcome'].values,
})

# ── Merge datasets ────────────────────────────────────────────────────────────
merged = pd.concat([existing, new_formatted], ignore_index=True)
merged['case_id'] = range(1, len(merged) + 1)

# ── Save ─────────────────────────────────────────────────────────────────────
merged.to_csv('data/cleaned_cases.csv', index=False)
print(f"\n🎉 Merged dataset saved!")
print(f"   Total cases : {len(merged)}")
print(f"   Convictions : {(merged['outcome']=='Conviction').sum()}")
print(f"   Acquittals  : {(merged['outcome']=='Acquittal').sum()}")
print(f"\nOutcome distribution:")
print(merged['outcome'].value_counts())
print(f"\nTop sections:")
print(merged['section'].value_counts().head(10))
