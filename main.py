
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import sqlite3
import requests

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

load_dotenv(BASE / ".env")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = FastAPI(title="MovieSphere")

app.mount(
    "/static",
    StaticFiles(directory=BASE / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE / "templates"
)


# --------------------------------------------------
# TMDB API CONNECTION
# --------------------------------------------------

def tmdb_get(endpoint, params=None):

    if not TMDB_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="TMDB API key is missing. Check your .env file."
        )

    try:

        response = requests.get(
            f"{TMDB_BASE_URL}/{endpoint}",
            params={
                "api_key": TMDB_API_KEY,
                **(params or {})
            },
            timeout=20
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to TMDB API."
        )


# --------------------------------------------------
# LOAD JSON DATA
# --------------------------------------------------

def load_json(name):

    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


MOVIES = load_json("movies.json")

RECOMMENDATIONS = load_json("recommendations.json")

BY_ID = {
    str(m.get("id")): m
    for m in MOVIES
}

BY_TITLE = {
    m.get("title", "").casefold(): m
    for m in MOVIES
}


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def db():

    conn = sqlite3.connect(
        BASE / "cinematch.db"
    )

    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (

            movie_id TEXT PRIMARY KEY,

            title TEXT NOT NULL,

            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    return conn


# --------------------------------------------------
# MOVIE HELPER FUNCTIONS
# --------------------------------------------------

def genres_of(movie):

    value = movie.get("genres", [])

    if isinstance(value, str):

        return [
            x.strip()
            for x in value.split(",")
            if x.strip()
        ]

    return [
        x if isinstance(x, str) else x.get("name", "")
        for x in value
        if x
    ]


def year_of(movie):

    date = str(
        movie.get("release_date") or ""
    )

    return (
        date[:4]
        if len(date) >= 4 and date[:4].isdigit()
        else ""
    )


def poster(movie):

    path = movie.get("poster_path")

    return (
        f"{TMDB_IMAGE_URL}{path}"
        if path
        else ""
    )


def movie_view(movie):

    return {
        **movie,

        "year": year_of(movie),

        "genre_list": genres_of(movie),

        "poster_url": poster(movie)
    }


def tmdb_movie_view(movie):

    return {
        **movie,

        "year": year_of(movie),

        "genre_list": genres_of(movie),

        "poster_url": poster(movie)
    }


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    genres = sorted({
        g
        for m in MOVIES
        for g in genres_of(m)
    })

    years = sorted(
        {
            year_of(m)
            for m in MOVIES
            if year_of(m)
        },
        reverse=True
    )

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "genres": genres,
            "years": years,
            "movie_count": len(MOVIES)
        }
    )


# --------------------------------------------------
# LOCAL MOVIES API
# --------------------------------------------------

@app.get("/api/movies")
def movies(
    q: str = "",
    genre: str = "all",
    year: str = "all",
    rating: float = 0,
    sort: str = "popular",
    page: int = 1,
    limit: int = 30
):

    result = MOVIES

    if q.strip():

        term = q.casefold().strip()

        result = [
            m for m in result
            if term in m.get("title", "").casefold()
        ]

    if genre != "all":

        result = [
            m for m in result
            if genre in genres_of(m)
        ]

    if year != "all":

        result = [
            m for m in result
            if year_of(m) == year
        ]

    result = [
        m for m in result
        if float(m.get("vote_average") or 0) >= rating
    ]

    if sort == "rating":

        result = sorted(
            result,
            key=lambda m: float(
                m.get("vote_average") or 0
            ),
            reverse=True
        )

    elif sort == "year":

        result = sorted(
            result,
            key=lambda m: year_of(m),
            reverse=True
        )

    elif sort == "title":

        result = sorted(
            result,
            key=lambda m: m.get("title", "").casefold()
        )

    else:

        result = sorted(
            result,
            key=lambda m: float(
                m.get("popularity")
                or m.get("vote_count")
                or 0
            ),
            reverse=True
        )

    total = len(result)

    limit = min(max(limit, 1), 100)

    page = max(page, 1)

    start = (page - 1) * limit

    return {
        "total": total,

        "page": page,

        "movies": [
            movie_view(m)
            for m in result[start:start + limit]
        ]
    }


