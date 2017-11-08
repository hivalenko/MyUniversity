from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<div style="text-align: center;"> <h1>HALLOU!!1 </h1></div> '
