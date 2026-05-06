create extension if not exists pgcrypto;

create table if not exists users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    created_at timestamptz not null default now()
);

create table if not exists resumes (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    content jsonb not null,
    raw_text text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_resumes_user_created_at
    on resumes (user_id, created_at desc);

create table if not exists jobs (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    company text not null,
    location text,
    description text not null,
    source text not null,
    url text not null,
    posted_at timestamptz,
    created_at timestamptz not null default now(),
    unique (source, url)
);

create index if not exists idx_jobs_posted_at
    on jobs (posted_at desc);

create table if not exists job_matches (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    job_id uuid not null references jobs(id) on delete cascade,
    match_score double precision not null check (match_score >= 0 and match_score <= 1),
    explanation jsonb not null,
    created_at timestamptz not null default now(),
    unique (user_id, job_id)
);

create index if not exists idx_job_matches_user_score_created_at
    on job_matches (user_id, match_score desc, created_at desc);

create table if not exists resume_versions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    job_id uuid not null references jobs(id) on delete cascade,
    content jsonb not null,
    rationale text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_resume_versions_user_created_at
    on resume_versions (user_id, created_at desc);

create table if not exists agent_runs (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    type text not null,
    input jsonb not null default '{}'::jsonb,
    output jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_agent_runs_user_created_at
    on agent_runs (user_id, created_at desc);
