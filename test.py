# NOTE: Do not modify.
from ai import *
import time

def read_sol_line(line):
    split = line.split(" ")
    sol_direction = int(split[0])
    sol_score = float(split[1])

    return sol_direction, sol_score

def print_test_result(result, item):
    if result:
        print("PASSED: Correct {}.".format(item))
    else:
        print("FAILED: Incorrect {}.".format(item))

TOL = 0.001
def test(board_file='test_states', sol_file='test_sols'):
    game = Game()
    with open(board_file) as file:
        state_lines = file.readlines()

    with open(sol_file) as file:
        sol_lines = file.readlines()

    for i in range(len(state_lines)):
        print("Test {}/{}:".format(i + 1, len(state_lines)))
        game.load_state_line(state_lines[i])
        ai = AI(game.current_state())
        ai.build_tree(ai.root, ai.search_depth)
        direction, score = ai.expectimax(ai.root)

        sol_direction, sol_score = read_sol_line(sol_lines[i])

        print_test_result((score >= sol_score - TOL) and score <= (sol_score + TOL), "expected score")

def get_best_tile(tile_matrix):
    best_tile = 0
    for i in range(0, len(tile_matrix)):
        for j in range(0, len(tile_matrix[i])):
            tile = tile_matrix[i][j]
            if tile > best_tile:
                best_tile = tile
    return best_tile

NUM_TESTS = 10
REQ_PASSES = 4
MIN_SCORE = 20000
TIME_LIMIT = 30

def test_ec():
    game = Game()
    print("Note: each test may take a while to run.")
    passes = 0
    for i in range(NUM_TESTS):
        random.seed(i)
        start = time.time()
        print("Test {}/{}:".format(i + 1, NUM_TESTS))
        game.set_state()
        while not game.game_over():
            ai = AI(game.current_state())
            direction = ai.compute_decision_ec()
            game.move_and_place(direction)
            current = time.time()
            elapsed = current - start
            if elapsed > TIME_LIMIT:
                print("\tTime limit of {} seconds broken. Exiting...".format(TIME_LIMIT))
                break
        print("\tScore/Best Tile: {}/{}".format(game.score, get_best_tile(game.tile_matrix)))
        if game.score >= MIN_SCORE:
            print("\tSUFFICIENT")
            passes += 1
        else:
            print("\tNOT SUFFICIENT (score less than {})".format(MIN_SCORE))

    if passes < REQ_PASSES:
        print("FAILED (less than {} passes)".format(REQ_PASSES))
    else:
        print("PASSED")

