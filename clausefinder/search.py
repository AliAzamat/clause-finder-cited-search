import re

STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for",
             "how", "if", "in", "is", "it", "of", "on", "or", "the", "to", "what", "when",
             "which", "who", "will", "with"}


def build_query(question):
    words = [w for w in re.findall(r"[a-z0-9]+", question.lower()) if w not in STOPWORDS]
    # quote each word so FTS5 treats it as a plain term, not query syntax
    return " OR ".join(f'"{w}"' for w in words)


def search(db, question, k=3):
    q = build_query(question)
    if not q:
        return []
    rows = db.execute(
        "SELECT doc, number, heading, body, start, end_, bm25(clauses, 3.0, 1.0) AS score "
        "FROM clauses WHERE clauses MATCH ? ORDER BY score LIMIT ?",
        (q, k),
    ).fetchall()
    return [dict(r) for r in rows]
