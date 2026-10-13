import unittest

from clausefinder.answer import make_answer
from clausefinder.search import search
from clausefinder.store import ingest_folder, open_index


class AnswerTests(unittest.TestCase):
    def test_answer_cites_the_exact_span(self):
        db = open_index()
        ingest_folder(db, "data/contracts")
        q = "How long is the duty to protect information?"
        a = make_answer(search(db, q, 1)[0], q)
        self.assertEqual((a["doc"], a["clause"]), ("orbit-nda.txt", "4"))
        text = open("data/contracts/orbit-nda.txt", encoding="utf-8").read()
        self.assertEqual(text[a["start"]:a["end"]], a["quote"])


if __name__ == "__main__":
    unittest.main()
