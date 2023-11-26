import streamlit as st
import pickle
import base64
import pandas as pd


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


def recommendations(movie, genre):
    movie_indx = movies_tags[movies_tags['original_title'] == movie].index[0]
    distances = similarity[movie_indx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:11]
    movie_rec = []
    for i in movies_list:
        if genre in movies_tags.iloc[i[0]].genres:
            movie_rec.append(movies_tags.iloc[i[0]].original_title)

    return movie_rec


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

set_background('WallpaperDog-20493695.jpg')
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

st.title('Movie Recommender System')

st.markdown("""
<font size='4'><font color = 'White'>
Do you love watching movies but don’t know what to watch next? Don’t worry, we have the perfect app for you!
This app is like a magic wand that can find the best movies for you based on your recent preferences. 
Just tell us the name of the movie you watched recently, and we will show you a list of movies that match your taste.
Already filtered by the movie's genre, director, and more. Whether you are in the mood for a comedy, a thriller, or a romance, 
this app will help you find your next favorite movie. Just enter your recent movie and let the magic happen!<br>
Devesh wants to know: What movie did you watch recently ?
</font>
""", unsafe_allow_html=True)

similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_sel = st.selectbox(label='Select The Movie', options=mov,label_visibility= "visible" )

genre_sel = st.selectbox(label='Genre', options=genre,label_visibility= "visible" )

if st.button('Here are Some Movie realted to your recent movie. Enjoy!'):
    recomend = recommendations(movie_sel,genre_sel)
    for i in recomend:
        st.write(i)