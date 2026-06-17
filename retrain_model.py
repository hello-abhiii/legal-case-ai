import pandas as pd
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
import faiss

# ── Load merged dataset ───────────────────────────────────────────────────────
df = pd.read_csv('data/cleaned_cases.csv')
print(f"✅ Loaded {len(df)} cases")
print(f"   Convictions : {(df['outcome']=='Conviction').sum()}")
print(f"   Acquittals  : {(df['outcome']=='Acquittal').sum()}")

# ── Prepare features ──────────────────────────────────────────────────────────
# Combine facts + section + court into one text feature
df['combined_text'] = (
    df['facts'].fillna('') + ' ' +
    df['section'].fillna('') + ' ' +
    df['court'].fillna('')
)

X = df['combined_text']
y = df['outcome']

# ── Train TF-IDF vectorizer ───────────────────────────────────────────────────
print("\n⏳ Training TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),   # unigrams + bigrams
    stop_words='english',
    min_df=2
)
X_vec = vectorizer.fit_transform(X)
print(f"✅ Vectorizer trained — vocab size: {len(vectorizer.vocabulary_)}")

# ── Train Logistic Regression ─────────────────────────────────────────────────
print("\n⏳ Training Logistic Regression model...")
model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    class_weight='balanced',
    random_state=42
)
model.fit(X_vec, y)
print("✅ Model trained!")

# ── Cross-validation ──────────────────────────────────────────────────────────
print("\n⏳ Running 5-Fold Cross Validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_vec, y, cv=cv, scoring='accuracy')
print(f"✅ CV Accuracy: {scores.mean()*100:.2f}% (+/- {scores.std()*100:.2f}%)")
print(f"   Per fold: {[f'{s*100:.1f}%' for s in scores]}")

# ── Full classification report ────────────────────────────────────────────────
y_pred = model.predict(X_vec)
print("\n📊 Classification Report:")
print(classification_report(y, y_pred))
print("Confusion Matrix:")
cm = confusion_matrix(y, y_pred, labels=['Conviction', 'Acquittal'])
print(f"                 Conviction  Acquittal")
print(f"Actual Conviction   {cm[0][0]:>6}     {cm[0][1]:>6}")
print(f"Actual Acquittal    {cm[1][0]:>6}     {cm[1][1]:>6}")

# ── Build FAISS index for similar case search ─────────────────────────────────
print("\n⏳ Building FAISS index...")
X_dense = X_vec.toarray().astype('float32')
dimension = X_dense.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(X_dense)
print(f"✅ FAISS index built with {index.ntotal} vectors")

# ── Save all models ───────────────────────────────────────────────────────────
print("\n⏳ Saving models...")
with open('models/prediction_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

faiss.write_index(index, 'models/case_index.faiss')

print("✅ Saved:")
print("   models/prediction_model.pkl")
print("   models/vectorizer.pkl")
print("   models/case_index.faiss")
print(f"\n🎉 Done! Model retrained on {len(df)} cases!")
