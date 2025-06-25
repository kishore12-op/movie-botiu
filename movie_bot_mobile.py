import streamlit as st
import requests

API_KEY = 'YOUR_TMDB_API_KEY'  # Replace this with your actual TMDb API key

def get_movie_info(movie_name):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}'
    search_response = requests.get(search_url).json()

    if not search_response['results']:
        return None

    movie = search_response['results'][0]
    movie_id = movie['id']
    details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    details_response = requests.get(details_url).json()

    title = movie.get('title', 'N/A')
    overview = movie.get('overview', 'No overview available.')
    release = movie.get('release_date', 'Unknown')
    poster_path = movie.get('poster_path', '')
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    rating = details_response.get('vote_average', 'N/A')
    genres = [g['name'] for g in details_response.get('genres', [])]
    runtime = details_response.get('runtime', 'N/A')

    tmdb_link = f"https://www.themoviedb.org/movie/{movie_id}"

    return {
        'title': title,
        'overview': overview,
        'release': release,
        'poster_url': poster_url,
        'rating': rating,
        'genres': genres,
        'runtime': runtime,
        'link': tmdb_link
    }

# Streamlit UI
st.set_page_config(
    page_title="🎬 Movie Bot",
    layout="centered",
)

st.markdown("<h2 style='text-align: center;'>🎥 Movie Info Chatbot</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter a movie name to get info, poster, and legal links.</p>", unsafe_allow_html=True)

movie_name = st.text_input("🎞️ Movie Name", placeholder="e.g. Interstellar")

if movie_name:
    with st.spinner("🔍 Searching..."):
        result = get_movie_info(movie_name)

    if result:
        st.image(result['poster_url'], use_column_width=True)
        st.markdown(f"### {result['title']}")
        st.markdown(f"📅 **Release Date:** {result['release']}")
        st.markdown(f"⭐ **Rating:** {result['rating']}")
        st.markdown(f"🎭 **Genres:** {', '.join(result['genres'])}")
        st.markdown(f"⏱️ **Runtime:** {result['runtime']} minutes")
        st.markdown(f"📝 {result['overview']}")
        st.markdown(f"[🔗 View on TMDb]({result['link']})")

        st.markdown("---")
        st.markdown("### 🎬 Watch Free Legal Movies:")
        st.markdown("- [📺 YouTube Free Movies](https://www.youtube.com/movies)")
        st.markdown("- [🍿 Tubi TV](https://tubitv.com)")
        st.markdown("- [🎞️ Public Domain Movies](https://publicdomainmovies.net)")
    else:
        st.error("❌ Movie not found. Try another name.")
