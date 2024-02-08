from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = "boomboom"

boggle_game = Boggle()

@app.route("/")
def home_page():
    """Shows board"""
    board = boggle_game.make_board()
    session["board"] = board
    high_score = session.get("high_score", 0)
    times_played = session.get("times_played", 0)
    return render_template("base.html", board = board, high_score = high_score, times_played = times_played)

@app.route("/check-guess")
def check_guess():
    """Checks if word is valid """
    guess = request.args.get("guess")
    board = session.get("board")
    result = boggle_game.check_valid_word(board, guess)
    
    # Return a valid response (in this case, a JSON response)
    return jsonify({"result": result})

@app.route("/post-score", methods=["POST"])
def post_score():
    """"""
    data = request.json
    #gets current score
    score = data.get("score")
    high_score = session.get("high_score",0)
    #sets new high score to the max of previous higscore or new score
    session["high_score"] = max(high_score, score)
    #update the number of times played
    times_played = session.get("times_played", 0)
    session["times_played"] = times_played + 1
    return jsonify({"high_score": session["high_score"], "times_played": session["times_played"]})