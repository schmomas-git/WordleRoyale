from WordleRoyale import util, db, models
import random

def check_guess(stage, letters, solution):

    #TODO logic
    current_attempt = letters[stage]
    (word, _) = util.split_word_matching(current_attempt)
    (matched_word, matching) = match_word(word, solution)
    matched_attempt = util.combine_word_matching(matched_word, matching)
    letters[stage] = matched_attempt

    return stage +1, letters, False

def match_word(word, solution):
    if len(word) == 5 and len(solution) == 5:
        sol_letter_dict = {}
        for letter in solution:
            if(sol_letter_dict.get(letter)) is None:
                sol_letter_dict[letter] = 1
            else:
                sol_letter_dict[letter] += 1

        #Matching for exact hits first
        matching = [-1,-1,-1,-1,-1]
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
    seed = util.get_date_string() + 'WordleRoyale1s7he8est'
    rng = random.Random(seed)
    rows = db.session.query(models.Word).count()
    index = rng.randrange(1, rows)
    word = models.Word.query.get(index)
    return str(word.word).upper()

def initiate_new_daily_game(session_id):
    solution = get_daily_word()
    new_session = models.DailySession(session_id=session_id, solution=solution, status='running')
    db.session.add(new_session)
    db.session.commit()

def solve_daily(session_id, stage, letters):
    session = models.DailySession.query.get(session_id)
    solution = session.solution
    (new_stage, new_letters, won) = check_guess(stage, letters, solution)
    attempt_string = util.attempt_string_from_letters(new_letters, stage)
    '''
    match stage:
        case 1:
            session.attempt1 = attempt_string
            pass
        case 2:
            session.attempt2 = attempt_string
            pass
        case 3:
            session.attempt3 = attempt_string
            pass
        case 4:
            session.attempt4 = attempt_string
            pass
        case 5:
            session.attempt5 = attempt_string
            pass
        case 6:
            session.attempt6 = attempt_string
            pass
    '''
    return new_stage, new_letters, won

def get_initial_letters_daily(session_id):
    letters = []
    session = models.DailySession.query.get(session_id)
    attempts = [session.attempt1, session.attempt2, session.attempt3, session.attempt4, session.attempt5,
                session.attempt6]
    for attempt in attempts:
        print(attempt)
