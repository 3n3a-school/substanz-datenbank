from flask import Flask, render_template, request, jsonify
from controllers.substance import Substance

app = Flask(__name__)

substanceController = Substance()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/substances")
def allSubstances():
    return render_template(
        'list.html', 
        substances=substanceController.readAll()
    )

@app.route("/substances/new")
def newSubstance():
    return render_template('create.html')

@app.route("/substances/edit/<id>")
def editSubstance(id):
    return render_template('edit.html', substance=substanceController.read(id))

@app.route("/substances/del/<id>")
def delSubstance(id):
    substanceController.delete(id)
    return f"deleted {id}"

@app.route("/api/substances", methods=["GET", "POST"])
def createSubstance():
    if request.method == "GET":
        return jsonify(substanceController.readAll())
    elif request.method == "POST":
        substanceController.create(request.form)
        return "success"

@app.route("/api/substances/<id>", methods=["POST"])
def updateSubstance(id):
    if request.method == "POST":
        substanceController.update(request.form, id)
        return "success"

if __name__ == "__main__":
    app.run(debug=True)
