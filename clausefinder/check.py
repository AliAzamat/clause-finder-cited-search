from pathlib import Path


def verify(answer, folder):
    """True only if the quote sits word for word at the cited place in the source file."""
    path = Path(folder) / answer["doc"]
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return text[answer["start"]:answer["end"]] == answer["quote"]
