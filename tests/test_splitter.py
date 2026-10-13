import unittest
from pathlib import Path

from clausefinder.splitter import split_clauses

TEXT = Path("data/contracts/acme-msa.txt").read_text(encoding="utf-8")


class SplitterTests(unittest.TestCase):
    def test_finds_every_numbered_clause(self):
        clauses = split_clauses(TEXT)
        self.assertEqual([c.number for c in clauses], ["1", "2", "3", "4", "5", "6"])
        self.assertEqual(clauses[3].heading, "Termination")

    def test_offsets_point_back_into_the_file(self):
        for c in split_clauses(TEXT):
            self.assertEqual(TEXT[c.start:c.end], c.body)

    def test_title_line_is_not_a_clause(self):
        self.assertNotIn("MASTER SERVICES", split_clauses(TEXT)[0].body)


if __name__ == "__main__":
    unittest.main()
