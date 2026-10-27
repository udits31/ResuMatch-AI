-- ResuMatch AI — Supabase (PostgreSQL) schema
-- Run this ONCE in the Supabase dashboard → SQL Editor, then run insert_data.sql.
-- Note: Supabase gives you one database per project, so there is no CREATE DATABASE / USE here.

-- ---------------------------------------------------------------------------
-- Table: resumes  — stores resume information for HR matching
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS resumes (
    resume_id        SERIAL PRIMARY KEY,
    resume_title     VARCHAR(255) NOT NULL,
    resume_text      TEXT NOT NULL,
    candidate_name   VARCHAR(255) NOT NULL,
    candidate_email  VARCHAR(255),
    candidate_phone  VARCHAR(50),
    experience_years INT,
    current_position VARCHAR(255),
    location         VARCHAR(255),
    uploaded_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resume_title     ON resumes (resume_title);
CREATE INDEX IF NOT EXISTS idx_candidate_name   ON resumes (candidate_name);
CREATE INDEX IF NOT EXISTS idx_experience_years ON resumes (experience_years);
CREATE INDEX IF NOT EXISTS idx_uploaded_at      ON resumes (uploaded_at);

-- ---------------------------------------------------------------------------
-- Table: job_descriptions  — stores job descriptions for HR matching
-- (MySQL ENUMs become VARCHAR + CHECK constraints in PostgreSQL)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_descriptions (
    job_id               SERIAL PRIMARY KEY,
    job_title            VARCHAR(255) NOT NULL,
    job_description_text TEXT NOT NULL,
    company_name         VARCHAR(255) NOT NULL,
    department           VARCHAR(255),
    employment_type      VARCHAR(20) DEFAULT 'full-time'
                             CHECK (employment_type IN ('full-time', 'part-time', 'contract', 'internship')),
    experience_required  VARCHAR(100),
    salary_range         VARCHAR(100),
    location             VARCHAR(255),
    posted_by            VARCHAR(255),
    posted_at            TIMESTAMPTZ DEFAULT NOW(),
    updated_at           TIMESTAMPTZ DEFAULT NOW(),
    status               VARCHAR(10) DEFAULT 'active'
                             CHECK (status IN ('active', 'closed', 'draft'))
);

CREATE INDEX IF NOT EXISTS idx_job_title    ON job_descriptions (job_title);
CREATE INDEX IF NOT EXISTS idx_company_name ON job_descriptions (company_name);
CREATE INDEX IF NOT EXISTS idx_department   ON job_descriptions (department);
CREATE INDEX IF NOT EXISTS idx_status       ON job_descriptions (status);
CREATE INDEX IF NOT EXISTS idx_posted_at    ON job_descriptions (posted_at);

-- ---------------------------------------------------------------------------
-- Table: resume_matches  — stores matching results between resumes and jobs
-- (MySQL JSON becomes JSONB in PostgreSQL)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS resume_matches (
    match_id               SERIAL PRIMARY KEY,
    resume_id              INT NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
    job_id                 INT NOT NULL REFERENCES job_descriptions(job_id) ON DELETE CASCADE,
    match_score            DECIMAL(5,2) NOT NULL,
    skill_match_percentage DECIMAL(5,2),
    matching_skills        JSONB,
    missing_skills         JSONB,
    resume_skills          JSONB,
    job_skills             JSONB,
    matched_at             TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_match UNIQUE (resume_id, job_id)
);

CREATE INDEX IF NOT EXISTS idx_resume_id   ON resume_matches (resume_id);
CREATE INDEX IF NOT EXISTS idx_job_id      ON resume_matches (job_id);
CREATE INDEX IF NOT EXISTS idx_match_score ON resume_matches (match_score);
CREATE INDEX IF NOT EXISTS idx_matched_at  ON resume_matches (matched_at);

-- ---------------------------------------------------------------------------
-- Keep updated_at current on UPDATE (PostgreSQL has no "ON UPDATE" clause,
-- so we use a trigger — this replaces MySQL's ON UPDATE CURRENT_TIMESTAMP).
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_resumes_updated_at ON resumes;
CREATE TRIGGER trg_resumes_updated_at
    BEFORE UPDATE ON resumes
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_jobs_updated_at ON job_descriptions;
CREATE TRIGGER trg_jobs_updated_at
    BEFORE UPDATE ON job_descriptions
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------------------
-- Table: profiles  — job-seeker profiles (multiple named profiles).
-- The whole profile is stored as JSONB so the schema can grow without DDL.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profiles (
    profile_id   SERIAL PRIMARY KEY,
    profile_name VARCHAR(255) UNIQUE NOT NULL,
    data         JSONB NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_profiles_updated_at ON profiles (updated_at);

DROP TRIGGER IF EXISTS trg_profiles_updated_at ON profiles;
CREATE TRIGGER trg_profiles_updated_at
    BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
