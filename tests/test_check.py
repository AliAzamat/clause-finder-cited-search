import unittest

from clausefinder.answer import make_answer
from clausefinder.check import verify
from clausefinder.search import search
from clausefinder.store import ingest_folder, open_index

Q = "Can either side end the contract for breach?"


class CheckTests(unittest.TestCase):
    def setUp(self):
        db = open_index()
        ingest_folder(db, "data/contracts")
        self.answer = make_answer(search(db, Q, 1)[0], Q)

    def test_real_quote_passes(self):
        self.assertTrue(verify(self.answer, "data/contracts"))

    def test_changed_word_is_rejected(self):
        bad = {**self.answer, "quote": self.answer["quote"].replace("thirty", "sixty")}
        self.assertFalse(verify(bad, "data/contracts"))

    def test_wrong_offsets_are_rejected(self):
        bad = {**self.answer, "start": self.answer["start"] + 1, "end": self.answer["end"] + 1}
        self.assertFalse(verify(bad, "data/contracts"))

    def test_missing_document_is_rejected(self):
        self.assertFalse(verify({**self.answer, "doc": "nope.txt"}, "data/contracts"))


if __name__ == "__main__":
    unittest.main()
