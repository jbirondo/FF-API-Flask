import os
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

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
