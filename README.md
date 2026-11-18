
# 🎬 MovieSphere – Your Movie World Awaits 🍿

> ✨ Discover amazing movies. 🔎 Find your favourites. ❤️ Build your watchlist.

MovieSphere is a movie discovery web application built with **Python** and **FastAPI**. It allows users to explore movies, search for titles, browse movies by genre, view movie information, and save favourite movies to a personal watchlist.

---

## 🌟 Features

- 🎥 **Movie Discovery:** Browse the available movie collection.
- 🔍 **Movie Search:** Search for movies by title.
- 🎭 **Genre Filters:** Explore Action, Comedy, Drama, Sci-Fi, and Thriller movies.
- ❤️ **Watchlist:** Add favourite movies and view them in your Watchlist.
- ⭐ **Movie Information:** View movie titles, release years, ratings, and other details.
- ➕ **Load More Movies:** Load additional movie results.
- 🌐 **TMDB Integration:** Retrieve movie information and expand the movie catalogue.
- 🌙 **Cinematic Interface:** Dark-themed design with warm orange highlights.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming |
| ⚡ FastAPI | Web application framework |
| 🧩 Jinja2 | HTML templating |
| 🌐 HTML | Web page structure |
| 🎨 CSS | Styling and layout |
| ⚙️ JavaScript | Frontend interactions |
| 📄 JSON | Movie data storage |
| 🗄️ SQLite | Watchlist data storage |
| 🎬 TMDB API | Movie information and posters |

---

## 📁 Project Structure

```text
🎬 MovieSphere/
│
├── 🐍 main.py
├── 📦 requirements.txt
├── 🔐 .env
├── 🚫 .gitignore
├── 📘 README.md
│
├── 📂 data/
│   ├── 🎞️ movies.json
│   └── ⭐ recommendations.json
│
├── 📂 static/
│   ├── 🎨 css/
│   ├── ⚙️ js/
│   └── 🖼️ images/
│
└── 📂 templates/
    └── 🌐 index.html
```

---

## ⚙️ Installation and Setup

### 1️⃣ Open the project folder

```bash
cd MovieSphere
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install fastapi uvicorn jinja2 requests python-dotenv
```

---

## 🔑 TMDB API Configuration

1. 🌐 Create an account at [The Movie Database](https://www.themoviedb.org/).
2. 🔐 Request an API key from your TMDB account settings.
3. 📄 Create a `.env` file in the same folder as `main.py`.
4. ✍️ Add your API key:

```env
TMDB_API_KEY=YOUR_TMDB_API_KEY
```

### 🔒 API Key Security

- Never publish your actual API key on GitHub.
- Add `.env` to your `.gitignore` file.
- Never share your API key publicly.

Example `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Run this command in your terminal:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

🌍 Open your browser:

```text
http://127.0.0.1:8000
```

💡 Press `CTRL + C` to stop the server.

---

## 🎨 Application Design

MovieSphere features a cinematic dark interface with warm orange and golden accents. It brings together movie discovery, search, genre navigation, and watchlist access in one place.

---

## 👩‍💻 Developer

**Developed by:** Srilikhitha

📧 **Email:** srilikhitha127@gmail.com

---

## 🙏 Acknowledgement

A special thanks to the developers and maintainers of **FastAPI** and **The Movie Database (TMDB)** for providing useful tools and movie data services that support this application.

---

## 📌 Important Notes

- 🎞️ Movies displayed depend on local movie data and/or TMDB API configuration.
- 🔑 A valid TMDB API key is required for TMDB API access.
- 🖼️ Poster availability depends on the image data returned by the movie data source.
- 🔒 Keep private credentials out of public repositories.
- 📝 Update this README whenever project features or setup instructions change.

---

<div align="center">

## 🍿 MovieSphere – Your Movie World Awaits! ✨

**🎬 Discover • 🔎 Explore • ❤️ Enjoy**

</div>
