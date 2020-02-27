from flask import Flask           # import flask
from flask import render_template

app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
def index():                     
    return render_template("index.html") 

if __name__ == "__main__":        # on running python app.py
    app.run()                     # run the flask app