# Job-to-Candidate Alignment Engine PRD (MVP)

## Product Positioning

This product is not a job finder. It is a **job-to-candidate alignment engine** that helps users:

1. understand fit for a specific role,
2. identify missing skills clearly, and
3. create a truthful job-specific resume version.

## Problem

Users apply to jobs with a single static resume and receive low response rates. They need:

- realistic match feedback per role,
- specific gap analysis, and
- safe optimization that does not invent experience.

## Primary Users

- Individual professionals actively applying to jobs.
- Typical range: early-career to mid-career candidates.

## MVP Goals

1. Store user resume and version history.
2. Ingest and normalize jobs into a unified schema.
3. Produce match score and explanation for a user-job pair.
4. Generate tailored resume versions with strict truthfulness constraints.
5. Trigger and observe end-to-end agent runs.

## Non-Goals (MVP)

- Advanced ATS connectors with deep customization.
- Multi-channel notifications beyond email.
- Full recommendation feed ranking system.

## Core User Stories

1. As a user, I can upload my source resume and retrieve it later.
2. As a user, I can see normalized jobs to evaluate.
3. As a user, I can run a match and receive:
   - score (0-1),
   - overlap skills,
   - missing skills,
   - realistic reasoning.
4. As a user, I can request a job-specific resume version.
5. As an operator, I can trigger agent runs manually or by cron and inspect logs.

## Functional Requirements

### Data Layer

- `users`: account identity.
- `resumes`: source resume store (no overwrite requirement handled through separate versions table).
- `jobs`: normalized job posting records.
- `job_matches`: user-job scoring and explanation.
- `resume_versions`: job-specific tailored resume outputs.
- `agent_runs`: audit trail for every agent execution.

### API Surface

- `POST /resume/upload`
- `GET /resume/{user_id}`
- `POST /jobs/ingest`
- `GET /jobs?user_id=`
- `POST /match/run`
- `POST /resume/optimize`
- `POST /agent/run`

### Agent Logic

Pipeline:

1. Fetch jobs
2. Normalize job
3. Match resume and job
4. Decision (`score > threshold`)
5. Resume optimization
6. Store resume version
7. Notify user

## Constraints and Policy

Resume optimization must obey:

- No invented experience.
- Only reframe existing content, reorder sections, and highlight relevant keywords.
- Keep claims evidence-backed by source resume content.

## Success Metrics (MVP)

- Match run completion rate.
- Percentage of matches above threshold that produce resume versions.
- User adoption of generated resume versions.
- Quality guardrail: zero known policy violations for invented experience.

## Risks and Mitigations

- **Risk:** Hallucinated claims in optimized resume.  
  **Mitigation:** policy prompts, post-generation validation, structured rationale storage.
- **Risk:** Noisy job data reduces match quality.  
  **Mitigation:** normalize schema and deduplicate on `(source, url)`.
- **Risk:** Score quality drift.  
  **Mitigation:** store explanations and review calibration samples regularly.
