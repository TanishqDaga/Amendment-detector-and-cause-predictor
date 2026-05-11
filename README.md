# NLP-Based Regulatory Document Change Detection System

An intelligent **Natural Language Processing (NLP)** framework designed to compare two versions of policy, regulation, or rule-based documents and automatically detect:

- Added rules
- Deleted rules
- Modified rules
- Numerical changes
- Intent behind modifications
- Predicted causes for amendments

The system combines **rule-based NLP**, **semantic similarity using Sentence-BERT**, and **domain-aware reasoning** to generate explainable insights from evolving documents.

---

# 📌 Project Overview

Organizations frequently update policies, academic regulations, legal rules, and compliance documents. Traditional text comparison methods fail to capture semantic modifications, contextual changes, and numerical updates effectively.

This project solves that problem using a hybrid NLP architecture capable of understanding meaning rather than relying only on exact textual differences.

---

# 🧠 Key Features

- PDF document extraction
- Text cleaning and normalization
- Rule-level segmentation
- Hybrid sector classification
- Semantic change detection using SBERT
- Numerical value comparison
- Intent detection
- Cause prediction engine
- Structured JSON output generation

---

# 🏗️ System Architecture

![Architecture](assets/Architecture.png)

---

# ⚙️ Workflow

## 1. Input Layer – Document Versions

The system takes two PDF documents as input:

- Old Document (PDF)
- New Document (PDF)

These documents may contain:
- Textual regulations
- Rules
- Tables
- Semi-structured content
- Numeric policies

---

## 2. Document Extraction Module

This module extracts usable content from PDFs.

### Technologies Used
- PyMuPDF → Primary text extraction
- pdfplumber → Fallback extraction
- OCR (optional) → Diagram/image text extraction

### Features
- Text extraction from all pages
- Table extraction and conversion into text
- Robust handling of poorly formatted PDFs

---

## 3. Text Cleaning & Normalization

Extracted content is standardized for NLP processing.

### Operations
- Regex-based cleaning
- Removal of irregular formatting
- Decimal value protection
- Sentence reconstruction
- Broken line merging

### Example

Before:
```text
Minimum attendance
required is 75 . 0 %
```

After:
```text
Minimum attendance required is 75.0%
```

---

## 4. Rule Segmentation

The cleaned document is divided into meaningful rule units.

### Techniques
- Section pattern recognition
- Sentence segmentation
- Fragment filtering

### Output

```python
[
  "Students must maintain 75% attendance.",
  "Late fee payment attracts penalty.",
  "Project submission deadline is 6 weeks."
]
```

---

# 🧠 Hybrid Classification Engine

This is the core intelligence layer of the system.

It classifies each rule into a domain-specific sector using three complementary approaches.

---

## A. Priority Rule Engine

Uses predefined keyword overrides for highly critical terms.

### Example

```python
{
   "misconduct": "Discipline",
   "fee": "Finance"
}
```

Ensures important rules are never misclassified.

---

## B. Keyword Scoring Model

Uses domain-specific keyword dictionaries.

### Working
- Counts keyword occurrences
- Assigns weighted scores
- Produces category likelihood

---

## C. SBERT Semantic Similarity Model

Uses Sentence-BERT (`all-MiniLM-L6-v2`) for semantic understanding.

### Process
- Convert rules into embeddings
- Convert sector descriptions into embeddings
- Compute cosine similarity
- Assign semantic relevance score

---

## Final Sector Assignment

```python
Final Score = 0.4 * Keyword Score + 0.6 * Semantic Score
```

This hybrid approach improves robustness against paraphrased or rewritten text.

---

# 🔍 Semantic Change Detection

This module compares old and new document rules semantically.

### Method
- Generate SBERT embeddings
- Compute cosine similarity
- Apply similarity threshold

### Outputs

| Change Type | Description |
|---|---|
| Added | Present only in new document |
| Deleted | Present only in old document |
| Modified | Semantically similar but textually different |

### Example

Old:
```text
Minimum attendance required is 75%.
```

New:
```text
Minimum attendance required is 80%.
```

