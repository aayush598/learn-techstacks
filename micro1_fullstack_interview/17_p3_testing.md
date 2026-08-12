# Priority 3 — Testing (Q448–Q465)

**Why these matter for micro1:** the coding exercise + behavioral rounds probe whether you write tests like a professional. Expect pytest, FastAPI `TestClient`, async tests, mocking LLM calls, and React testing questions.

---

## Q448: Why do we test? What are the main test types?

**Why:** catch regressions, document behavior, enable safe refactoring, speed up development (fail fast), and prevent production incidents. Tests are *specifications that run*.

**Main types:**
- **Unit tests** — one function/class in isolation (deps mocked). Fast, hundreds/thousands, run every commit.
- **Integration tests** — real components together: DB + repository, API + real DB, queue + worker. Slower, fewer.
- **E2E tests** — the full user journey through the real UI (Playwright/Cypress). Slowest, fewest, most brittle.
- **Contract tests** — API/provider contract checks between services.
- **Load/perf tests** — is it fast enough under load (Q243).

**The pyramid:** many fast unit tests at the bottom → fewer integration → fewest E2E at the top. If your E2E suite is your primary safety net, you're testing too late.

---

## Q449: How do pytest fixtures work?

**Fixtures** provide setup/teardown and reusable objects; they're *injected by function argument name*.

```python
import pytest
from app.db import get_session

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL)      # fresh test DB
    yield engine.connect()                         # the test runs here
    engine.dispose()                               # teardown

def test_save_application(db_session):             # fixture injected by name
    row = insert_application(db_session, ...)
    assert row.status == "submitted"
```

**Scope ladder** (run once, reused): `function` (default) < `class` < `module` < `session`. Use session-scoped fixtures for the *expensive* things (test DB, LLM stub client) and function-scoped for *isolation* (fresh data).

**Conftest:** `conftest.py` holds shared fixtures so every test file gets them without imports.

---

## Q450: Unit vs integration vs E2E — where's the line?

**Unit:** `score_candidate()` with a fake LLM + fake DB. Tests *logic* in isolation. No I/O.
**Integration:** FastAPI `TestClient` against a **real Postgres** (Testcontainers) — does the endpoint + repository + schema actually work together? Catches SQL errors, serialization mismatches, transaction bugs.
**E2E:** Playwright — candidate uploads a resume, applies, sees the AI chat reply. Verifies the *user journey* across backend + frontend.

**Rule of thumb:** unit tests answer "is the logic right?", integration "do the parts fit?", E2E "can a user complete the flow?". Every bug you can catch in a cheaper layer, catch there.

---

## Q451: How do you mock in Python? (mock, patch, monkeypatch)

**Mock:** replace a dependency with a controllable fake object.

```python
from unittest.mock import Mock, patch

@patch("app.services.screening.call_llm")          # patch by import path
def test_score_returns_recommendation(mock_llm):
    mock_llm.return_value = {"score": 0.9, "summary": "Strong fit"}
    result = score_candidate("job_1", "cand_2")
    assert result["recommendation"] == "advance"
    mock_llm.assert_called_once()                  # assert the call happened
```

- **`mock.return_value`** — fixed return; **`mock.side_effect`** — raise or yield a sequence.
- **`assert_called_with` / `assert_any_call`** — verify exact inputs (great for "did we send the right prompt?").
- **`patch` targets the import path** where it's *used* (`app.services.screening.call_llm`), not where it's defined.
- **pytest `monkeypatch`** — lighter-weight: set/delete attributes, env vars, dict entries; auto-undo after the test.
- **`respx` / `httpx.MockTransport`** — mock outgoing HTTP for async clients.

**Rule:** mock at the **boundary** (the external call), not internals — otherwise tests validate your mocks, not your code.

---

## Q452: How do you test FastAPI endpoints?

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_apply_creates_application():
    r = client.post("/api/v1/applications",
                    json={"job_id": "job_1", "candidate_id": "cand_1"},
                    headers={"Authorization": "Bearer test-token"})
    assert r.status_code == 201
    assert r.json()["status"] == "submitted"
