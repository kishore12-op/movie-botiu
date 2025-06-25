import streamlit as st
import requests

API_KEY = 'd4e5f5cfcf11b1712dc7c985e92e4fd4'

BASE_URL = "https://api.themoviedb.org/3"
POSTER_PATH = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="🎬 NeoFlix", layout="wide")
st.markdown("<h1 style='text-align:center; color:#E50914;'>NeoFlix 🎥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white;'>Your futuristic movie explorer 🔮</p>", unsafe_allow_html=True)

def fetch_movies(endpoint, params=None):
    if params is None:
        params = {}
    params['api_key'] = API_KEY
    response = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return response.json().get("results", [])

def display_movie_section(title, movies):
    st.markdown(f"### {title}")
    cols = st.columns(5)
    for i, movie in enumerate(movies[:10]):
        with cols[i % 5]:
            if movie.get("poster_path"):
                st.image(f"{POSTER_PATH}{movie['poster_path']}", use_column_width=True)
                st.caption(movie.get("title", "Unknown"))

# Trending
trending = fetch_movies("/trending/movie/day")
display_movie_section("🔥 Trending Movies", trending)

# Anime
anime = fetch_movies("/discover/movie", {"with_genres": "16", "sort_by": "popularity.desc"})
display_movie_section("🌸 Anime Picks", anime)

# Adult
adult = fetch_movies("/discover/movie", {"include_adult": "true", "sort_by": "popularity.desc"})
display_movie_section("🔞 Adult Movies (18+)", adult)

# New Releases
now_playing = fetch_movies("/movie/now_playing")
display_movie_section("🆕 Now Playing", now_playing)

# YouTube trailer (Optional - embed for 1st trending movie)
if trending and 'title' in trending[0]:
    query = trending[0]['title'] + " official trailer"
    st.markdown("### 🎞️ Featured Trailer")
    st.video(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
