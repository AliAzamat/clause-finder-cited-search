import unittest

from clausefinder.search import build_query, search
from clausefinder.store import ingest_folder, open_index


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.db = open_index()
        ingest_folder(self.db, "data/contracts")

    def test_query_drops_stopwords_and_quotes_terms(self):
        self.assertEqual(build_query("What is the governing law?"), '"governing" OR "law"')

    def test_governing_law_question_finds_a_governing_law_clause(self):
        top = search(self.db, "What law governs this agreement?", 1)[0]
        self.assertEqual((top["doc"], top["number"]), ("acme-msa.txt", "6"))

    def test_punctuation_cannot_break_the_query(self):
        search(self.db, 'termination" OR (')  # must not raise

    def test_empty_question_returns_nothing(self):
        self.assertEqual(search(self.db, "the of a"), [])


if __name__ == "__main__":
    unittest.main()
