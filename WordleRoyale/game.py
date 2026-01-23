import datetime
from WordleRoyale import util, db, models, cleanup_daily_sessions
from WordleRoyale.cleanup_daily_sessions import last_cleanup
import random
from flask_security import current_user

empty_letters_stage = [{'letter': '', 'status': -1}, {'letter': '', 'status': -1}, {'letter': '', 'status': -1},
                       {'letter': '', 'status': -1}, {'letter': '', 'status': -1}]


def check_guess(stage, letters, solution):
    current_attempt = letters[stage]
    (word, _) = util.split_word_matching(current_attempt)
    (matched_word, matching) = match_word(word, solution)
    matched_attempt = util.combine_word_matching(matched_word, matching)
    letters[stage] = matched_attempt

    won = True if [2,2,2,2,2] == matching else False
    status = 'won' if won else 'lost' if stage + 1 >= 6 else 'running'
    return stage + 1, letters, status

def match_word(word, solution):
    if len(word) == 5 and len(solution) == 5:
        sol_letter_dict = {}
        for letter in solution:
            if(sol_letter_dict.get(letter)) is None:
                sol_letter_dict[letter] = 1
            else:
                sol_letter_dict[letter] += 1

        #Matching for exact hits first
        matching = [0,0,0,0,0]
        for position in range(5):
            if word[position] == solution[position]:
                matching[position] = 2
                sol_letter_dict[word[position]] -= 1

        #Then matching for wrong positions
        for position in range(5):
            if matching[position] != 2:
                entry = sol_letter_dict.get(word[position])
                if entry is not None and entry > 0:
                    sol_letter_dict[word[position]] -= 1
                    matching[position] = 1

        return word, matching

    else:
        return None


def get_daily_word():
    seed = util.get_date_string() + 'WordleRoyale1s7he8estInTheWholeWorld!'
    rng = random.Random(seed)
    rows = db.session.query(models.Word).count()
    index = rng.randrange(1, rows)
    word = models.Word.query.get(index)
    return str(word.word).upper()

def get_random_word():
    rng = random.Random()
    rows = db.session.query(models.Word).count()
    index = rng.randrange(1, rows)
    word = models.Word.query.get(index)
    return str(word.word).upper()

def initiate_new_daily_game(session_id):
    solution = get_daily_word()
    new_session = models.DailySession(session_id=session_id, solution=solution, status='running')
    db.session.add(new_session)
    db.session.commit()

def initiate_new_ranked_game(user_id):
    solution = get_random_word()
    new_session = models.RankedSession(user_id=user_id, solution=solution, status='running')
    db.session.add(new_session)
    db.session.commit()

def solve_with_session(session, data):
    stage, letters = data['stage'], data['letters']
    solution = session.solution
    (new_stage, new_letters, new_status) = check_guess(stage, letters, solution)
    attempt_string = util.attempt_string_from_letters(new_letters, stage)
    match stage:
        case 0:
            session.attempt1 = attempt_string
        case 1:
            session.attempt2 = attempt_string
        case 2:
            session.attempt3 = attempt_string
        case 3:
            session.attempt4 = attempt_string
        case 4:
            session.attempt5 = attempt_string
        case 5:
            session.attempt6 = attempt_string
    session.status = new_status
    if new_status == 'won':
        try_update_streak()
    db.session.commit()
    return new_stage, new_letters, new_status


def cleanup():
    db.session.query(models.DailySession).filter(models.DailySession.solution != get_daily_word()).delete()
    db.session.commit()
    cleanup_daily_sessions.last_cleanup = datetime.datetime.now()


def solve_daily(session_id, data):
    if cleanup_daily_sessions.last_cleanup is None or cleanup_daily_sessions.last_cleanup + datetime.timedelta(hours=24) < datetime.datetime.now():
        cleanup()
    session = models.DailySession.query.get(session_id)
    return solve_with_session(session, data)

def solve_ranked(data):
    increase = 0
    user_id = current_user.get_id()
    session = models.RankedSession.query.get(user_id)
    (stage, letters, status) = solve_with_session(session, data)
    if status != 'running':
        increase = apply_ranking(stage, status)
    return stage, letters, status, increase

