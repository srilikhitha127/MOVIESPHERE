# MovieSphere — Python Movie Discovery Platform

MovieSphere is a Python FastAPI movie discovery application with a cinematic orange/gold and dark-maroon interface, search, genre/year/rating filters, movie details, watchlist, and recommendations.

## Run on Windows

1. Extract the ZIP folder.
2. Open the `MovieSphere_Python` folder.
3. Double-click `run.bat`.
4. Keep the black terminal window open.
5. Open http://127.0.0.1:8000 in Chrome.

The first run creates `.venv` and installs the packages automatically. If Windows blocks the batch file, open CMD in this folder and run:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## Movie data through 2026

The project includes the original 4,803-title offline TMDB 5000 collection plus a small curated 2026 release starter list in `data/recent_2026.json`.

For a broader live catalogue, create a free TMDB developer account and obtain an API key or Read Access Token. Copy `.env.example` to `.env` and set:

```env
TMDB_API_KEY=your_tmdb_v3_api_key_or_v4_read_access_token
```

Restart MovieSphere. When the key is configured, Discover/Search use TMDB's live movie endpoints and request releases dated from 2018-01-01 through 2026-12-31. The application uses TMDB's `/discover/movie`, `/search/movie`, `/movie/{id}`, and `/movie/{id}/similar` endpoints. Without a key, the app still works offline with the included data and the curated 2026 titles.

TMDB data and images are provided by The Movie Database (TMDB). Movie release dates can vary by country and change over time. The curated 2026 entries are a starter list, not a complete catalogue.

## Features

- MovieSphere brand and responsive cinematic UI
- Search movies by title
- Filter by genre, release year, and rating
- Sort by popularity, rating, newest, or title
- Movie detail modal and similar-title recommendations
- SQLite watchlist saved locally
- Optional live TMDB catalogue through 2026
- Offline fallback dataset

## Project structure

```text
MovieSphere_Python/
├── main.py
├── requirements.txt
├── run.bat
├── .env.example
├── README.md
├── data/
│   ├── movies.json
│   ├── recommendations.json
│   ├── recent_2026.json
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Tests

```bash
pytest -q
```

### MovieSphere hero artwork
The homepage uses `static/moviesphere-hero.png` as its cinematic moon, seated-viewer and filmstrip background. Keep this file in the `static` folder when moving or deploying the app.
