from WordleRoyale import util

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