def extract_session_attempts(session):
    letters = []
    stage = 0
    status = 'running'
    if session is not None:
        attempts = [session.attempt1, session.attempt2, session.attempt3, session.attempt4, session.attempt5,
                    session.attempt6]
        status = session.status
    else:
        attempts = [None] * 6
    for attempt in attempts:
        if attempt is not None:
            letters.append(util.matching_string_to_letters(attempt))
            stage += 1
        else:
            letters.append(empty_letters_stage)
    return letters, stage, status

def get_initial_data_daily(session_id):
    session = None
    if session_id is not None:
        session = models.DailySession.query.get(session_id)
    (letters,stage, status) = extract_session_attempts(session)
    return {'letters': letters, 'stage': stage, 'status': status}

def get_initial_data_ranked(new_game = False):
    user_id = current_user.get_id()
    session = models.RankedSession.query.get(user_id)
    if session is None:
        initiate_new_ranked_game(user_id)
        session = models.RankedSession.query.get(user_id)
    if (session.status == 'won'  or session.status == 'lost') and new_game:
        db.session.delete(session)
        initiate_new_ranked_game(user_id)
        session = models.RankedSession.query.get(user_id)

    (letters,stage, status) = extract_session_attempts(session)
    return {'letters': letters, 'stage': stage, 'status': status}

def validate_word(letters):
    word = ''
    for letter in letters:
        word += letter['letter']
    return models.Word.query.filter_by(word=word).first() is not None

def try_update_streak():
    now = datetime.datetime.now()
    zero_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    user_id = current_user.get_id()
    if user_id is None:
        return
    streak = models.Streak.query.get(user_id)
    if streak is None:
        #create one
        new_streak = models.Streak(user_id=user_id, count=1, last_update=zero_date)
        db.session.add(new_streak)
    else:
        if zero_date > streak.last_update:
            #last streak date is within the last day
            if zero_date - datetime.timedelta(days=1) <= streak.last_update:
                #raise count by one
                streak.count += 1
                streak.last_update = zero_date
            else:
                #reset count
                streak.count = 1
                streak.last_update = zero_date
    db.session.commit()


def retrieve_user_streak(user_id):
    streak = models.Streak.query.get(user_id)
    if streak is None:
        return -1
    else:
        return streak.count

def get_daily_solution(session_id):
    session = models.DailySession.query.get(session_id)
    if (session is not None) & (session.status != 'running'):
        return session.solution

    return '-'

def get_ranked_solution():
    user_id = current_user.get_id()
    session = models.RankedSession.query.get(user_id)
    if (session is not None) & (session.status != 'running'):
        return session.solution

    return '-'



def get_leaderboard():
    top20 = []
    user_score = {'username': '-', 'score': 0}
    scores = (
        models.Score.query
        .order_by(models.Score.score.desc())
        .all()
    )
    for score in scores[:20]:
        top20.append({'username':score.username,'score': score.score})
    if current_user.is_authenticated:
        individual_score = models.Score.query.get(current_user.get_id())
        if individual_score is not None:
            rank = next((i+1 for i, score in enumerate(scores) if score.user_id == individual_score.user_id), None)
            user_score = {'rank': rank, 'username': individual_score.username, 'score': individual_score.score}
        else:
            user_score = {'rank': -1,'username': current_user.username, 'score': 0}
    return top20, user_score

def create_new_leaderboard_user(user_id, username):
    score = models.Score(user_id=user_id, username=username, score=0)
    db.session.add(score)

def apply_ranking(stage, status):
    score = models.Score.query.get(current_user.get_id())
    if score is None:
        create_new_leaderboard_user(current_user.get_id(), current_user.username)
        score = models.Score.query.get(current_user.get_id())

    scoring = {
        1: 10,
        2: 7,
        3: 4,
        4: 3,
        5: 2,
        6: 1,
    }
    if status == 'lost':
        increase = -3
    else:
        increase = scoring.get(stage)
    score.score += increase
    db.session.commit()
    return increase