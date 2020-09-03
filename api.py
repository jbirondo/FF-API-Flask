import os
import datetime
import flask
import flask_cors
from flask import request, jsonify, json
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = False

CORS(app, supports_credentials=True)

pprplayers = open("ppr.json", "r")
halfpprplayers = open("halfppr.json", "r")
standardplayers = open("standard.json", "r")

pprdata = json.loads(pprplayers.read())
halfpprdata = json.loads(halfpprplayers.read())
standarddata = json.loads(standardplayers.read())

ppr_json = '{ "format": "ppr", "rankings": ' + json.dumps(pprdata, indent=4, separators=(
    ",", ": ")) + ", 'Time Updated': " + '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()) + "}"

halfppr_json = '{ "format": "standard", "rankings": ' + json.dumps(halfpprdata, indent=4, separators=(
    ",", ": ")) + ", 'Time Updated': " + '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()) + "}"

standard_json = '{ "format": "standard", "rankings": ' + json.dumps(standarddata, indent=4, separators=(
    ",", ": ")) + ", 'Time Updated': " + '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()) + "}"


@app.route('/', methods=['GET'])
def home():
    return "<h1>VOR Fantasy Football API</h1>"

@app.route('/ppr', methods=['GET'])
def api_ppr():
    return ppr_json

@app.route('/halfppr', methods=['GET'])
def api_halfppr():
    return halfppr_json    

@app.route('/standard', methods=['GET'])
def api_standard():
    return standard_json

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
