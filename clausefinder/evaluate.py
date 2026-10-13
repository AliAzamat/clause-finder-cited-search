import json
import sys

from .search import search
from .store import ingest_folder, open_index


def recall_at(db, questions, k=3):
    hits, misses = 0, []
    for item in questions:
        top = search(db, item["q"], k)
        if any(r["doc"] == item["doc"] and r["number"] == item["clause"] for r in top):
            hits += 1
        else:
            misses.append(item["q"])
    return hits / len(questions), misses


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data/contracts"
    qs = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "eval/questions.json"))
    db = open_index()
    ingest_folder(db, folder)
    score, misses = recall_at(db, qs)
    print(f"recall@3 = {score:.2f}")
    for q in misses:
        print("MISS:", q)
