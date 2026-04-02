import sqlite3
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "/tmp/smartassist.db")

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── Task tools ──────────────────────────────────────────────────────────────

def create_task(title: str, due_date: str = "", priority: str = "medium") -> dict:
    """Create a new task and store it in the database."""
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO tasks (title, due_date, priority, status, created_at) VALUES (?,?,?,?,?)",
        (title, due_date, priority, "pending", datetime.now().isoformat())
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return {"status": "created", "task_id": task_id, "title": title, "due_date": due_date, "priority": priority}

def list_tasks(status: str = "pending") -> dict:
    """List all tasks filtered by status: pending, completed, or all."""
    conn = _get_conn()
    if status == "all":
        rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC", (status,)).fetchall()
    conn.close()
    tasks = [dict(r) for r in rows]
    return {"tasks": tasks, "count": len(tasks)}

def complete_task(task_id: int) -> dict:
    """Mark a task as completed by its ID."""
    conn = _get_conn()
    conn.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "completed", "task_id": task_id}

def delete_task(task_id: int) -> dict:
    """Delete a task by its ID."""
    conn = _get_conn()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "task_id": task_id}

# ── Notes tools ─────────────────────────────────────────────────────────────

def save_note(title: str, content: str) -> dict:
    """Save a new note to the database."""
    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO notes (title, content, created_at) VALUES (?,?,?)",
        (title, content, datetime.now().isoformat())
    )
    conn.commit()
    note_id = cur.lastrowid
    conn.close()
    return {"status": "saved", "note_id": note_id, "title": title}

def list_notes() -> dict:
    """List all saved notes."""
    conn = _get_conn()
    rows = conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    conn.close()
    notes = [dict(r) for r in rows]
    return {"notes": notes, "count": len(notes)}

def get_note(note_id: int) -> dict:
    """Get full content of a note by its ID."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"error": f"Note {note_id} not found"}

def delete_note(note_id: int) -> dict:
    """Delete a note by its ID."""
    conn = _get_conn()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "note_id": note_id}
