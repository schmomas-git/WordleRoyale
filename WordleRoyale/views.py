from flask import render_template, request, jsonify, session, send_file, make_response
import random
from WordleRoyale import app, db, models, util, game



@app.route('/')
def index():
    id = random.Random().randint(1,336)
    word = db.session.get(models.Word, id)
    return f'Landing Page {id}: {word.word}'

@app.route('/daily')
def daily_page():
    word = db.session.get(models.Word, util.get_daily_index())
    session_cookie = request.cookies.get('session_id')
    if session_cookie:
        game.get_initial_letters_daily(session_cookie)
    return render_template('daily_page.html', word=word)

@app.route('/api/solve/daily', methods=['POST'])
def solve_daily():
    #checken, ob eine session vorhanden ist
    session_id = ''
    session_cookie = request.cookies.get('session_id')
    if not session_cookie:
        session_id = util.get_unique_id()
        game.initiate_new_daily_game(session_id)
    else:
        session_id = session_cookie

    data = request.get_json()
    stage = data['stage']
    letters = data['data']
    (response_stage, response_letters, won) = game.solve_daily(session_id, stage, letters)
    response = make_response({'stage': response_stage, 'letters': response_letters})
    response.set_cookie('session_id', session_id)
    return response