import datetime
import random
import uuid


def get_next_midnight():
    now = datetime.datetime.now()
    tomorrow_midnight = datetime.datetime.combine(
        now.date() + datetime.timedelta(days=1),
        datetime.datetime.min.time()
    )
    return tomorrow_midnight

def get_date_string():
    current_date = datetime.datetime.now()
    return f'{current_date.year}-{current_date.month}-{current_date.day}'

def matching_string_to_letters(matching):
    letters_stage = []
    pieces = [matching[i:i + 2] for i in range(0, len(matching), 2)]

    for piece in pieces[0:5]:
        letters_stage.append({'letter': piece[0], 'status': piece[1]})
    return letters_stage

def split_word_matching(combination):
    word = []
    matching = []
    for entry in combination:
        word.append(entry['letter'])
        matching.append(entry['status'])

    return word, matching

def combine_word_matching(word, matching):
    if len(word) != len(matching):
        return None

    combination = []
    for position in range(len(matching)):
        combination.append({'letter': word[position], 'status': matching[position]})

    return combination

def get_unique_id():
    unique_id = uuid.uuid4()
    return str(unique_id)

def attempt_string_from_letters(letters, stage):
    attempt = letters[stage]
    attempt_string = ''
    for letter in attempt:
        attempt_string += letter['letter'] + str(letter['status'])
    return attempt_string