```

**Tips:**
- **Override dependencies** (`app.dependency_overrides[get_current_user]`) to inject a fake user instead of real auth (Q60).
- **Use a test DB** — point the session dependency at a test database, not prod.
- Test the **error paths**: 400/401/404/409/422 shapes (Q392).
- `TestClient` runs sync against the ASGI app (it drives the event loop for you); for true async, use `httpx.AsyncClient(transport=ASGITransport(app))` with pytest-asyncio.

---

## Q453: How do you test async code?

**pytest-asyncio:**
```python
import pytest

@pytest.mark.asyncio
async def test_fetch_candidate(client):
    data = await client.get(f"/candidates/{id}")
    assert data is not None

@pytest.fixture
def event_loop():  # scope per test for isolation
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
```

**Async pitfalls:**
- Don't call `asyncio.run()` inside tests (nested loop errors) — use the `@pytest.mark.asyncio` decorator and pytest's loop.
- **Mock async functions** with `AsyncMock` (or `Mock` with `side_effect=AsyncMock(...)`).
- Assert the coroutine is awaited — forgetting `await` is the classic silent bug.
- **anyio** (modern FastAPI) lets the same test run on asyncio *and* trio via `@pytest.mark.anyio`.

---

## Q454: How do you test database code?

**Options (best → worst):**
1. **Testcontainers** — spin up a real Postgres in Docker per test run (or per session). Closest to prod (real SQL semantics, indexes, constraints). Slower, needs Docker.
2. **Transaction rollback pattern** — begin a transaction in the fixture, run the test inside it, rollback at the end → each test sees clean state without recreating the schema.
3. **SQLite in-memory** — fast, but **not a Postgres** (JSONB, arrays, FTS, and some SQL differ) → dangerous false confidence. Use only for trivial logic.

```python
@pytest.fixture
def db(db_engine):                       # session-scoped, once
    with db_engine.begin() as conn:
        schema.create_all(conn)          # build once
    yield db_engine

@pytest.fixture
def session(db):                         # function-scoped
    conn = db.connect()
    trans = conn.begin()
    try:
        yield conn
    finally:
        trans.rollback()                 # isolation for free
        conn.close()
```

**Factories vs fixtures:** use factories (or `factory_boy`) for common entities (job, candidate) — less duplication, easy variations.

---

## Q455: How do you keep tests isolated and deterministic?

1. **Fresh state per test:** transaction-rollback or truncate tables between tests; never depend on test *order*.
2. **Randomness/time:** freeze time (`freezegun`), seed random/`faker`, inject clocks — tests must be reproducible.
3. **No shared mutable globals:** reset singletons/connection pools/caches between tests.
4. **Isolated resources:** each test run gets its own DB, its own S3 bucket prefix, its own Redis keyspace (prefix by run id).
5. **Parallelize safely:** pytest-xdist works when each worker has its own DB/schema.
6. **One assertion idea per test** where practical — failures are easier to localize.
7. **No sleeps/flakiness:** prefer deterministic waiting (poll with timeout) over `time.sleep(2)`.

---

## Q456: How do you test AI/LLM features?

**You never call the real LLM in tests** — it's slow, costs money, and is non-deterministic. Test *your logic* with a deterministic fake:

1. **Stub the client boundary:**
```python
@pytest.fixture
def fake_llm(monkeypatch):
    async def fake_completion(messages, **kw):
        return ChatResponse(content="Test summary", usage=Usage(100, 50))
    monkeypatch.setattr(llm_client, "complete", fake_completion)
```

2. **Golden/snapshot tests:** freeze the output for a known resume+job; assert exact structure (score, rubric fields) — catch schema regressions.
3. **Schema/validation tests:** feed a realistic (sanitized) resume text; assert the Pydantic output model parses and required fields are present.
4. **Prompt contract tests:** assert the prompt sent to the LLM contains required sections and **no PII leaks** (email/phone stripped) — this is a security test.
5. **Retry/fallback tests:** fake provider raising 429/timeout → assert retry + fallback path fires (Q438, Q398).
6. **Cost guard:** assert token caps are respected (e.g., truncated context never exceeds max_tokens).
7. **Determinism trick:** for tests, inject temperature=0 and a fixed seed where the API allows — but still don't call the real provider.

---

## Q457: What is parametrization in pytest?

Run the same test over many inputs without copying code:

```python
import pytest

