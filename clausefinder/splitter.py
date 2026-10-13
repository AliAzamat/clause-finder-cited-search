import re
from dataclasses import dataclass

# A clause starts on a line like "4. Termination. Either party may..."
CLAUSE_START = re.compile(r"^(\d+(?:\.\d+)*)\.\s+([^.\n]+)\.\s*", re.M)


@dataclass(frozen=True)
class Clause:
    number: str
    heading: str
    body: str
    start: int  # offset of the body in the source file
    end: int    # offset just past the body


def split_clauses(text):
    matches = list(CLAUSE_START.finditer(text))
    clauses = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].rstrip()
        end = start + len(body)
        clauses.append(Clause(m.group(1), m.group(2), body, start, end))
    return clauses
