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
    return render_template('daily_page.html', word=word)

@app.route('/attemptDaily')
def attempt_daily():
    session_id = request.cookies.get('session_id')
    if session_id:
        current_session = db.session.get(models.Session, session_id)
        return current_session.attempt1
    else:
        session_id = "456"
        new_session = models.Session(session_id = session_id, solution = "tests", attempt1 = "t1e0s0t0s0")
        db.session.add(new_session)
        db.session.commit()
        response = make_response("New session should have been created and cookie should be set")
        response.set_cookie('session_id', session_id)
        return response

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    stage = data['stage']
    letters = data['data']
    session_id = request.cookies.get('session_id')
    current_session = db.session.get(models.Session, session_id)
    solution = current_session.solution
    (response_stage, response_letters, won) = game.check_guess(stage, letters, solution)
    response = {'stage': response_stage, 'letters': response_letters}
    return response