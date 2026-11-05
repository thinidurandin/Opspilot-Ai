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

## Try enquiry intake

In the API docs, use `POST /cases` with a synthetic message:

```json
{"message": "I was charged twice for my monthly membership. Can you help?"}
```

Copy the returned ID into `GET /cases/{case_id}` to open the saved enquiry.
For local development, the API stores cases in `opspilot.sqlite3`. Set
`OPSPILOT_CASE_DB` to use another file. This intake API has no authentication yet,
so keep it local and use synthetic messages.

## Open the demo payment history

Use `GET /cases/{case_id}/demo-customer` with an existing case ID. The endpoint
returns the same fictional Tunnel Express Car Wash account for every saved case.
It contains two AUD 49.00 charges for the same membership period. The demo
account and payments are sample data for testing the billing workflow.

## Run the tests

```sh
python -m pytest
```

GitHub Actions runs the same test command on pushes and pull requests.

## Build milestones

1. **API foundation** — health endpoint and automated test.
2. **Case management** — capture and reopen enquiries locally, then add PostgreSQL, synthetic accounts, and payments.
3. **Evidence and drafting** — upload policies and use one LangGraph workflow to classify, retrieve, look up, and draft.
4. **Staff review** — add the Next.js dashboard, role based permissions, approval, simulated actions, and audit logging.
6. **Evaluation** — measure classification, retrieval, citations, safety, latency, and estimated cost on 50–100 fixed synthetic enquiries.
