import streamlit as st
import pickle
import pandas as pd
import requests #for API handling
from urllib.request import urlopen
import cloudpickle as cp

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
ds = pd.DataFrame(movies_dict)

similarity = cp.load(urlopen('https://drive.google.com/file/d/1tmBWrdLOiwpKyHwBGsE1ORBkqBQztqEd/view?usp=drive_link'))

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=63327e3082fe5f1739b92a3c4d0a33e9&language=en-US')
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']


def recommend(movie):
    fil = (ds['title']==movie)
    index = ds[fil].index[0]
    lis = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])[1:6]
    posters = []
    recommended_movies = []
    for tup in lis:
        # movie_id = tup[0]
        recommended_movies.append(ds.loc[tup[0],'title'])
        #fetching poster
        movie_id = ds.loc[tup[0]]['id']
        posters.append(fetch_poster(movie_id))
    return recommended_movies,posters



st.title('Movie Recommender System')
choices = list(ds['title'].values)
choices.insert(0,'Select a movie')

# st.text()
selected_movie_name = st.selectbox(
'Which film do you want to be recommeded?',
choices
)

if st.button('Recommend'):
    # st.write(selected_movie_name)
    recommendation, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(recommendation[0])
        st.image(posters[0])

    with col2:
        st.subheader(recommendation[1])
        st.image(posters[1])

    with col3:
        st.subheader(recommendation[2])
        st.image(posters[2])

    with col4:
        st.subheader(recommendation[3])
        st.image(posters[3])

    with col5:
        st.subheader(recommendation[4])
        st.image(posters[4])

# API Key 63327e3082fe5f1739b92a3c4d0a33e9
# https://api.themoviedb.org/3/movie/75?api_key=63327e3082fe5f1739b92a3c4d0a33e9&language=en-US
