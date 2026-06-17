import pandas as pd, pickle, warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import faiss

all_cases = pd.read_csv('data/cleaned_cases.csv')
orig = all_cases[all_cases['case_id'] <= 66].copy()
print(f"Clean cases: {len(orig)} | Total cases: {len(all_cases)}")

orig['combined'] = orig['facts'].fillna('') + ' ' + orig['section'].fillna('') + ' ' + orig['court'].fillna('')
vec = TfidfVectorizer(max_features=3000, ngram_range=(1,2), sublinear_tf=True)
X = vec.fit_transform(orig['combined'])
y = orig['outcome']

model = LogisticRegression(max_iter=5000, solver='saga', C=1.0, class_weight='balanced', random_state=42)
scores = cross_val_score(model, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring='accuracy')
print(f"CV Accuracy: {scores.mean()*100:.2f}%")
model.fit(X, y)
print(classification_report(y, model.predict(X)))

all_cases['combined'] = all_cases['facts'].fillna('') + ' ' + all_cases['section'].fillna('') + ' ' + all_cases['court'].fillna('')
vec2 = TfidfVectorizer(max_features=8000, ngram_range=(1,2), sublinear_tf=True, min_df=2)
X2 = vec2.fit_transform(all_cases['combined']).toarray().astype('float32')
idx = faiss.IndexFlatL2(X2.shape[1])
idx.add(X2)

pickle.dump(model, open('models/prediction_model.pkl','wb'))
pickle.dump(vec,   open('models/vectorizer.pkl','wb'))
pickle.dump(vec2,  open('models/search_vectorizer.pkl','wb'))
faiss.write_index(idx, 'models/case_index.faiss')
print(f"Done! Prediction: {scores.mean()*100:.2f}% | Search index: {idx.ntotal} cases")
