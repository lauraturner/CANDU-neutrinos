from flask import Flask, jsonify, render_template, request, redirect, url_for         # import flask
import app.main as main

app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
def index():                     
    return render_template("index.html") 

# route hit by the submit button to calculate neutrino spectrums 
# for the selected reactors and time period
@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
	if request.method == "POST":
		data = request.form.to_dict(flat=False)
		reactors = data['reactors[]']
		start = data['start'][0]
		end = data['end'][0]
		main.main(start, end, reactors)
		return url_for('results')
	

@app.route('/results')
def results():
	return render_template('graphs.html')

if __name__ == "__main__":        # on running python app.py
	app.run(debug=True)