# --------------------------------------------------
# LOCAL MOVIE SEARCH
# --------------------------------------------------

@app.get("/api/search")
def search(q: str = ""):

    if len(q.strip()) < 2:
        return []

    term = q.casefold().strip()

    found = [
        m for m in MOVIES
        if term in m.get("title", "").casefold()
    ]

    found.sort(
        key=lambda m: (
            not m.get("title", "").casefold().startswith(term),
            m.get("title", "").casefold()
        )
    )

    return [
        movie_view(m)
        for m in found[:7]
    ]


# --------------------------------------------------
# LOCAL MOVIE DETAILS
# --------------------------------------------------

@app.get("/api/movie/{movie_id}")
def movie_detail(movie_id: str):

    movie = BY_ID.get(str(movie_id))

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie_view(movie)


# --------------------------------------------------
# LOCAL MOVIE RECOMMENDATIONS
# --------------------------------------------------

@app.get("/api/recommendations/{movie_id}")
def recommendations(movie_id: str):

    movie = BY_ID.get(str(movie_id))

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    entries = RECOMMENDATIONS.get(
        movie.get("title"),
        []
    )

    output = []

    for item in entries:

        title = (
            item
            if isinstance(item, str)
            else (
                item.get("title")
                or item.get("movie_title")
                or item.get("name")
            )
        )

        score = (
            None
            if isinstance(item, str)
            else item.get(
                "score",
                item.get("similarity_score")
            )
        )

        candidate = (
            BY_TITLE.get(str(title).casefold())
            if title
            else None
        )

        if candidate:

            output.append({
                **movie_view(candidate),
                "similarity": score
            })

    return output


# --------------------------------------------------
# WATCHLIST - GET
# --------------------------------------------------

@app.get("/api/watchlist")
def get_watchlist():

    with db() as conn:

        rows = conn.execute("""
            SELECT movie_id
            FROM watchlist
            ORDER BY added_at DESC
        """).fetchall()

    return [
        movie_view(BY_ID[x["movie_id"]])
        for x in rows
        if x["movie_id"] in BY_ID
    ]


# --------------------------------------------------
# WATCHLIST - ADD
# --------------------------------------------------

