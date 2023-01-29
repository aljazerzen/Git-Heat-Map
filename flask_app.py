from flask import Flask, render_template, request
import databaseToJSON
import databaseToJSONFiltered
import glob

app = Flask(__name__)
app.static_folder = "static"

@app.route("/")
def index_page():
    db_list = [db[:-3] for db in glob.glob("*.db")]
    return render_template("index.html", db_list=db_list)

@app.route("/<name>")
def treemap_page(name):
    return render_template("treemap.html", name=name)

@app.route("/filetree/<name>.json")
def filetree_json(name):
    return databaseToJSON.get_json_from_db(f"{name}.db")

@app.route("/highlight/<name>.json")
def highight_json(name):
    params = {}
    emails = request.args.getlist("emails")
    params["emails"] = emails
    query, params = databaseToJSONFiltered.get_filtered_query(params)
    return databaseToJSON.get_json_from_db(f"{name}.db", query, params)

app.run(host='0.0.0.0')
