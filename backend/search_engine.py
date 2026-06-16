import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# ── Step 1: Load cleaned data ──
df = pd.read_csv("data/cleaned_cases.csv")
print("Loaded", len(df), "cases")

# ── Step 2: Load the embedding model ──
print("Loading embedding model... (first time takes 1-2 mins)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")

# ── Step 3: Convert all cases to vectors ──
print("Creating embeddings...")
embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')
print("Embeddings shape:", embeddings.shape)

# ── Step 4: Build FAISS index ──
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print("FAISS index built with", index.ntotal, "cases")

# ── Step 5: Save everything ──
faiss.write_index(index, "models/case_index.faiss")
df.to_csv("data/cleaned_cases.csv", index=False)

with open("models/embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("\nSearch engine ready!")
print("Saved: models/case_index.faiss")

# ── Step 6: Test a search ──
def find_similar_cases(query, top_k=3):
    query_vec = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vec, top_k)
    print(f"\nQuery: {query}")
    print(f"Top {top_k} similar cases:\n")
    for i, idx in enumerate(indices[0]):
        print(f"  {i+1}. {df['title'][idx]}")
        print(f"     Section : {df['section'][idx]}")
        print(f"     Outcome : {df['outcome'][idx]}")
        print(f"     Facts   : {df['facts'][idx]}")
        print()

# Test it
find_similar_cases("accused stole a bike from parking area ipc 379")
