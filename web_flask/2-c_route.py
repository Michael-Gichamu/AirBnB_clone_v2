#!/usr/bin/python3
"""
Starts a Flask web app
Listening on 0.0.0.0, port 5000
Route:
    /: display “Hello HBNB!"
    /hbnb: display “HBNB”
    /c/<text> - display "C <text>"
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_func(text):
    """Display “C ” followed by the value of the text variable"""
    text = text.replace("_", " ")
    return f"C {text}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
