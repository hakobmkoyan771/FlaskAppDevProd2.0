#!/usr/bin/python3
import argparse
from flask import Flask

app = Flask(__name__)

@app.route("/")
<<<<<<< HEAD
def hello():
    return "Hello!"
=======
def main():
    return "Main Page"
>>>>>>> 7e37c2b (.)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pass debug variable')
    parser.add_argument('--deb', required=True, type=bool, help='boolean debug argument')
    args = parser.parse_args()
    app.debug = args.deb
    app.run(host="0.0.0.0", port="5050")    
