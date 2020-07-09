from flask import Flask, request
from flask_cors import CORS
from helpers.allCategories import game_dict
import json 

app = Flask(__name__)
cors = CORS(app, resources={r"/*":{"origins": "*"}})

# input ===> Game or all games, Range or by default, Links or None
@app.route('/', methods=['GET', 'POST'])
def customVideos():
    game = request.json
    # print(game['data'])
    # return game['data']

@app.route('/supported_games', methods=['GET'])
def supported_games():
    # will get all games from game_dict and return back to ui
    games = [x for x in game_dict.keys()]
    
    return json.dumps(games)

@app.route('/submitForm', methods=['POST', 'GET'])
def submitForm():
    # submitting form to create video