Detected:
```text
Modified Rule
```

Unlike traditional diff systems, this captures meaning-level changes.

---

# 🔢 Numerical Analysis

Detects quantitative modifications in rules.

### Extracted Elements
- Percentages
- Currency values
- Durations
- Thresholds

### Examples

```text
75% → 80%
₹1000 → ₹2000
6 weeks → 8 weeks
```

This ensures critical numerical policy updates are highlighted explicitly.

---

# 🎯 Intent Detection

Determines the purpose behind each rule modification.

### Technique
Rule-based keyword matching.

### Example Intents
- Attendance
- Finance
- Evaluation
- Discipline

### Example

```text
"Students must pay fee before due date"

→ Intent: Finance
```

This adds contextual understanding to amendments.

---

# 🧩 Cause Prediction Engine

One of the most advanced modules in the system.

It transforms raw changes into explainable insights using:
- Rule-based reasoning
- Semantic similarity
- Dataset-driven relevance

---

## Working Pipeline

### 1. Input
- Old rule
- New rule
- Intent label

---

### 2. Intent Mapping
Maps rules to predefined intent categories.

---

### 3. Knowledge Base (CAUSE_KB)

Maps intents to possible reasons.

### Example

```python
CAUSE_KB = {
   "Attendance": [
      "Improve discipline",
      "Increase classroom engagement"
   ],
   "Finance": [
      "Operational cost management",
      "Ensure timely payment"
   ]
}
```

---

### 4. Dataset Support

Uses:
- `cause_dataset.json`
- `cause_embeddings.pt`

Generated using Sentence-BERT embeddings.

This enables:
- Context-aware reasoning
- Better cause prediction accuracy

---

### 5. Hybrid Cause Selection

Combines:
- Intent filtering
- Semantic relevance
- Dataset similarity

Returns the most probable causes.

---

### Example Outputs

```text
Attendance increase
→ Improve discipline
→ Increase engagement
```

```text
Fee increase
→ Operational cost management
→ Ensure timely payment
```

---

# 📤 Output Generator

The final module compiles all findings into structured outputs.

## Output Includes
- Added rules
- Deleted rules
- Modified rules
- Sector classification
- Numerical changes
- Intent labels
- Predicted causes

---

# 📄 JSON Output Example

```json
{
  "modified_rules": [
    {
      "old": "Minimum attendance required is 75%",
      "new": "Minimum attendance required is 80%",
      "intent": "Attendance",
      "numerical_change": "75% -> 80%",
      "predicted_causes": [
        "Improve discipline",
        "Increase engagement"
      ]
    }
  ]
}
```

---

# 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| NLP Framework | Sentence-BERT |
| Embedding Model | all-MiniLM-L6-v2 |
| PDF Extraction | PyMuPDF, pdfplumber |
| OCR | Tesseract OCR |
| Similarity Metric | Cosine Similarity |
| Data Handling | JSON |
| ML Library | PyTorch |
| Regex Processing | Python re |

---

# 📂 Suggested Project Structure

```text
project/
│
├── data/
│   ├── old_document.pdf
│   ├── new_document.pdf
│   ├── cause_dataset.json
│   └── cause_embeddings.pt
│
├── extraction/
├── preprocessing/
├── segmentation/
├── classification/
├── change_detection/
├── numerical_analysis/
├── intent_detection/
├── cause_prediction/
├── output/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Future Improvements

- GUI Dashboard
- Multi-language support
- Legal-domain fine-tuned transformers
- Explainable AI visualization
- Real-time amendment monitoring
- Cloud deployment APIs

---

# 📈 Applications

- Academic regulation analysis
- Legal document comparison
- Government policy tracking
- Compliance auditing
- Financial regulation monitoring
- Corporate policy management

---

# 🤝 Contribution

Contributions are welcome.

You can contribute by:
- Improving NLP accuracy
- Adding new domains
- Enhancing semantic reasoning
- Optimizing performance
- Building frontend dashboards

---



---

# 👨‍💻 Author

Developed as an NLP-based intelligent document amendment analysis system for semantic policy comparison and explainable change detection.
