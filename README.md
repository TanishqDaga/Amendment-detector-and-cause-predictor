# NLP-Based Regulatory Document Change Detection System

> 📜 **Published Indian Patent Application**
>
> **Patent Title:** *System and Method for Amendment Detection and Analysis for Regulatory Documents*
>
> **Application Number:** **202641076170**
>
> **Publication Year:** **2026**

An intelligent **Natural Language Processing (NLP)** framework for automatically detecting, analyzing, and explaining amendments between different versions of regulatory, legal, academic, and policy documents.

The patented framework combines **rule-based NLP**, **Sentence-BERT semantic similarity**, **domain-aware reasoning**, and **explainable AI** to identify meaningful document changes beyond traditional text comparison techniques.

---

# 📌 Project Overview

Regulatory and policy documents are frequently updated across government organizations, universities, enterprises, and legal institutions. Conventional document comparison tools primarily rely on textual differences, making them ineffective in understanding semantic modifications, contextual changes, and numerical amendments.

This project introduces a **patented AI-driven amendment detection framework** capable of identifying meaningful changes while also predicting the intent and probable causes behind modifications.

The work has been recognized as a **Published Indian Patent Application** for its novel hybrid approach toward regulatory document analysis.

---

# 📜 Patent Information

**Patent Title**

**System and Method for Amendment Detection and Analysis for Regulatory Documents**

**Application Number**

**202641076170**

### Patent Highlights

The patented system introduces an intelligent NLP pipeline capable of:

- Semantic amendment detection
- Rule-level comparison
- Intent prediction
- Cause prediction
- Numerical change analysis
- Domain-aware classification
- Explainable AI-driven document analysis

> **Note:** This repository contains the research prototype and implementation corresponding to the published patent.

---

# 🧠 Key Features

- AI-based amendment detection
- Patent-backed hybrid NLP architecture
- PDF document extraction
- Text normalization
- Rule-level segmentation
- Hybrid sector classification
- Semantic similarity using Sentence-BERT
- Numerical change detection
- Intent identification
- Cause prediction engine
- Structured JSON output generation
- Explainable amendment analysis

---

# 🏗️ Patented System Architecture

![Architecture](assets/Architecture.png)

The architecture consists of multiple NLP modules working together to process two versions of regulatory documents and generate explainable amendment reports.

---

# ⚙️ Workflow

## 1. Input Layer

The framework accepts two document versions:

- Previous Version (PDF)
- Updated Version (PDF)

Supported document types include:

- Government regulations
- University rulebooks
- Corporate policies
- Legal documents
- Financial compliance documents
- Standard operating procedures

---

## 2. Document Extraction Module

The extraction engine converts PDF documents into machine-readable text.

### Technologies Used

- PyMuPDF
- pdfplumber
- OCR (optional)

### Features

- Multi-page extraction
- Table extraction
- Poor formatting recovery
- Structured text generation

---

## 3. Text Cleaning & Normalization

Extracted text is standardized before NLP processing.

### Operations

- Regex cleaning
- Whitespace normalization
- Decimal protection
- Sentence reconstruction
- Broken line merging
- Formatting normalization

### Example

Before

```text
Minimum attendance
required is 75 . 0 %
```

After

```text
Minimum attendance required is 75.0%
```

---

## 4. Rule Segmentation

The cleaned document is divided into meaningful rule units.

### Techniques

- Section recognition
- Pattern matching
- Sentence segmentation
- Fragment filtering

### Output Example

```python
[
    "Students must maintain 75% attendance.",
    "Late fee payment attracts penalty.",
    "Project submission deadline is 6 weeks."
]
```

---

# 🧠 Hybrid Classification Engine

One of the key innovations of the patented framework is its hybrid sector classification engine.

The system combines three complementary approaches to maximize classification accuracy.

---

## A. Priority Rule Engine

Critical keywords are assigned predefined categories.

Example:

```python
{
    "misconduct": "Discipline",
    "attendance": "Attendance",
    "fee": "Finance"
}
```

This guarantees highly important regulatory rules are classified correctly.

---

## B. Keyword Scoring Model

Domain-specific keyword dictionaries generate weighted scores for every rule.

The classifier:

- Counts keyword frequency
- Assigns category weights
- Produces confidence scores

---

## C. Semantic Classification using Sentence-BERT

Sentence-BERT (`all-MiniLM-L6-v2`) provides semantic understanding.

Workflow:

- Convert rules into embeddings
- Convert sector descriptions into embeddings
- Compute cosine similarity
- Generate semantic relevance scores

Final Classification:

```
Final Score =
0.4 × Keyword Score +
0.6 × Semantic Score
```

This hybrid methodology significantly improves robustness against paraphrased regulations.

---

# 🔍 Semantic Change Detection

The patented semantic comparison engine detects meaningful modifications between document versions instead of relying on textual differences.

### Methodology

- Generate Sentence-BERT embeddings
- Compute cosine similarity
- Match semantically related rules
- Apply similarity thresholds

### Detected Changes

| Change | Description |
|---------|-------------|
| Added | Rule exists only in new version |
| Deleted | Rule removed from latest version |
| Modified | Same meaning with textual or numerical differences |

### Example

Old Rule

```text
Minimum attendance required is 75%.
```

Updated Rule

```text
Minimum attendance required is 80%.
```

Output

```text
Modified Rule
```

Unlike traditional diff tools, the framework recognizes **semantic amendments** rather than merely textual edits.

---

# 🔢 Numerical Analysis

In addition to semantic understanding, the framework performs quantitative analysis to detect numerical modifications within regulatory documents.

