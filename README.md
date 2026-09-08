# JobGuard AI

**AI-Powered Job Intelligence, Resume Matching & Scam Detection**

JobGuard AI is a project focused on helping job seekers understand whether a job is suitable for their resume and whether a job posting contains suspicious indicators.

The project currently focuses on three main areas:

* Resume Parsing
* Resume–Job Matching
* Job Scam Detection

## How it works

```text
Resume + Job Description
          |
          v
    Resume Analysis
          |
    +-----+-----+
    |           |
    v           v
Job Matching   Scam Detection
    |           |
    v           v
Match Score   Risk Analysis
    |
    v
 Skill Gap
```

## Resume Matching

The resume matching module uses NLP and Sentence Transformers to compare the resume with a job description.

Currently, the prototype uses:

* Sentence Transformers
* `all-MiniLM-L6-v2`
* Cosine Similarity
* Skill Matching
* Semantic Similarity

The current prototype combines semantic similarity and skill matching:

```text
Final Score = 70% Semantic Score + 30% Skill Score
```

It also shows:

* Matching Skills
* Missing Skills
* Overall Match Score

For example, if a job requires:

```text
Python, SQL, Git, Docker, AWS
```

and the resume contains:

```text
Python, SQL, Git, Pandas
```

the system can identify:

```text
Matching Skills: Python, SQL, Git
Missing Skills: Docker, AWS
```

## Resume Parser

The resume parser is being developed to extract useful information from resumes.

The current implementation includes Python, `pdfplumber` and Regex-based text processing.

Planned parser capabilities include:

* PDF and DOCX support
* Text extraction
* Section identification
* Skill extraction
* Structured resume data

## Job Scam Detection

The Fake Job Detector currently uses a rule-based approach.

It checks for indicators commonly found in suspicious job postings, such as:

* Registration or processing fees
* Security deposits
* Guaranteed job claims
* No-interview offers
* WhatsApp/Telegram-only contact
* UPI/payment requests
* Urgency-based messages
* Unrealistic earning claims

The detector generates a risk score and classifies the posting as:

```text
Low Risk
Medium Risk
High Risk
```

It also returns the reasons for the detected indicators.

The system is intended for **risk assessment**, not for declaring a job definitively fake based only on keywords.

## Tech Stack

### Current

**Language**

* Python

**AI / NLP**

* Sentence Transformers
* `all-MiniLM-L6-v2`
* Cosine Similarity
* NLP / Text Processing

**Resume Processing**

* pdfplumber
* Regex

**Scam Detection**

* Regex
* Keyword Matching
* Rule-Based Risk Scoring

**Tools**

* Google Colab
* Jupyter Notebook
* VS Code
* Git
* GitHub

### Planned

* React + JavaScript
* FastAPI
* SQLite

## Project Structure

```text
JobGuard-AI/
│
├── backend/
│   ├── fake_job_detector.py
│   ├── resume_matcher.py
│   ├── resume_parser.py
│   ├── main.py
│   ├── requirements.txt
│   └── Member3_Resume_Matching.ipynb
│
├── data/
│   └── sample_data.txt
│
├── Resume Preseure/
│   └── resume.py
│
├── .gitignore
└── README.md
```

The structure will be updated as the project modules are completed and integrated.

## Team

**Vivek Sharma** — Project Lead
**Shubhangi Singh Rajput** — Job Scam Detection
**Ananya Awasthi** — Resume Matching & AI
**Vinay Prajapati** — Resume Parsing
**Ishita Awasthi** — Resume Parsing
**Sunanya Goswami** — Frontend Development

## Future Work

* Complete the resume parser
* Prepare the job dataset
* Finalize the resume matching module
* Improve scam detection rules
* Develop the React frontend
* Build FastAPI APIs
* Connect all modules
* Perform end-to-end testing
* Deploy the application

## Project Goal

The goal of JobGuard AI is to give job seekers a simple way to understand:

**How well does my resume match this job, which skills am I missing, and does the job posting contain suspicious signs?**

---

**Project:** JobGuard AI
**Purpose:** Academic / Educational Project
