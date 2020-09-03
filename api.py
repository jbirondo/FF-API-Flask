import flask 
from flask import request, jsonify, json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

pprplayers = open("ppr.json", "r")
halfpprplayers = open("halfppr.json", "r")
standardplayers = open("standard.json", "r")

pprdata = json.loads(pprplayers.read())
halfpprdata = json.loads(halfpprplayers.read())
standarddata = json.loads(standardplayers.read())

@app.route('/', methods=['GET'])
def home():
    return "<h1>VOR Fantasy Football API</h1>"

@app.route('/ppr', methods=['GET'])
def api_ppr():
    return json.dumps(pprdata)

@app.route('/standard', methods=['GET'])
def api_standard():
    return json.dumps(standarddata)

@app.route('/halfppr', methods=['GET'])
def api_halfppr():
    return json.dumps(halfpprdata)

app.run()