### Supported Numerical Elements

- Percentages
- Currency values
- Durations
- Thresholds
- Numeric limits
- Scores
- Credits

### Example Changes

```text
75%  → 80%
₹1,000 → ₹2,000
6 weeks → 8 weeks
20 Credits → 24 Credits
```

This ensures that critical numerical amendments are explicitly highlighted instead of being treated as ordinary text modifications.

---

# 🎯 Intent Detection

The framework determines the purpose behind every detected amendment using rule-based NLP and contextual analysis.

### Example Intent Categories

- Attendance
- Finance
- Evaluation
- Examination
- Discipline
- Research
- Academic Regulations
- Administration

### Example

Input Rule

```text
Students must pay the fee before the due date.
```

Detected Intent

```text
Finance
```

Intent detection provides contextual understanding that assists administrators in interpreting policy changes.

---

# 🧩 Cause Prediction Engine

One of the distinguishing innovations of the patented framework is the **Cause Prediction Engine**, which estimates the probable reason behind each amendment.

The engine combines:

- Rule-based reasoning
- Intent classification
- Semantic similarity
- Knowledge-base matching

to generate explainable amendment insights.

---

## Working Pipeline

### Step 1 — Input

The engine receives:

- Previous Rule
- Updated Rule
- Intent Label

---

### Step 2 — Intent Mapping

Each amendment is mapped to a predefined intent category.

---

### Step 3 — Knowledge Base

A domain-specific knowledge base associates intents with likely amendment causes.

Example

```python
CAUSE_KB = {
    "Attendance": [
        "Improve discipline",
        "Increase classroom engagement"
    ],
    "Finance": [
        "Operational cost management",
        "Ensure timely payments"
    ]
}
```

---

### Step 4 — Semantic Knowledge Matching

The framework utilizes:

- `cause_dataset.json`
- `cause_embeddings.pt`

generated using Sentence-BERT embeddings.

This enables:

- Context-aware reasoning
- Semantic similarity matching
- Improved prediction accuracy

---

### Step 5 — Cause Prediction

The final prediction combines:

- Intent relevance
- Semantic similarity
- Knowledge-base confidence

to return the most probable causes.

Example

```text
Attendance Increased

Predicted Causes

• Improve discipline
• Increase engagement
```

---

# 📤 Output Generator

The final module compiles every detected amendment into structured machine-readable reports.

The generated output contains:

- Added Rules
- Deleted Rules
- Modified Rules
- Sector Classification
- Numerical Changes
- Intent Labels
- Predicted Causes

---

# 📄 Example JSON Output

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

# 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Programming Language | Python |
| NLP Framework | Sentence-BERT |
| Embedding Model | all-MiniLM-L6-v2 |
| Machine Learning | PyTorch |
| PDF Processing | PyMuPDF, pdfplumber |
| OCR | Tesseract OCR |
| Similarity Metric | Cosine Similarity |
| Data Format | JSON |
| Text Processing | Regular Expressions |

---

# 📂 Project Structure

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
├── assets/
│   └── Architecture.png
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Future Scope

Potential future enhancements include:

- Fine-tuned Legal Language Models (LLMs)
- Multi-language regulatory analysis
- Cloud-based SaaS deployment
- Explainable AI dashboards
- Real-time amendment monitoring
- Enterprise compliance integrations
- Government policy intelligence platform
- REST API deployment
- Interactive visualization dashboards

---

# 📈 Applications

The patented framework can be applied across multiple domains:

- Government regulation tracking
- University academic regulation comparison
- Legal document analysis
- Corporate policy management
- Financial compliance monitoring
- Insurance policy comparison
- Healthcare regulatory analysis
- Contract amendment detection
- Enterprise compliance auditing

---

# 🏆 Novel Contributions

The patented framework introduces several innovations beyond traditional document comparison systems:

- Hybrid NLP-based semantic amendment detection
- Rule-level intelligent comparison
- Domain-aware sector classification
- Explainable intent prediction
- AI-assisted cause prediction
- Numerical amendment analysis
- Structured JSON report generation
- Hybrid rule-based and semantic reasoning architecture

---

# 📚 Research Significance

This work demonstrates the application of modern Natural Language Processing techniques to automate regulatory document analysis.

Unlike traditional text-difference approaches, the framework understands the **meaning** behind amendments, making it suitable for real-world compliance, governance, and legal intelligence applications.

---

# 🤝 Contributing

Contributions are welcome.

Possible contribution areas include:

- Improving NLP accuracy
- Adding additional regulatory domains
- Fine-tuning transformer models
- Optimizing semantic matching
- Developing web dashboards
- API integrations
- Performance optimization
- Cloud deployment

Please open an Issue or Pull Request for proposed improvements.

---

# 📜 Patent Citation

If you use this work in academic research or industrial projects, please cite the published patent:

**Tanishq Daga.**  
*System and Method for Amendment Detection and Analysis for Regulatory Documents.*  
**Published Indian Patent Application**  
Application No. **202641076170**  
India, 2026.

---

# 👨‍💻 Author

**Tanishq Daga**

Computer Science Engineering Student | Full Stack Developer | NLP Researcher

This repository contains the implementation of the methodology presented in the **Published Indian Patent Application**:

**System and Method for Amendment Detection and Analysis for Regulatory Documents**

**Application No.: 202641076170**

The project demonstrates an AI-driven framework for semantic amendment detection, explainable document analysis, intent recognition, numerical comparison, and cause prediction in regulatory documents.

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

If this work contributes to your research or development, please cite the published patent and acknowledge the repository.
