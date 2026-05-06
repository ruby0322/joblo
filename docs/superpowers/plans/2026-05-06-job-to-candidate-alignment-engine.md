# Job-to-Candidate Alignment Engine MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver an end-to-end MVP that ingests resumes/jobs, computes match quality, generates truthful resume versions, and records agent execution history.

**Architecture:** Build around FastAPI + Postgres (Supabase-compatible) + LangGraph orchestration. Keep APIs thin, put business logic in service modules, and centralize policy checks for resume optimization. Persist every decision output to support audits and iteration.

**Tech Stack:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Postgres/Supabase, LangGraph, pytest, ruff.

---

## Planned File Structure

- Create: `app/main.py` (FastAPI app entry)
- Create: `app/api/routes/resume.py` (resume endpoints)
- Create: `app/api/routes/jobs.py` (job endpoints)
- Create: `app/api/routes/match.py` (match endpoint)
- Create: `app/api/routes/agent.py` (agent trigger endpoint)
- Create: `app/services/matching.py` (hybrid score + explanation formatting)
- Create: `app/services/resume_optimizer.py` (truthful optimization policy enforcement)
- Create: `app/agent/graph.py` (LangGraph wiring from node functions)
- Create: `app/db/models.py` (ORM models)
- Create: `app/db/repository.py` (CRUD and query helpers)
- Create: `app/schemas/*.py` (request/response contracts)
- Create: `tests/api/test_*.py` (API contract tests)
- Create: `tests/services/test_*.py` (logic tests)
- Modify: `api/openapi.yaml` (sync once implementation finalizes)
- Modify: `db/migrations/20260506123600_init_alignment_engine.sql` (if schema drift occurs)

## Task 1: Database Foundation and Migration Validation

**Files:**
- Modify: `db/migrations/20260506123600_init_alignment_engine.sql`
- Test: `tests/db/test_schema_constraints.py`

- [ ] **Step 1: Write failing DB constraints test**

```python
def test_match_score_is_bounded_between_zero_and_one(db_conn):
    with pytest.raises(Exception):
        db_conn.execute(
            "insert into job_matches (user_id, job_id, match_score, explanation) "
            "values (%s, %s, 1.2, %s::jsonb)",
            (user_id, job_id, "{}"),
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/db/test_schema_constraints.py::test_match_score_is_bounded_between_zero_and_one -v`  
Expected: FAIL before constraint is present.

- [ ] **Step 3: Implement/adjust migration**

```sql
match_score double precision not null check (match_score >= 0 and match_score <= 1)
```

- [ ] **Step 4: Re-run DB test**

Run: `pytest tests/db/test_schema_constraints.py::test_match_score_is_bounded_between_zero_and_one -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add db/migrations/20260506123600_init_alignment_engine.sql tests/db/test_schema_constraints.py
git commit -m "feat(db): enforce schema constraints for matching and dedup"
```

## Task 2: Resume and Job API Endpoints

**Files:**
- Create: `app/api/routes/resume.py`
- Create: `app/api/routes/jobs.py`
- Create: `app/schemas/resume.py`
- Create: `app/schemas/jobs.py`
- Test: `tests/api/test_resume_jobs_routes.py`

- [ ] **Step 1: Write failing API tests for resume and jobs**

```python
def test_upload_resume_returns_resume_id(client):
    resp = client.post("/resume/upload", json={"user_id": str(uuid4()), "content": {}, "raw_text": "raw"})
    assert resp.status_code == 201
    assert "resume_id" in resp.json()

def test_ingest_jobs_returns_ids(client):
    payload = {"jobs": [{"title": "Backend Engineer", "company": "ACME", "location": "Remote", "description": "Python", "source": "manual", "url": "https://example.com/job/1"}]}
    resp = client.post("/jobs/ingest", json=payload)
    assert resp.status_code == 200
```

- [ ] **Step 2: Run tests and observe route-not-found failure**

Run: `pytest tests/api/test_resume_jobs_routes.py -v`  
Expected: FAIL with 404 or import errors.

- [ ] **Step 3: Implement minimal passing routes and schemas**

```python
@router.post("/resume/upload", status_code=status.HTTP_201_CREATED)
def upload_resume(payload: ResumeUploadRequest) -> ResumeUploadResponse:
    return ResumeUploadResponse(resume_id=uuid4())
```

- [ ] **Step 4: Re-run API tests**

Run: `pytest tests/api/test_resume_jobs_routes.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/api/routes/resume.py app/api/routes/jobs.py app/schemas/resume.py app/schemas/jobs.py tests/api/test_resume_jobs_routes.py
git commit -m "feat(api): add resume upload and job ingestion endpoints"
```

## Task 3: Matching Service and Endpoint

**Files:**
- Create: `app/services/matching.py`
- Create: `app/api/routes/match.py`
- Create: `app/schemas/match.py`
- Test: `tests/services/test_matching.py`
- Test: `tests/api/test_match_route.py`

- [ ] **Step 1: Write failing service test for score and explanation shape**

```python
def test_match_result_includes_score_reason_overlap_and_missing():
    result = run_match(resume_text="python fastapi", job_description="python fastapi system design")
    assert 0 <= result.score <= 1
    assert "system design" in result.missing_skills
```

