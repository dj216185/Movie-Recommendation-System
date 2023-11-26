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

if st.button('Here are Some Movie realted to your recent movie. Enjoy!'):
    recomend = recommendations(movie_sel,genre_sel)
    for i in recomend:
        n = n+1
        st.markdown(f"""
            <div style="background-color: rgba(240, 240, 240, 0.5); padding: 10px; border-radius: 10px;">
                <h6 style="color: #022a30;"> {i}</h6>
            </div>
            """, unsafe_allow_html=True)
    if n == 0:
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
