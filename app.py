import json
import os
import uuid
from pathlib import Path

from flask import (Flask, redirect, render_template, request, send_file,
                   session, url_for)
from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy

import db.commands as commands
import db.database as database
from db.model import Model
from src.utils import check_if_exists, get_file_path

app = Flask(__name__, static_url_path="", static_folder="static")

app.config.from_object(os.environ.get("APP_SETTINGS", "config.DevelopmentConfig"))
database.init_app(app)
commands.init_app(app)

dropzone = Dropzone(app)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "hello"),
    SEND_FILE_MAX_AGE_DEFAULT=0,
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE=".json",
    DROPZONE_MAX_FILE_SIZE=20,
)


@app.route("/", methods=["POST", "GET"])
def upload():
    session_id = str(uuid.uuid4())
    if request.method == "POST":
        session_id = session["uid"]
        f = request.files.get("file")
        file_path = get_file_path(session_id)
        f.save(file_path)
        os.system(f"./scripts/copy_js.sh {session_id}")
        pipeline = Path(file_path).read_text()
        model = Model(session_id=session_id, pipeline=pipeline)
        database.db.session.add(model)
        database.db.session.commit()
    session["uid"] = str(uuid.uuid4())
    return render_template("cover.html", session_id=session["uid"])


@app.route("/pipeline/<name>")
def pipeline(name):
    print(name)
    print(request.url)
    _pipe_exists = check_if_exists(name)
    if not _pipe_exists:
        pipe = Model.query.filter_by(session_id=name).first()
        if not pipe:
            print("lolno")
            return redirect(url_for("upload"))
        else:
            print(pipe.pipeline)
            file_path = get_file_path(name)
            Path(file_path).write_text(pipe.pipeline)
            os.system(f"./scripts/copy_js.sh {name}")
    url = request.url
    return render_template("pipe.html", name=name, url=url)


@app.route("/example_pipeline")
def download_example():
    return send_file(
        "static/example_pipeline.json",
        mimetype="application/json",
        attachment_filename="example_pipeline.json",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
