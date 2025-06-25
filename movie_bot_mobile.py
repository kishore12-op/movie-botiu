import streamlit as st
import requests

# CONFIG
API_KEY = "d4e5f5cfcf11b1712dc7c985e92e4fd4"
TMDB_BASE = "https://api.themoviedb.org/3"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body { background-color: #111; color: white; }
    .block-container { padding-top: 2rem; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;color:#E50914;'>🎬 NeoFlix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Stream trending, anime, adult and new movies – all in one place</p>", unsafe_allow_html=True)


# --- Function to fetch movie sections ---
def fetch_movies(endpoint, params=None):
    if params is None:
        params = {}
    params["api_key"] = API_KEY
    res = requests.get(f"{TMDB_BASE}{endpoint}", params=params)
    return res.json().get("results", [])


# --- Function to render a horizontal scroll row ---
def render_row(movies):
    cols = st.columns(len(movies[:5]))
    for i, movie in enumerate(movies[:5]):
        with cols[i]:
            if movie.get("poster_path"):
                st.image(POSTER_BASE + movie["poster_path"], use_column_width=True)
            st.markdown(f"<small>{movie.get('title', 'Unknown')}</small>", unsafe_allow_html=True)


# --- Sections ---
sections = {
    "🔥 Trending": fetch_movies("/trending/movie/week"),
    "🌸 Anime": fetch_movies("/discover/movie", {"with_genres": "16", "sort_by": "popularity.desc"}),
    "🔞 Adult": fetch_movies("/discover/movie", {"include_adult": "true", "sort_by": "popularity.desc"}),
    "🆕 New Releases": fetch_movies("/movie/now_playing"),
}

for title, data in sections.items():
    st.markdown(f"## {title}")
    render_row(data)
    st.markdown("---")

# --- Optional YouTube Trailer placeholder ---
if sections["🔥 Trending"]:
    title = sections["🔥 Trending"][0]["title"]
    st.markdown("### 🎞️ Featured Trailer")
    st.video(f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+official+trailer")
