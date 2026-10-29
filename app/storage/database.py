import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "analyst.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                session_id TEXT PRIMARY KEY,
                user_query TEXT NOT NULL,
                dataset_id TEXT NOT NULL,
                status TEXT NOT NULL,
                analysis_plan TEXT,
                tool_calls TEXT,
                evidence TEXT,
                validation_results TEXT,
                errors TEXT,
                final_report TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def save_analysis_session(state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO analysis_sessions (
                session_id,
                user_query,
                dataset_id,
                status,
                analysis_plan,
                tool_calls,
                evidence,
                validation_results,
                errors,
                final_report,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(session_id) DO UPDATE SET
                status = excluded.status,
                analysis_plan = excluded.analysis_plan,
                tool_calls = excluded.tool_calls,
                evidence = excluded.evidence,
                validation_results = excluded.validation_results,
                errors = excluded.errors,
                final_report = excluded.final_report,
                updated_at = excluded.updated_at
            """,
            (
                state["session_id"],
                state.get("user_query", ""),
                state.get("dataset_id", ""),
                state.get("status", ""),
                json.dumps(state.get("analysis_plan", []), default=str),
                json.dumps(state.get("tool_calls", []), default=str),
                json.dumps(state.get("evidence", []), default=str),
                json.dumps(
                    state.get("validation_results", []),
                    default=str,
                ),
                json.dumps(state.get("errors", []), default=str),
                state.get("final_report", ""),
                now,
                now,
            ),
        )

        connection.commit()


def get_analysis_session(session_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM analysis_sessions
            WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone()

    if row is None:
        return None

    return {
        "session_id": row["session_id"],
        "user_query": row["user_query"],
        "dataset_id": row["dataset_id"],
        "status": row["status"],
        "analysis_plan": json.loads(row["analysis_plan"] or "[]"),
        "tool_calls": json.loads(row["tool_calls"] or "[]"),
        "evidence": json.loads(row["evidence"] or "[]"),
        "validation_results": json.loads(
            row["validation_results"] or "[]"
        ),
        "errors": json.loads(row["errors"] or "[]"),
        "final_report": row["final_report"] or "",
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }