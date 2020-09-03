import flask 
from flask import request, jsonify, json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

players = open("index.json", "r")
pprdata = json.loads(players.read())

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/all', methods=['GET'])
def api_all():
    return json.dumps(pprdata)

app.run()
