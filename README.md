# FreeSAT

A Flask site for free SAT, PSAT, and ACT practice.

Students can build a set by exam, section, topic, difficulty, and question count, then:

- copy, print, or download a worksheet (PDF, TXT, or JSON)
- sit a timed Bluebook-style module with a question map, mark-for-review, answer elimination, notes, calculator, and a math reference sheet
- add more original items with a personal OpenAI API key

The bank ships with **10 labeled demo questions** plus extra original practice so filters work without an API key. None of the items are official College Board or ACT questions.

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

## Create more questions

On **Create questions**, paste an OpenAI API key. The key is used only for that request and is not stored by the server. You can keep it in the browser if you want. New items are written to `data/generated.json` and then appear in worksheets and the testing room.

## Notes

College Board, Bluebook, SAT, PSAT, and ACT are trademarks of their owners. This project is not affiliated with them.
