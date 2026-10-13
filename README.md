# Clause Finder

**Ask a plain-English question about a folder of contracts and get back the exact sentence that answers it, cited by document, clause number, and character offsets. A separate checker re-reads the source file before returning anything, so every answer is verified against the original text.**

Built in Python using only the standard library and SQLite FTS5, so there's nothing to install. It has 16 unit tests and a small retrieval evaluation.

```text
$ curl "localhost:8765/search?q=how+long+do+confidentiality+duties+last"
{
  "doc": "orbit-nda.txt",
  "clause": "4",
  "heading": "Duration",
  "quote": "The duty to protect Confidential Information survives for five years after the date of disclosure.",
  "start": 689,
  "end": 787,
  "verified": true
}
```

The response above is the top result, trimmed. The real response returns up to three results and includes the BM25 `score` for each.

## How it works

```text
contracts/*.txt
   │  splitter.py   regex finds "4. Heading. Body..." and records each body's start/end offset
   ▼
SQLite FTS5 table   heading + body searchable; doc, number, offsets stored but not indexed
   │  search.py     question → stopwords dropped, each term quoted, OR-joined → BM25 (heading ×3)
   ▼
top 3 clauses
   │  answer.py     pick the sentence sharing the most words with the question; compute its file offsets
   ▼
candidate answers
   │  check.py      re-read the source file; keep only if text[start:end] == quote
   ▼
verified answers → GET /search
```

- **Citations are character spans in the original file**, not just a document name. Anyone can open the file and confirm the quote.
- **Questions can't inject query syntax.** Only letters and digits are kept, and every remaining word is quoted, so quotes, parentheses, or an `OR` typed into a question are never read as FTS5 operators. A test covers this.
- **Headings weigh three times as much as bodies** in BM25 ranking, so a word that appears in a clause's title counts more than one buried in its text.
- **Verification is separate from extraction.** `check.py` doesn't trust the offsets it's given. It rejects a quote if a single word differs (for example, "thirty" changed to "sixty"), if the offsets are wrong, or if the document is missing.

## Evaluation

`eval/questions.json` has 8 questions, each labelled with the clause that answers it. Here's how often the right clause appears in the top 3 results (recall@3):

| Tokenizer | recall@3 | Miss |
|---|---|---|
| `unicode61` | 0.88 | "How long do confidentiality duties last?" |
| `porter unicode61` (current) | **1.00** | — |

The miss happens because the question says *confidentiality* and *duties*, while the clause says *Confidential* and *duty*. Without stemming those words never match. The Porter stemmer reduces both pairs to the same root. Both rows reproduce by switching the `tokenize` setting in `store.py`.

The corpus is three short sample contracts (18 clauses), and the questions were written alongside them. A perfect score here shows the pipeline works end to end. It doesn't show how well retrieval holds up on real contract libraries.

## Quick start

There are no third-party dependencies; you only need Python with an SQLite build that includes FTS5, which standard builds do. Tested on Python 3.13.

```bash
git clone https://github.com/AliAzamat/clause-finder-cited-search.git
cd clause-finder-cited-search

python -m unittest                      # 16 tests
python -m clausefinder.evaluate         # recall@3 = 1.00
python -m clausefinder.server           # prints "indexed 18 clauses", then serves on 127.0.0.1:8765
```

Then:

```bash
curl "localhost:8765/search?q=where+is+arbitration+held"
```

Both commands accept arguments for your own data: `python -m clausefinder.server <folder> <port>` and `python -m clausefinder.evaluate <folder> <questions.json>`.

## Project layout

| Path | Purpose |
|---|---|
| `clausefinder/splitter.py` | Split a contract into numbered clauses with exact offsets |
| `clausefinder/store.py` | FTS5 schema and folder ingestion |
| `clausefinder/search.py` | Safe query building and BM25 ranking |
| `clausefinder/answer.py` | Best-sentence extraction with file offsets |
| `clausefinder/check.py` | Verify a quote against the source file |
| `clausefinder/server.py` | `GET /search?q=…` JSON endpoint, returning verified results only |
| `clausefinder/evaluate.py` | recall@k over a labelled question set |
| `data/contracts/` | Sample MSA, SaaS agreement, and NDA |
| `eval/questions.json` | 8 labelled questions |

## Limitations

- **Matching is by keyword (BM25), not by meaning.** A question that uses none of the clause's words won't find it, even with stemming.
- **Sentence splitting is naive.** `answer.py` splits on every period, so "1.5 percent" or "Inc." cuts a sentence short. For example, it returns "Interest is 1." from "Interest is 1.5 percent per month." A clause body with no period at all raises a `TypeError`.
- **The verifier confirms exactness, not relevance.** It proves the quote is really in the file at the cited place, but not that the sentence answers the question. Because the offsets come from the same files, it mainly catches files that changed after indexing and offset bugs.
- **Only one clause format is parsed:** lines like `4. Heading. Body…`, where sub-numbers such as `4.1` also work. Other numbering styles and PDFs or Word files aren't handled.
- **The index is in memory and rebuilt on every start.** The server is a single-threaded `http.server` bound to localhost, meant for local use.
