from flask import Flask, render_template, request
from controllers.substance import Substance

app = Flask(__name__)

substanceController = Substance()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/substances/new")
def newSubstance():
    return render_template('create.html')

@app.route("/api/substances", methods=["POST"])
def createSubstance():
    substanceController.create(request.form)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
