import unittest

from clausefinder.store import ingest_folder, open_index


class StoreTests(unittest.TestCase):
    def test_ingest_counts_every_clause(self):
        db = open_index()
        self.assertEqual(ingest_folder(db, "data/contracts"), 18)
        row = db.execute("SELECT count(*) AS n FROM clauses WHERE doc = 'orbit-nda.txt'").fetchone()
        self.assertEqual(row["n"], 6)


if __name__ == "__main__":
    unittest.main()