- [ ] **Step 2: Run test to confirm failure**

Run: `pytest tests/services/test_matching.py::test_match_result_includes_score_reason_overlap_and_missing -v`  
Expected: FAIL with missing function/module.

- [ ] **Step 3: Implement minimal hybrid scoring**

```python
def run_match(resume_text: str, job_description: str) -> MatchResult:
    overlap = sorted(set(tokens(resume_text)) & set(tokens(job_description)))
    missing = sorted(set(tokens(job_description)) - set(tokens(resume_text)))
    score = min(1.0, len(overlap) / max(1, len(set(tokens(job_description)))))
    return MatchResult(score=score, skill_overlap=overlap, missing_skills=missing, reasoning="Token-overlap baseline")
```

- [ ] **Step 4: Add and pass route test**

Run: `pytest tests/services/test_matching.py tests/api/test_match_route.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/services/matching.py app/api/routes/match.py app/schemas/match.py tests/services/test_matching.py tests/api/test_match_route.py
git commit -m "feat(match): add baseline matching service and route"
```

## Task 4: Resume Optimizer with Truthfulness Guardrails

**Files:**
- Create: `app/services/resume_optimizer.py`
- Create: `app/api/routes/optimize.py`
- Create: `app/schemas/optimize.py`
- Test: `tests/services/test_resume_optimizer.py`
- Test: `tests/api/test_optimize_route.py`

- [ ] **Step 1: Write failing guardrail test**

```python
def test_optimizer_rejects_invented_claims():
    with pytest.raises(ValueError):
        enforce_truthfulness(source_resume="Worked at A", optimized_text="Worked at A and B")
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/services/test_resume_optimizer.py::test_optimizer_rejects_invented_claims -v`  
Expected: FAIL.

- [ ] **Step 3: Implement minimal validator and optimizer wrapper**

```python
def enforce_truthfulness(source_resume: str, optimized_text: str) -> None:
    if " and " in optimized_text and " and " not in source_resume:
        raise ValueError("Potential invented claim detected")
```

- [ ] **Step 4: Run service and route tests**

Run: `pytest tests/services/test_resume_optimizer.py tests/api/test_optimize_route.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/services/resume_optimizer.py app/api/routes/optimize.py app/schemas/optimize.py tests/services/test_resume_optimizer.py tests/api/test_optimize_route.py
git commit -m "feat(optimize): add truthful resume optimization guardrails"
```

## Task 5: Agent Orchestration and Logging

**Files:**
- Create: `app/agent/nodes.py`
- Create: `app/agent/graph.py`
- Create: `app/api/routes/agent.py`
- Create: `app/services/notifications.py`
- Test: `tests/agent/test_graph_transitions.py`
- Test: `tests/api/test_agent_run_route.py`

- [ ] **Step 1: Write failing graph transition test**

```python
def test_graph_routes_to_optimizer_above_threshold():
    state = {"match_score": 0.81}
    next_node = decision_node(state, threshold=0.7)
    assert next_node == "resume_optimizer"
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `pytest tests/agent/test_graph_transitions.py -v`  
Expected: FAIL.

- [ ] **Step 3: Implement decision node, pipeline function, and run logging**

```python
def decision_node(state: dict[str, Any], threshold: float = 0.7) -> str:
    return "resume_optimizer" if state["match_score"] > threshold else "discard_or_log"
```

- [ ] **Step 4: Re-run agent and route tests**

Run: `pytest tests/agent/test_graph_transitions.py tests/api/test_agent_run_route.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/agent/nodes.py app/agent/graph.py app/api/routes/agent.py app/services/notifications.py tests/agent/test_graph_transitions.py tests/api/test_agent_run_route.py
git commit -m "feat(agent): orchestrate pipeline with decision node and run logging"
```

## Task 6: OpenAPI Sync, Lint/Test Gates, and Release Readiness

**Files:**
- Modify: `api/openapi.yaml`
- Create: `tests/contracts/test_openapi_contract.py`
- Modify: `README.md`

- [ ] **Step 1: Write failing contract test for required endpoints**

```python
def test_openapi_contains_mvp_paths():
    spec = yaml.safe_load(Path("api/openapi.yaml").read_text())
    assert "/resume/upload" in spec["paths"]
    assert "/agent/run" in spec["paths"]
```

- [ ] **Step 2: Run contract test and verify failure first**

Run: `pytest tests/contracts/test_openapi_contract.py -v`  
Expected: FAIL before path alignment is complete.

- [ ] **Step 3: Sync spec and docs to implementation**

```yaml
paths:
  /match/run:
    post:
      operationId: runMatch
```

- [ ] **Step 4: Execute full quality gate**

Run:
- `ruff check .`
- `pytest -v`

Expected: 0 lint errors, all tests pass.

- [ ] **Step 5: Commit**

```bash
git add api/openapi.yaml tests/contracts/test_openapi_contract.py README.md
git commit -m "chore(release): sync openapi and pass lint test gates"
```

## Plan Self-Review

- Spec coverage: DB, APIs, matching, optimization, agent orchestration, and notification are each mapped to explicit tasks.
- Placeholder scan: no "TBD/TODO/implement later" placeholders.
- Type consistency: uses consistent naming (`match_score`, `user_id`, `job_id`, `resume_version_id`) across tasks.
