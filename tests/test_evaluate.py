import json
import unittest

from clausefinder.evaluate import recall_at
from clausefinder.store import ingest_folder, open_index


class EvaluateTests(unittest.TestCase):
    def test_recall_at_3_is_perfect_on_the_sample_set(self):
        db = open_index()
        ingest_folder(db, "data/contracts")
        score, misses = recall_at(db, json.load(open("eval/questions.json")))
        self.assertEqual(misses, [])
        self.assertEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
