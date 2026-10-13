# Harvey | Clause Finder: Cited Search Over a Contract Library

An intermediate Python project shaped around the retrieval work named in Harvey's Software Engineer, New Grad (2027) posting, which lists "retrieval over large document collections" and asks new grads to own the quality of everything they ship. Clause Finder reads a folder of contract text files, splits each into numbered clauses with a regular expression while recording the exact character span of every clause, and indexes them in an SQLite FTS5 table whose address columns are stored but never searched. A plain-English question is rebuilt into a safe query (stopwords dropped, every term quoted so user punctuation can never be read as query syntax) and ranked with BM25, with headings weighted above bodies. For each hit the project extracts one sentence as a candidate answer and computes its span in the source file, then a separate checker re-reads the original file and keeps the answer only if the quote is word for word at the cited span, so a changed word such as thirty to sixty is rejected. A small HTTP endpoint returns only verified answers. The closing steps measure retrieval with an eight-question set (recall at 3 is 0.88 with the plain tokenizer and one visible miss), read why the miss happened, fix it with the Porter stemmer, and re-run the same set to 1.00, then discuss what that number does not prove. This is a practice project built from the posting's description of the work; it does not describe Harvey's own systems, and the stack below, Python's standard library and SQLite FTS5, is this project's own choice, not something the posting names.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- SQLite
- FTS5
- BM25
- http.server
- unittest
