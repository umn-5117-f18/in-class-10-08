import io
import os

from flask import Flask, abort, flash, jsonify, redirect, render_template, \
    request, send_file, url_for
import psycopg2
from werkzeug.utils import secure_filename

import db

app = Flask(__name__)
app.secret_key = "a_secret_key"

@app.before_first_request
def initialize():
    db.setup()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route('/')
def home():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT img_id, filename FROM images order by img_id desc")
        images = [record for record in cur]
    return render_template("home.html", images=images)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['png', 'jpg']

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash("no file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("no selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # convert the flask object to a regular file object
        data = request.files['file'].read()

        with db.get_db_cursor(commit=True) as cur:
            # we are storing the original filename for demo purposes
            # might be useful to also/instead save the file extension or mime type
            cur.execute("insert into images (filename, img) values (%s, %s)",
                (filename, data))
    return redirect(url_for("home"))


@app.route('/img/<int:img_id>')
def serve_img(img_id):
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM images where img_id=%s", (img_id,))
        image_row = cur.fetchone()

        # in memory binary stream
        stream = io.BytesIO(image_row["img"])

        return send_file(
            stream,
            attachment_filename=image_row["filename"])


if __name__ == '__main__':
    pass
