# Unified Resume Platform

A comprehensive AI-powered resume management platform with two main components:
1. **HR Dashboard** - Resume-job matching and analysis
2. **Job Seeker Tools** - Profile management, job analysis, and resume generation

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download the spaCy English model (one-time, needed for skill extraction)
python -m spacy download en_core_web_sm

# Configure the database (Supabase / PostgreSQL)
# 1. Create a free project at https://supabase.com
# 2. In the Supabase SQL Editor, run supabase_schema.sql then insert_data.sql
# 3. Copy .env.example to .env and paste your Supabase connection string

# Start application
python app.py
```

Visit: http://localhost:5000

> **Python 3.13 note:** if `pip install` tries to build spaCy/numpy from source and fails,
> install prebuilt wheels instead: `pip install --only-binary=:all: spacy==3.8.16`
>
> The sentence-transformers model (`all-MiniLM-L6-v2`, ~80 MB) downloads automatically on
> the first match, and NLTK data downloads automatically on first run — both need internet once.

## 📁 Project Structure

Clean, organized structure with backend models, integrations, database layer, and frontend assets.

## 🎯 Features

### HR Dashboard
- ✅ Resume-job matching with AI analysis
- ✅ Skill gap identification
- ✅ Database-driven sample data
- ✅ Professional scoring system

### Job Seeker Tools
- ✅ Profile management (personal info, experience, education, skills)
- ✅ Job description analysis (keywords, requirements extraction)
- ✅ Tailored resume generation
- ✅ Multi-format export (PDF, Word, Text)

## 🔧 Configuration

The app connects to a **Supabase (PostgreSQL)** database using a connection string
stored in a `.env` file (never committed to git).

1. Copy `.env.example` to `.env`
2. In Supabase: **Settings → Database → Connection string → URI** (port 5432)
3. Paste it into `.env`, filling in your database password:

```bash
SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
```

## 🧠 Matching Engine (NLP)

Resume–job matching combines two NLP signals into one score
(`30% document similarity + 70% skill overlap`):

- **Semantic similarity** — the resume and job description are encoded with
  sentence-embeddings (`all-MiniLM-L6-v2`) and compared with cosine similarity.
  This captures *meaning*, so "built REST APIs" matches "API development" even
  with no shared words. The original **TF-IDF** (keyword) score is kept as a
  baseline, and both are shown side by side in the HR dashboard.
- **Skill extraction** — skills are pulled from text with spaCy's `PhraseMatcher`
  over a curated, categorized taxonomy with synonym handling, so "ML" ↔
  "machine learning", "k8s" ↔ "kubernetes" and "containerization" → Docker all
  resolve to one canonical skill. Falls back to regex if spaCy is unavailable.

If the semantic model or spaCy model is missing, the engine degrades gracefully
(TF-IDF only / regex skills) rather than failing.

## 📋 User Flow

### Job Seekers
1. Fill profile details (personal info, experience, education, skills)
2. Enter job description for analysis
3. Generate tailored resume based on job requirements
4. Export resume as PDF, Word, or Text file

### HR Users
1. Select resume and job description from database
2. Run AI-powered matching analysis
3. View compatibility scores and skill gaps
4. Make informed hiring decisions

## 🛠 Dependencies

See requirements.txt for all dependencies.

## 📊 Database

Supabase (PostgreSQL) database with resumes, job descriptions, and matching tables. Profile data stored in JSON.