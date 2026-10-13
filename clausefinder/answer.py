import re

from .search import STOPWORDS


def best_sentence(body, question):
    """Return (quote, offset_in_body) for the sentence sharing most words with the question."""
    terms = {w for w in re.findall(r"[a-z0-9]+", question.lower()) if w not in STOPWORDS}
    best = None
    for m in re.finditer(r"[^.]+\.", body):
        sentence = m.group(0).strip()
        words = set(re.findall(r"[a-z0-9]+", sentence.lower()))
        score = len(terms & words)
        if best is None or score > best[0]:
            best = (score, sentence, body.index(sentence, m.start()))
    return best[1], best[2]


def make_answer(hit, question):
    quote, offset = best_sentence(hit["body"], question)
    return {
        "doc": hit["doc"],
        "clause": hit["number"],
        "heading": hit["heading"],
        "quote": quote,
        "start": hit["start"] + offset,
        "end": hit["start"] + offset + len(quote),
        "score": hit["score"],
    }
