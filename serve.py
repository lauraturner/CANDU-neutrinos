from flask import Flask, jsonify, render_template, request           # import flask
import calc

app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
def index():                     
    return render_template("index.html") 

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
	data = request.form.to_dict(flat=False)
	reactors = data['reactors[]']
	start = data['start'][0]
	end = data['end'][0]
	# calc.main(start, end, reactors)
	return data

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the flask app