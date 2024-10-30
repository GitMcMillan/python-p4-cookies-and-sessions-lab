#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return jsonify(articles), 200

@app.route('/articles/<int:id>')
def show_article(id):
# if this is first request, session views should equal 0
    #for every request to this route, session value +1
    session['page_views'] = session.get('page_views', 0) + 1

#if session view is <= 3, render JSON response with article
    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if article:
            return jsonify(article.to_dict()), 200
        else:
            return {'message': 'Article not found'}, 404
    #if views is > 3, render JSON respoinse with error messaage and  401 status code
    else:
        return{'message': 'Maximum pageview limit reached'}, 401


    

if __name__ == '__main__':
    app.run(port=5555)
