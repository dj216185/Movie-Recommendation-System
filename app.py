import streamlit as st
import pickle
import base64
import pandas as pd
import requests
import json


def fetch_tmdb_page(movie):
    base_url = "https://api.themoviedb.org/3"
    api_key = "775e17103186edaa11ddd7b33e965919"

    # Search for the movie
    search_url = f"{base_url}/search/movie?api_key={api_key}&query={movie.replace(' ', '+')}"
    response = requests.get(search_url)
    data = json.loads(response.text)

    # Check if the search returned any movies
    if data['results']:
        # Get the first movie from the results
        first_movie = data['results'][0]
        movie_id = first_movie['id']

        # Return the TMDB page for the movie
        return f"https://www.themoviedb.org/movie/{movie_id}"
    else:
        return "Movie not found on TMDB"

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=775e17103186edaa11ddd7b33e965919&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)


def recommendations(movies, genre):
    movie_indx = movies_tags[movies_tags['original_title'] == movies].index[0]
    distances = similarity[movie_indx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:11]
    movie_rec = []
    poster_rec = []
    for i in movies_list:
        movie_id = movies_tags.iloc[i[0]].id
        if genre in movies_tags.iloc[i[0]].genres:
            movie_rec.append(movies_tags.iloc[i[0]].original_title)
            poster_rec.append(fetch_poster(movie_id))

    return movie_rec, poster_rec


# Add a description

st.markdown("""
<style>
.markdown-text-container {
    background-color: rgba(255, 255, 255, 0.8);
    font-weight: bold;
}
input {
    -webkit-text-fill-color: white;
    -webkit-background-clip: text;
}
h1 {
    color: White;
}
.selectbox label {
    color: orange;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

set_background('Designer (4).png')
movie = pickle.load(open('movies_dict.pkl', 'rb'))
movies_tags = pd.DataFrame(movie)
mov = movies_tags['original_title'].values
genre = [
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Science Fiction",
    "Thriller",
    "TV Movie",
    "War",
    "Western"
]

st.markdown("""
    <h1 style="color: #022a30;">Feed Me A Movie</h1>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
        <h4 style="color: #4f5425;">Looking for your next movie to watch? 
        Our app recommends films based on your recent viewing. 
        Just input the last movie you watched, and we’ll suggest 
        similar ones, filtered by genre, director, and more. 
        Devesh asks: What’s the last movie you watched?</h4>
    </div>
    """, unsafe_allow_html=True)


similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_sel = st.selectbox(label='Select The Movie', options=mov,label_visibility= "visible" )

genre_sel = st.selectbox(label='Genre', options=genre,label_visibility= "visible" )

n = 0

# if st.button('Here are Some Movie realted to your recent movie. Enjoy!'):
#     recomend = recommendations(movie_sel,genre_sel)
#     for i in recomend:
#         n = n+1
#         st.markdown(f"""
#             <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
#                 <h6 style="color: #022a30;"> {i}</h6>
#             </div>
#             """, unsafe_allow_html=True)
#     if n == 0:
#         st.markdown(f"""
#                <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
#                    <h3 style="color: #022a30;">The Database will be Soon Updated !
#                                                 Search For Some Other Genre </h3>
#                </div>
#                """, unsafe_allow_html=True)
if st.button('Here are Some Movie related to your recent movie. Enjoy!'):
    movie_rec, poster_rec = recommendations(movie_sel, genre_sel)
    if movie_rec:
        for i in range(0, len(movie_rec), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(movie_rec):
                    imdb_link = fetch_tmdb_page(movie_rec[i+j])
                    with cols[j]:
                        st.markdown(f"""
                            <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
                                <h6 style="color: #022a30;"><a href="{imdb_link}" target="_blank">{movie_rec[i+j]}</a></h6>
                                <img src="{poster_rec[i+j]}" alt="Movie Poster" style="width:100%;">
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
               <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
                   <h3 style="color: #022a30;">The Database will be Soon Updated !
                                                Search For Some Other Genre </h3>
               </div>
               """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .reportview-container .main footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <footer>
        <p>Copyright © 2023 Devesh Jaluka</p>
    </footer>
    """, unsafe_allow_html=True)
