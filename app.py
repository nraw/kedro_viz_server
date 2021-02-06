import os
import uuid

from flask import (Flask, render_template, request, send_file,
                   send_from_directory, session)
from flask_dropzone import Dropzone
from kedro_static_viz import static_viz

app = Flask(__name__, static_url_path="", static_folder="static")

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
    app.static_folder = "static"
    session_id = str(uuid.uuid4())
    if request.method == "POST":
        session_id = session["uid"]
        f = request.files.get("file")
        filename = session_id + ".json"
        file_path = os.path.join("pipes", filename)
        f.save(file_path)
        viz_directory = os.path.join("pipes", session_id)
        static_viz(
            load_file=file_path, directory=viz_directory, serve=False, browser=False
        )
    session["uid"] = str(uuid.uuid4())
    return render_template("cover.html", session_id=session["uid"])


@app.route("/pipeline/<name>")
def pipeline(name):
    print(name)

    viz_directory = os.path.join("pipes", name)
    app.static_folder = viz_directory
    return send_from_directory(viz_directory, "index.html")


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