@pytest.mark.parametrize("job_req, resume_skills, expected", [
    (["python", "sql"],  ["python", "sql", "react"], True),
    (["kubernetes"],     ["python", "sql"],           False),
    ([],                 [],                          True),
])
def test_skill_overlap(job_req, resume_skills, expected):
    assert has_required_skills(job_req, resume_skills) == expected
```

- Each row is a separate test in the report (failures pinpoint the exact case).
- Add **edge cases as rows**: empty lists, None, long strings, unicode (resumes have all of these!).
- Use `pytest.mark.parametrize("flag", [True, False])` to test code paths both ways.

---

## Q458: What is test coverage? What's a good target?

**Coverage** = % of lines/branches executed by the test suite (`pytest --cov --cov-report=term-missing`).

- **Good target:** ~80% line coverage, with the critical logic (scoring, auth, idempotency, money paths) at 100% branch coverage. Coverage below 70% is usually a red flag; above 90% often means diminishing returns.
- **Coverage is a floor, not a goal** — 100% coverage of the wrong tests (mocked-to-death) proves nothing. The *risk* is what matters: untested error paths, race conditions, and payment/LLM-call branches are the dangerous gaps.
- Gate the CI on coverage *dropping below* a baseline (trend), not on an absolute number.
- Measure **branch coverage** for conditionals, not just lines.

---

## Q459: What is TDD? When is it worth it?

**Test-Driven Development:** red → green → refactor. Write a failing test for the behavior you want, watch it fail (proves the test can fail!), write the minimal code to pass, then refactor.

- **Worth it:** new features with clear behavior, bug fixes (write a regression test that reproduces the bug first), tricky logic (scoring, idempotency, locking), anything with security implications.
- **Less valuable:** throwaway scripts, exploratory prototypes, UI tweaks.
- **Best practice in the real world:** *test-first for bugs and core logic; test-after (but promptly) for peripheral code* — the discipline is having tests, not the exact ordering.

---

## Q460: How do you test React components?

**Vitest/Jest + React Testing Library:**
```jsx
import { render, screen, fireEvent } from "@testing-library/react";
import { CandidateCard } from "./CandidateCard";

test("shows match score and fires shortlist", () => {
  const onShortlist = vi.fn();
  render(<CandidateCard score={0.87} onShortlist={onShortlist} />);
  expect(screen.getByText("87%")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: /shortlist/i }));
  expect(onShortlist).toHaveBeenCalledWith("cand_1");
});
```

**Principles:**
- Test **behavior, not implementation** — query by role/text (`getByRole`, `getByText`), not class names or internals.
- Render the smallest meaningful unit; use `userEvent` (more realistic than `fireEvent`).
- Async: `await screen.findByText(...)` for effects/fetches; wrap with `waitFor` for polling.
- Wrap providers (Router, QueryClient, ThemeProvider) via a custom `render` helper.
- Mock network with MSW (Mock Service Worker) — intercept real fetch calls.

---

## Q461: How do you test hooks?

**`@testing-library/react` `renderHook`:**
```jsx
import { renderHook, act, waitFor } from "@testing-library/react";
import { useMatchScore } from "./useMatchScore";

test("loads and exposes score", async () => {
  const { result } = renderHook(() => useMatchScore("job_1", "cand_2"));
  expect(result.current.loading).toBe(true);
  await waitFor(() => expect(result.current.score).toBe(0.87));
  expect(result.current.loading).toBe(false);
});

