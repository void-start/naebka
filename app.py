from flask import Flask, send_from_directory

app = Flask(__name__)

FILES_DIR = "files"

@app.route("/download", methods=["GET"])
def download():
    filename = "test.zip"  # ← ЖЁСТКО ЗАДАНО
    return send_from_directory(
        directory=FILES_DIR,
        path=filename,
        as_attachment=True
    )

@app.route("/")
def health():
    return "OK"
