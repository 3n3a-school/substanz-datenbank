from flask import Flask, render_template, request, jsonify, redirect, url_for
from controllers.substance import Substance

app = Flask(__name__)

substanceController = Substance()

@app.route("/")
def index():
    return redirect(url_for('allSubstances'))

@app.route("/substances")
@app.route("/substances/")
def allSubstances():
    args = request.args
    query = ""
    if 'q' in args:
        query  = request.args.get('q')
        substances = substanceController.readByTitle(
            query
        )
    else:
        substances = substanceController.readAll()
    return render_template(
        'index.html', 
        substances=substances,
        query=query,
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
    return redirect(url_for('allSubstances'))

@app.route("/api/substances", methods=["GET", "POST"])
def createSubstance():
    if request.method == "GET":
        return jsonify(substanceController.readAll())
    elif request.method == "POST":
        substanceController.create(request.form)
        return redirect(url_for('allSubstances'))

@app.route("/api/substances/<id>", methods=["POST"])
def updateSubstance(id):
    if request.method == "POST":
        updateRes = substanceController.update(request.form, id)
        if updateRes is not True:
            print(f"Error in Update: {updateRes}")
            return {"error": "Update caused error"}
        else:
           return redirect(url_for('allSubstances'))
        
if __name__ == "__main__":
    app.run(debug=True)
