from flask import render_template, request, jsonify, session, send_file, make_response
import random
from WordleRoyale import app, db, models, util, game
from flask_security import current_user, auth_required


@app.route('/')
def index():

    return render_template('home.html')

@app.route('/daily')
def daily_page():
    session_cookie = request.cookies.get('session_id')
    initial_data = game.get_initial_data_daily(session_cookie)
    if initial_data['status'] == 'won':
        game.try_update_streak()

    word = game.get_daily_word()
    return render_template('daily_page.html', word=word, initial_data=initial_data)

@app.route('/ranked')
@auth_required('token', 'session')
def ranked_page():
    initial_data = game.get_initial_data_ranked()

    session_for_word = models.RankedSession.query.get(current_user.get_id())
    word = session_for_word.solution

    return render_template('ranked_page.html', word=word, initial_data=initial_data)

@app.route('/leaderboard')
def leaderboard_page():
    (top20, user_score) = game.get_leaderboard()
    print(user_score)
    print(len(top20))
    return render_template('leaderboard.html', top20=top20, user_score=user_score)

@app.route('/api/validWord', methods=['POST'])
def valid_word():
    return str(game.validate_word(request.get_json()))

@app.route('/api/solve/daily', methods=['POST'])
def solve_daily():
    session_cookie = request.cookies.get('session_id')
    if not session_cookie:
        session_id = util.get_unique_id()
        game.initiate_new_daily_game(session_id)
    else:
        session_id = session_cookie

    data = request.get_json()
    (response_stage, response_letters, response_status) = game.solve_daily(session_id, data)
    response = make_response({'status': response_status, 'stage': response_stage, 'letters': response_letters})
    response.set_cookie('session_id', session_id, expires= util.get_next_midnight() )
    return response

@app.route('/api/solve/ranked', methods=['POST'])
@auth_required('token', 'session')
def solve_ranked():
    data = request.get_json()
    (stage, letters, status, increase) = game.solve_ranked(data)
    return make_response({'status': status, 'stage': stage, 'letters': letters, 'increase': increase})

@app.route('/api/streak/getStreak')
def streak_get():
    if not current_user.is_authenticated:
        return str(-1)
    return str(game.retrieve_user_streak(current_user.get_id()))

@app.route('/api/score/getScore')
def score_get():
    ( _, user_score) = game.get_leaderboard()
    return jsonify(user_score)

@app.route('/api/getDailySolution')
def get_daily_solution():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return '-'
    solution = game.get_daily_solution(session_id)
    return solution

@app.route('/api/getRankedSolution')
def get_ranked_solution():
    solution = game.get_ranked_solution()
    return solution

@app.route('/api/newRankedGame')
def new_ranked_game():
    initial_data = game.get_initial_data_ranked(new_game = True)
    return jsonify(initial_data)