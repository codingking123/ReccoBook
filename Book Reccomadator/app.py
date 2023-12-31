import pickle

import numpy as np
import pandas as pd
from flask import Flask, redirect, url_for, render_template, request, abort

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books_dict = pickle.load(open('books_dict.pkl', 'rb'))
books = pd.DataFrame(books_dict)
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
# books['Book-Title']=books['Book-Title'].lower()


app = Flask(__name__)  # installaling a flask object


@app.route('/')  # defining a route in the application
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/team')
def team_ui():
    return render_template('team.html')


@app.route('/failure')
def failure_ui():
    return render_template('failure.html')


@app.route('/success')
def success_ui():
    return render_template('success.html')

    # change from here to 


@app.route('/signin', methods=['post'])
def signin():
    if request.method == 'post':
        if request.form['user_email'] == 'user_email':
            return redirect(url_for('success'))
        else:
            abort(401)
    else:
        return render_template('success.html')
    # here


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # index = np.where(pt.index == user_input)[0][0]
    # similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    # data = []
    # for i in similar_items:
    #     item = []
    #     temp_df = books[books['Book-Title'] == pt.index[i[0]]]
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
    #     data.append(item)

    # print(data)

    # return render_template('recommend.html',data=data)

    user_input = user_input.lower()
    data = []
    try:
        if (user_input == books['Book-Title'].values).any():
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
                item.extend(list(popular_df['avg_rating'].values))

                # rating=list(popular_df['avg_rating'].values)

                data.append(item)
        if len(data) > 0:
            return render_template('recommend.html', data=data)
        else:
            return render_template('failure.html')
    except:
        pass
    else:
        if ((user_input != books['Book-Title']).all()):
            print("No book found")

    print(data)

    return render_template('recommend.html', data=data)


@app.route('/contact')
def contact_ui():
    return render_template('contact.html')


# return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)  # lanunched webserver
