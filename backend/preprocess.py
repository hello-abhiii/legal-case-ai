import pandas as pd
import re

# ── Step 1: Load the dataset ──
df = pd.read_csv("data/cases.csv")
print("Loaded", len(df), "cases")
print(df.head())

# ── Step 2: Clean text function ──
def clean_text(text):
    text = str(text)
    text = text.lower()                          # lowercase
    text = re.sub(r'<[^>]+>', '', text)          # remove HTML tags
    text = re.sub(r'[^a-z0-9\s]', '', text)     # remove special characters
    text = re.sub(r'\s+', ' ', text).strip()    # remove extra spaces
    return text

# ── Step 3: Apply cleaning ──
df['clean_facts'] = df['facts'].apply(clean_text)
df['clean_section'] = df['section'].apply(clean_text)
df['clean_court'] = df['court'].apply(clean_text)

# ── Step 4: Combine into one text column ──
df['combined_text'] = (
    df['clean_facts'] + " " +
    df['clean_section'] + " " +
    df['clean_court']
)

# ── Step 5: Save cleaned data ──
df.to_csv("data/cleaned_cases.csv", index=False)
print("\nCleaning done!")
print("Saved to data/cleaned_cases.csv")
print("\nSample combined text:")
print(df['combined_text'][0])
