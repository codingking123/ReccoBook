import pickle

import numpy as np
import pandas as pd
import streamlit as st
from app import app
from flask import redirect, url_for, render_template, request, abort

# popular_df = pickle.load(open('popular.pkl', 'rb'))
# pt = pickle.load(open('pt.pkl', 'rb'))

st.title('ReccoBook')
books_dict = pickle.load(open('books_dict.pkl', 'rb'))
books = pd.DataFrame(books_dict)
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

books_dict = books_dict['Book-Title'].values
selected_book_name = st.selectbox(
    'Type or select a book name from the dropdown',
    books_dict)

if st.button('Recommend'):
    recommended_books_names, recommended_books_images = recommend(selected_book_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_books_names[0])
        st.image(recommended_books_images[0])
    with col2:
        st.text(recommended_books_names[1])
        st.image(recommended_books_images[1])
    with col3:
        st.text(recommended_books_names[2])
        st.image(recommended_books_images[2])
    with col4:
        st.text(recommended_books_names[3])
        st.image(recommended_books_images[3])
    with col5:
        st.text(recommended_books_names[4])
        st.image(recommended_books_images[4])


        def fetch_images(books_id):
            pass


        # @app.route('/recommend_books', methods=['post'])
        def recommend():
            index = books[books['Book-Title'] == books].index[0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), reverse=True, key=lambda x: x[1])
            recommended_books_names = []
            recommended_books_images = []
            for i in similar_items[1:6]:
                books_id = books.iloc[i[0]].books_id
                recommended_books_images.append(fetch_images(books_id))
                recommended_books_names.append(books.iloc[i[0]].books)

            return recommended_books_names, recommended_books_images

# @app.route('/')  # defining a route in the application
# def index():
#     return render_template('index.html',
#                            book_name=list(popular_df['Book-Title'].values),
#                            author=list(popular_df['Book-Author'].values),
#                            image=list(popular_df['Image-URL-M'].values),
#                            votes=list(popular_df['num_ratings'].values),
#                            rating=list(popular_df['avg_rating'].values)
#                            )

#
# @app.route('/team')
# def team_ui():
#     return render_template('team.html')
#
#
# @app.route('/failure')
# def failure_ui():
#     return render_template('failure.html')
#
#
# @app.route('/success')
# def success_ui():
#     return render_template('success.html')
#
#     # change from here to
#
#
# @app.route('/signin', methods=['post'])
# def signin():
#     if request.method == 'post':
#         if request.form['user_email'] == 'user_email':
#             return redirect(url_for('success'))
#         else:
#             abort(401)
#     else:
#         return render_template('success.html')
#     # here
#
#
# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')


#
# @app.route('/contact')
# def contact_ui():
#     return render_template('contact.html')
