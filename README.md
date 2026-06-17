# ⚖️ Legal Case Outcome Prediction & Similar Case Recommendation System

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.137-green?logo=fastapi)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.9-orange?logo=scikit-learn)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-purple?logo=render)
![GitHub Pages](https://img.shields.io/badge/Frontend-GitHub%20Pages-black?logo=github)

> **Academic Year 2026–2027 | Department of Information Retrieval & ML | Summer Internship Project**

A full-stack AI-powered system that assists legal professionals by predicting court case outcomes and recommending similar past judgments using Machine Learning and Natural Language Processing.

---

## 🌐 Live Demo

| | URL |
|---|---|
| 🎨 **Frontend** | https://hello-abhiii.github.io/legal-case-ai |
| ⚡ **Backend API** | https://legal-case-ai.onrender.com |
| 📋 **API Docs** | https://legal-case-ai.onrender.com/docs |
| 💻 **GitHub** | https://github.com/hello-abhiii/legal-case-ai |

> ⚠️ The free Render instance may take 30–50 seconds to wake up on first request.

---

## 📸 Screenshots

### Home Page
![Home](docs/screenshots/home.png)

### Prediction Result
![Result](docs/screenshots/result.png)

---

## 📌 Project Synopsis

This system assists legal professionals by leveraging **Artificial Intelligence** and **Natural Language Processing** to analyze legal cases and provide data-driven insights. It serves as a **decision-support tool** for lawyers, law students, and legal researchers — not to replace legal professionals or judicial decision-making.

When a user enters a new case, the system:
1. Converts the case details into numerical vectors using **TF-IDF**
2. Searches a database of historical judgments using **Cosine Similarity**
3. Returns the **top 3 most similar past cases**
4. Predicts the likely **outcome (Conviction / Acquittal)**
5. Provides an **explanation** referencing similar influencing cases

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.14 |
| **Backend Framework** | FastAPI |
| **ML Model** | Logistic Regression (Scikit-learn) |
| **Text Vectorization** | TF-IDF (Scikit-learn) |
| **Similarity Search** | Cosine Similarity |
| **Database** | PostgreSQL 15 |
| **Frontend** | HTML, Tailwind CSS, Chart.js |
| **Backend Hosting** | Render |
| **Frontend Hosting** | GitHub Pages |

---

## 📊 Model Performance

Evaluated using **5-Fold Cross Validation** on 66 Indian court cases:

| Metric | Score |
|---|---|
| ✅ Accuracy | **95.49%** |
| ✅ Precision | **95.90%** |
| ✅ Recall | **95.49%** |
| ✅ F1 Score | **95.19%** |

### Confusion Matrix
```
                 Conviction  Acquittal
Actual Conviction     50          0
Actual Acquittal       0         16
```

> Target accuracy was 70–85%. Our model **exceeds** the target at 95%.

---

## 📁 Dataset

Custom dataset of **66 realistic Indian court cases** based on real IPC sections and empirical conviction rates:

| IPC Section | Crime | Cases |
|---|---|---|
| IPC 379 | Theft | 10 |
| IPC 420 | Cheating / Fraud | 10 |
| IPC 323 | Voluntarily Causing Hurt | 8 |
| IPC 380 | Theft in Dwelling House | 6 |
| IPC 468 | Forgery | 6 |
| IPC 392 | Robbery | 4 |
| IPC 506 | Criminal Intimidation | 4 |
| IPC 363 | Kidnapping | 4 |
| IPC 302 | Murder | 4 |
| IPC 325 | Grievous Hurt | 4 |
| IPC 447 | Criminal Trespass | 3 |
| IPC 384 | Extortion | 3 |

---

## 🚀 Project Structure

```
legal_ai/
├── backend/
│   └── main.py              # FastAPI application
├── data/
│   └── cleaned_cases.csv    # Dataset (66 cases)
├── models/
│   ├── prediction_model.pkl # Trained ML model
│   ├── vectorizer.pkl       # TF-IDF vectorizer
│   └── case_index.faiss     # FAISS index
├── frontend/
│   └── index.html           # Web interface
├── docs/
│   └── index.html           # GitHub Pages deployment
├── evaluate.py              # Model evaluation script
├── download_dataset.py      # Dataset builder
├── setup_db.py              # PostgreSQL setup
├── import_cases.py          # Import cases to DB
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 15
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/hello-abhiii/legal-case-ai.git
cd legal-case-ai
```

### Step 2 — Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up PostgreSQL
```bash
psql postgres -c "CREATE DATABASE legal_ai;"
python3 setup_db.py
python3 import_cases.py
```

### Step 5 — Train the model
```bash
python3 download_dataset.py
```

### Step 6 — Run the backend
```bash
uvicorn backend.main:app --reload
```

### Step 7 — Open the frontend
```bash
open frontend/index.html
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/analyze` | Predict case outcome |
| GET | `/cases` | Get all cases |
| GET | `/history` | Get prediction history |

### Example Request
```bash
curl -X POST "https://legal-case-ai.onrender.com/analyze" \
-H "Content-Type: application/json" \
-d '{
  "facts": "accused stole a bike from parking area",
  "section": "IPC 379",
  "court": "District Court"
}'
```

### Example Response
```json
{
  "predicted_outcome": "Conviction",
  "confidence": "85.22%",
  "similar_cases": [
    {
      "title": "State vs Dinesh",
      "section": "IPC 379",
      "outcome": "Conviction",
      "facts": "accused stole a bicycle from parking area near market"
    }
  ],
  "explanation": [
    "Similar to State vs Dinesh which ended in Conviction"
  ]
}
```

---

## 📋 Development Phases

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Requirement Analysis | ✅ Done |
| Phase 2 | Data Collection | ✅ Done |
| Phase 3 | Data Cleaning | ✅ Done |
| Phase 4 | Data Preprocessing (NLP) | ✅ Done |
| Phase 5 | Feature Extraction (TF-IDF) | ✅ Done |
| Phase 6 | Similar Case Search Engine | ✅ Done |
| Phase 7 | Outcome Prediction Model | ✅ Done |
| Phase 8 | Model Evaluation (95% accuracy) | ✅ Done |
| Phase 9 | Explanation System | ✅ Done |
| Phase 10 | FastAPI Backend | ✅ Done |
| Phase 11 | PostgreSQL Database | ✅ Done |
| Phase 12 | Frontend Development | ✅ Done |
| Phase 13 | Testing | ✅ Done |
| Phase 14 | Deployment (Render + GitHub Pages) | ✅ Done |

---

## ⚠️ Disclaimer

This system is designed as a **decision-support tool** for academic and research purposes only. It does **not** replace legal professionals or judicial decision-making. Always consult a qualified legal professional for actual legal advice.

---

## 👨‍💻 Author

**Abhinav**
Department of Information Retrieval & ML
Academic Year 2026–2027

---

## 📄 License

This project is for academic purposes only. Dataset based on publicly available Indian court case information.
