# INFICON Form Filler
### Automatic PDF & Word form completion using your company data

---

## How to Use

### Windows
1. Make sure **Python** is installed — download free from https://www.python.org/downloads/
   -  During installation, check **"Add Python to PATH"**
2. Double-click **`Install and Run.bat`**
3. The first launch installs all needed libraries automatically (takes 2–5 min)
4. On the next launch it starts instantly

### Mac / Linux
1. Make sure Python 3 is installed
2. Open Terminal, navigate to this folder
3. Run: `bash install_and_run.sh`

---

## Using the App

1. Click **Browse file…** and select your PDF or Word form
2. Click **Fill Form** — the progress bar will track the process
3. When complete, click **Save Output** to save the filled form

---

## What Gets Filled

The app uses AI to match each field in your form to the company data stored in `confluence_data.json`.

- **Auto-filled** — high-confidence matches (≥80%)
- **Review suggested** — medium-confidence matches (70–80%), shown in orange
- **Needs manual review** — low-confidence matches, left blank

---

## Files in this folder

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `confluence_data.json` | Company data source |
| `similarity_test.py` | AI field matching |
| `vector_embedding_model.py` | Embedding model loader |
| `fill_pdf_form.py` | PDF form filler |
| `fill_docx_form.py` | Word form filler |
| `Install and Run.bat` | Windows launcher |
| `install_and_run.sh` | Mac/Linux launcher |

---

## Troubleshooting

**"Python is not installed"** — Download from python.org and re-run the launcher.

**App opens but nothing fills** — Your form may not have standard fillable fields.

**Slow first launch** — The AI model (~1.3 GB) is downloaded once and cached automatically.
