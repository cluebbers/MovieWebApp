# MovieWebApp

Simple Flask app to manage users and their favorite movies using OMDb + SQLite.

## Setup

```bash
cd Assessment/MovieWebApp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
OMDB_KEY=your_omdb_api_key
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000`.
