import io
from controllers.synonyms import Synonym
from controllers.groups import Group
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from werkzeug.wsgi import wrap_file
from controllers.substance import Substance
from controllers.images import Image

app = Flask(__name__)

substanceController = Substance()
imageController = Image()
groupController = Group()
synonymController = Synonym()

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
        substances = substanceController.findByTitle(
            query
        )
    else:
        substances = substanceController.findAll()
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
    return render_template('edit.html', substance=substanceController.find(id))

@app.route("/api/substances", methods=["GET", "POST"])
def createSubstance():
    if request.method == "GET":
        return jsonify(substanceController.findAll())
    elif request.method == "POST":
        substance_id = substanceController.create(request.form)
        imageController.create(request.files, substance_id)
        groupController.create(substance_id, request.form)
        synonymController.create(substance_id, request.form)
        return redirect(url_for('allSubstances'))

@app.route("/api/substances/del/<id>")
def delSubstance(id):
    print(substanceController.delete(id))
    return redirect(url_for('allSubstances'))

@app.route("/api/substances/<id>", methods=["POST"])
def updateSubstance(id):
    if request.method == "POST":
        updateRes = substanceController.update(request.form, id)
        if 'images' in request.files.keys():
            updateRes = imageController.update(request.files, id)
        if updateRes is not True:
            print(f"Error in Update: {updateRes}")
            return {"error": "Update caused error"}
        else:
           return redirect(url_for('allSubstances'))

@app.route("/api/images/<id>")
def getImage(id):
    file = imageController.find(id)
    return send_file( 
            io.BytesIO(
                file["content"]
            )
        ,
        mimetype=file["mimetype"],
    )

if __name__ == "__main__":
    app.run(debug=True)
