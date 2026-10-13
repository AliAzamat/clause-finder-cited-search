import sqlite3
from pathlib import Path

from .splitter import split_clauses

SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS clauses USING fts5(
    heading, body,
    doc UNINDEXED, number UNINDEXED, start UNINDEXED, end_ UNINDEXED,
    tokenize = 'porter unicode61'
)
"""


def open_index(path=":memory:"):
    db = sqlite3.connect(path, check_same_thread=False)  # the HTTP handler may run on another thread
    db.row_factory = sqlite3.Row
    db.execute(SCHEMA)
    return db


def ingest_folder(db, folder):
    count = 0
    for path in sorted(Path(folder).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for c in split_clauses(text):
            db.execute(
                "INSERT INTO clauses (heading, body, doc, number, start, end_) VALUES (?,?,?,?,?,?)",
                (c.heading, c.body, path.name, c.number, c.start, c.end),
            )
            count += 1
    db.commit()
    return count
