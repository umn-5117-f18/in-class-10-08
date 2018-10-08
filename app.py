import os

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
import psycopg2
from werkzeug.utils import secure_filename

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
    app.logger.info("home")
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM movie")
        movies = [record for record in cur]
    return render_template("home.html", movies=movies)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['png', 'jpg']

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        app.logger.warn("no file part")
        # flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        # flash('No selected file')
        app.logger.warn("no selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        app.logger.info(f"ready to save file {filename}")
        data = request.files['file'].read()

        with db.get_db_cursor(commit=True) as cur:
            cur.execute("insert into images (filename, img) values (%s, %s)",
                (filename, data))

        #
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
    return redirect(url_for("home"))


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
