import pickle

import pandas as pd
import streamlit as st
import requests

st.title('Movie Recommend System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1449514548b90162ca33db81bf97ba9c'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

selected_movie_name = st.selectbox(
    'Movies',
    movies['title'].values
)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_poster

if st.button('Recommend'):
    name,poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])
