import flask 
from flask import request, jsonify, json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

pprplayers = open("ppr.json", "r")
pprdata = json.loads(pprplayers.read())

@app.route('/', methods=['GET'])
def home():
    return "<h1>VOR Fantasy Football API</h1>"


@app.route('/api/ppr', methods=['GET'])
def api_ppr():
    return json.dumps(pprdata)

app.run()