@app.post("/api/watchlist/{movie_id}")
def add_watchlist(movie_id: str):

    movie = BY_ID.get(str(movie_id))

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    with db() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO watchlist(movie_id, title)
            VALUES(?, ?)
            """,
            (
                str(movie_id),
                movie["title"]
            )
        )

    return {
        "ok": True
    }


# --------------------------------------------------
# WATCHLIST - REMOVE
# --------------------------------------------------

@app.delete("/api/watchlist/{movie_id}")
def remove_watchlist(movie_id: str):

    with db() as conn:

        conn.execute(
            "DELETE FROM watchlist WHERE movie_id=?",
            (str(movie_id),)
        )

    return {
        "ok": True
    }


# --------------------------------------------------
# WATCHLIST - CLEAR
# --------------------------------------------------

@app.delete("/api/watchlist")
def clear_watchlist():

    with db() as conn:

        conn.execute(
            "DELETE FROM watchlist"
        )

    return {
        "ok": True
    }


# ==================================================
# TMDB LIVE MOVIE API
# ==================================================


# --------------------------------------------------
# TEST TMDB CONNECTION
# --------------------------------------------------

@app.get("/api/tmdb/test")
def test_tmdb():

    data = tmdb_get("configuration")

    return {
        "message": "TMDB Connected Successfully!",

        "status": "success"
    }


# --------------------------------------------------
# POPULAR MOVIES
# --------------------------------------------------

@app.get("/api/tmdb/popular")
def tmdb_popular(page: int = 1):

    data = tmdb_get(
        "movie/popular",
        {
            "page": max(page, 1)
        }
    )

    return {
        "total": data.get("total_results", 0),

        "page": data.get("page", 1),

        "movies": [
            tmdb_movie_view(m)
            for m in data.get("results", [])
        ]
    }


# --------------------------------------------------
# NOW PLAYING MOVIES
# --------------------------------------------------

@app.get("/api/tmdb/now-playing")
def tmdb_now_playing(page: int = 1):

    data = tmdb_get(
        "movie/now_playing",
        {
            "page": max(page, 1),

            "region": "IN"
        }
    )

    return {
        "total": data.get("total_results", 0),

        "movies": [
            tmdb_movie_view(m)
            for m in data.get("results", [])
        ]
    }


# --------------------------------------------------
# UPCOMING MOVIES
# --------------------------------------------------

@app.get("/api/tmdb/upcoming")
def tmdb_upcoming(page: int = 1):

    data = tmdb_get(
        "movie/upcoming",
        {
            "page": max(page, 1),

            "region": "IN"
        }
    )

    return {
        "total": data.get("total_results", 0),

        "movies": [
            tmdb_movie_view(m)
            for m in data.get("results", [])
        ]
    }


# --------------------------------------------------
# TOP RATED MOVIES
# --------------------------------------------------

@app.get("/api/tmdb/top-rated")
def tmdb_top_rated(page: int = 1):

    data = tmdb_get(
        "movie/top_rated",
        {
            "page": max(page, 1)
        }
    )

    return {
        "total": data.get("total_results", 0),

        "movies": [
            tmdb_movie_view(m)
            for m in data.get("results", [])
        ]
    }


# --------------------------------------------------
# DISCOVER MOVIES - INCLUDING 2026
# --------------------------------------------------

@app.get("/api/tmdb/discover")
def tmdb_discover(
    year: int = 2026,
    rating: float = 0,
    genre: int = 0,
    sort: str = "popularity.desc",
    page: int = 1
):

    allowed_sorts = [
        "popularity.desc",
        "vote_average.desc",
        "primary_release_date.desc",
        "primary_release_date.asc",
        "original_title.asc"
    ]

    if sort not in allowed_sorts:

        raise HTTPException(
            status_code=400,
            detail="Invalid sorting option"
        )

    params = {
        "page": max(page, 1),

        "primary_release_year": year,

        "sort_by": sort,

        "vote_count.gte": 1
    }

    if rating > 0:
        params["vote_average.gte"] = rating

    if genre > 0:
        params["with_genres"] = genre

    data = tmdb_get(
        "discover/movie",
        params
    )

    return {
        "total": data.get("total_results", 0),

        "page": data.get("page", 1),

        "movies": [
            tmdb_movie_view(m)
            for m in data.get("results", [])
        ]
    }


# --------------------------------------------------
# TMDB MOVIE SEARCH
# --------------------------------------------------

@app.get("/api/tmdb/search")
def tmdb_search(query: str, page: int = 1):

    if len(query.strip()) < 2:
        return []

    data = tmdb_get(
        "search/movie",
        {
            "query": query.strip(),

            "page": max(page, 1),

            "include_adult": False
        }
    )

    return [
        tmdb_movie_view(m)
        for m in data.get("results", [])
    ]


# --------------------------------------------------
# TMDB MOVIE DETAILS
# --------------------------------------------------

@app.get("/api/tmdb/movie/{movie_id}")
def tmdb_movie_detail(movie_id: int):

    movie = tmdb_get(
        f"movie/{movie_id}"
    )

    return tmdb_movie_view(movie)


# --------------------------------------------------
# TMDB MOVIE RECOMMENDATIONS
# --------------------------------------------------

@app.get("/api/tmdb/movie/{movie_id}/recommendations")
def tmdb_recommendations(movie_id: int, page: int = 1):

    data = tmdb_get(
        f"movie/{movie_id}/recommendations",
        {
            "page": max(page, 1)
        }
    )

    return [
        tmdb_movie_view(m)
        for m in data.get("results", [])
    ]
