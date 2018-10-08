import os

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
import psycopg2

import db

app = Flask(__name__)

@app.before_first_request
def initialize():
    db.setup()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route('/')
def home():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM movie")
        movies = [record for record in cur]
    return render_template("home.html", movies=movies)

@app.route('/movies/<movie_id>')
def movie(movie_id):
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM movie where movie_id=%s", (movie_id,))
        movie = cur.fetchone()

    if not movie:
        return abort(404)

    return render_template("movie.html", movie=movie)

@app.route('/genres/<genre>')
def genre(genre):
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM movie where genre=%s", (genre,))
        movies = [record for record in cur]
    return render_template("home.html", movies=movies)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        # TODO flash
        redirect('home')

    with db.get_db_cursor() as cur:
        # XXX: hack for query wildcard characters w/ correct escaping
        query_wildcard = f"%{query}%"
        cur.execute("SELECT * FROM movie where title ilike (%s)", (query_wildcard,))
        movies = [record for record in cur]
    return render_template("home.html", movies=movies)


if __name__ == '__main__':
    pass
