from fastapi import FastAPI

from apps.api.cases import router as cases_router

app = FastAPI(title="OpsPilot API")
app.include_router(cases_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
