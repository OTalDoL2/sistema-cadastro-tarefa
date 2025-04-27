from flask import Flask
from Database import Database


app = Flask(__name__)

app.route('/')
def main():
    return '<h1>Hello World!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
