import datetime
import random
import uuid


def get_date_string():
    current_date = datetime.datetime.now()
    return f'{current_date.year}-{current_date.month}-{current_date.day}'

def get_daily_index():
    seed = get_date_string() + 'WordleRoyale1s7he8est'
    rng = random.Random(seed)
    index = rng.randrange(1, 336)
    return index

def combine_word_matching_string(word, matching):
    if len(word) != len(matching):
        return None

    combination = []
    for position in range(len(matching)):
        combination.append(word[position] + matching[position])

    return combination

def split_word_matching_string(combination):
    word = []
    matching = []
    for entry in combination:
        word.append(entry[0])
        matching.append(entry[1])

    return word, matching

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
    print(attempt_string)