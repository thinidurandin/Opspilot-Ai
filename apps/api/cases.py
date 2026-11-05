import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, StringConstraints

router = APIRouter(prefix="/cases", tags=["cases"])


class CaseInput(BaseModel):
    message: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=5000)]


class Case(CaseInput):
    id: UUID


def case_database() -> Path:
    return Path(os.getenv("OPSPILOT_CASE_DB", "opspilot.sqlite3"))


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, message TEXT NOT NULL)"
        )
    except Exception:
        connection.close()
        raise
    return connection


@router.post("", status_code=status.HTTP_201_CREATED)
def create_case(data: CaseInput, database: Annotated[Path, Depends(case_database)]) -> Case:
    case = Case(id=uuid4(), message=data.message)
    with closing(connect(database)) as connection, connection:
        connection.execute("INSERT INTO cases VALUES (?, ?)", (str(case.id), case.message))
    return case


@router.get("/{case_id}")
def get_case(case_id: UUID, database: Annotated[Path, Depends(case_database)]) -> Case:
    with closing(connect(database)) as connection:
        row = connection.execute(
            "SELECT message FROM cases WHERE id = ?", (str(case_id),)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return Case(id=case_id, message=row[0])
