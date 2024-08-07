from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "Hellow, flask"

@app.route("/hello")
def hello():
    return "Hello,World"