test("updates state on shortlist", () => {
  const { result } = renderHook(() => useShortlist());
  act(() => result.current.toggle("cand_3"));      // state updates must be in act()
  expect(result.current.isShortlisted("cand_3")).toBe(true);
});
```

- **Rule:** wrap state changes in `act()` to flush React updates.
- For effects that fetch, `waitFor` + mocked network (MSW) is the reliable pattern.
- If a hook needs context (e.g., auth), pass a `wrapper` component to `renderHook`.

---

## Q462: How do you write E2E tests? (Playwright)

**Playwright tests the real browser against the real stack:**

```ts
import { test, expect } from "@playwright/test";

test("candidate applies end-to-end", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /sign in/i }).click();
  await page.getByLabel("Email").fill("candidate@example.com");
  await page.getByLabel("Password").fill(process.env.E2E_PASSWORD!);
  await page.getByRole("button", { name: /apply to role/i }).click();
  await expect(page.getByText(/application submitted/i)).toBeVisible();
});
```

**Best practices:**
- **Resilient selectors:** `getByRole`/`getByLabel`/`getByText` — never CSS-only or xpath.
- **Run against a dedicated E2E environment** (staging) with seeded data + a test user, or use Playwright's API to set up state (fast login via API instead of clicking through auth).
- **Test the critical journeys only:** apply, chat with AI (stub the LLM with a canned stream in E2E), recruiter shortlist, notification. 10 solid E2E tests beat 100 brittle ones.
- **Isolation:** each test creates its own data (unique email per run).
- Run in CI on every PR; keep the suite < ~5–10 min.

---

## Q463: What are the differences between mocks, stubs, fakes, and spies?

- **Mock** — records calls + returns configured values; assert *how* it was called (`assert_called_with`).
- **Stub** — just returns a canned answer; doesn't verify interactions. Simplest fake.
- **Fake** — a real working implementation that's simpler/faster (in-memory repo, fake LLM client). Best for behavior, not just plumbing.
- **Spy** — wraps the *real* object and records calls without replacing behavior.

**Rule:** *spy* when you want the real behavior plus visibility; *stub* when you only need a return; *mock* when you must verify interaction; *fake* when real behavior is valuable (DB, LLM) but expensive. Too many mocks = tests that pass while the code is broken.

---

## Q464: How do you deal with flaky tests?

**Flaky = passes sometimes, fails others — the test is lying. Fix the cause, not the symptom.**

Common causes + fixes:
- **Timing/sleeps** → deterministic waits (poll with timeout, `waitFor`).
- **Shared state/order dependence** → isolate per test (Q455).
- **Real network calls** → mock/stub at boundaries (Q451, Q456).
- **Randomness/time** → freeze/seed (Q455).
- **Race conditions in the code under test** → fix the bug, don't retry the test.
- **Resource limits** (ports, DB connections) → unique resources per worker.

**Process:** when a test flakes, **don't add `@pytest.mark.flaky(retries=2)`** — that hides it. Investigate immediately; tag-and-quarantine only as a short-term measure, tracked as a bug with an owner.

---

## Q465: What's your testing strategy for the recruiter project?

**The "design a test strategy" answer:**

1. **Fast unit layer (most tests):** scoring functions, prompt building, idempotency logic, PII redaction — pure logic, fully mocked.
2. **Integration layer (the important middle):** FastAPI endpoints against a real Postgres (Testcontainers) covering apply → parse → screen flows; repository tests; queue-consumer tests with a real Redis; **LLM tests via a fake client** (deterministic golden outputs) + a contract test that the real provider satisfies the schema.
3. **Frontend:** Vitest + RTL for components/hooks; MSW for network; a handful of Playwright E2E journeys (apply, chat, shortlist) against staging with stubbed LLM.
4. **Contract/eval tests for AI:** a regression set of resumes+jobs with expected rubric scores — guards prompt changes (Q682).
5. **Non-functional:** load test the parsing pipeline and the streaming endpoint (time-to-first-token), circuit-breaker failure drill (provider down → fallback works).
6. **CI gating:** unit+integration on every PR (fast), E2E on merge, coverage floor, flaky-test quarantine policy (Q464).