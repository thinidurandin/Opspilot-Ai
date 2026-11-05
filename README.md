# OpsPilot

An operations copilot for Australian small businesses. The first demo follows a
synthetic car wash enquiry from intake through staff review.

## Run the API locally

From the repository root, using Python 3.13:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r apps/api/requirements-dev.txt
python -m uvicorn apps.api.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API. The health check at
http://127.0.0.1:8000/health returns `{"status":"ok"}` when the server is running.

## Run the tests

```sh
python -m pytest
```

GitHub Actions runs the same test command on pushes and pull requests.

## Build milestones

1. **API foundation** — health endpoint and automated test.
2. **Case management** — store enquiries, synthetic accounts, and payments in PostgreSQL.
3. **Evidence and drafting** — upload policies and use one LangGraph workflow to classify, retrieve, look up, and draft.
4. **Staff review** — add the Next.js dashboard, role-based permissions, approval, simulated actions, and audit logging.
5. **Evaluation** — measure classification, retrieval, citations, safety, latency, and estimated cost on 50–100 fixed synthetic enquiries.
