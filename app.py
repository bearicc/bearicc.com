from flask import Flask, render_template
import sys
import logging

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
else:
    logging.basicConfig(stream=sys.stderr)
