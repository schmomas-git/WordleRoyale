from WordleRoyale import game, util

def test_check_guess():

    stage = 1
    letters = [
        [{'letter':"E", 'status': -1},{'letter':"T", 'status': 1},{'letter':"W", 'status': -1},{'letter':"A", 'status': 2},{'letter':"S", 'status': 1}],
        [{'letter':"T", 'status': 0},{'letter':"E", 'status': 0},{'letter':"S", 'status': 0},{'letter':"T", 'status': 0},{'letter':"E", 'status': 0}],
        [{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0}],
        [{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0}],
        [{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0}],
        [{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0},{'letter':"", 'status': 0}],
    ]
    solution = 'TESTS'

    result = game.check_guess(stage, letters, solution)
    print(result)

def test_util_matching_string_to_letters(matching):
    result = util.matching_string_to_letters(matching)
    print(result)

if __name__ == '__main__':
    #test_check_guess()
    test_util_matching_string_to_letters('T2E2S2T2S2')

