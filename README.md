# FreeSAT

A Flask site for free SAT, PSAT, and ACT practice.

Students can build a set by exam, section, topic, difficulty, and question count, then:

- copy, print, or download a worksheet (PDF, TXT, or JSON)
- sit a timed Bluebook-style module with a question map, mark-for-review, answer elimination, notes, calculator, and a math reference sheet
- optionally generate **additional** original items with an OpenAI API key

The bank ships with **10 labeled demo questions** plus extra original practice. No API key is required to use those. A key is used only to generate extra questions when you want more than the local bank has. None of the items are official College Board or ACT questions.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

```bash
pytest
```

## Additional questions (optional API key)

Practice, worksheets, and the testing room work with no key.

To generate more items:

- paste an OpenAI API key on **Generate more** or in the practice builder, or
- set `OPENAI_API_KEY` in the environment

The key is used only for that generation request. It is not required for the demo set. New items are written to `data/generated.json` and then appear in worksheets and the testing room.

## Notes

College Board, Bluebook, SAT, PSAT, and ACT are trademarks of their owners. This project is not affiliated with them.
