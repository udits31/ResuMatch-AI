# Unified Resume Platform

A comprehensive AI-powered resume management platform with two main components:
1. **HR Dashboard** - Resume-job matching and analysis
2. **Job Seeker Tools** - Profile management, job analysis, and resume generation

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure the database (Supabase / PostgreSQL)
# 1. Create a free project at https://supabase.com
# 2. In the Supabase SQL Editor, run supabase_schema.sql then insert_data.sql
# 3. Copy .env.example to .env and paste your Supabase connection string

# Start application
python app.py
```

Visit: http://localhost:5000

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