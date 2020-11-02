from enum import IntEnum
import numpy as np

class Action(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Result(IntEnum):
    DRAW = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class RPSPolicy:
    def __init__(self, name, move_function):
        self.name = name
        self.move_function = move_function
        self.history = []
        self.opponent_history = []

    def get_next_move(self):
        next_action = self.move_function(self.history, self.opponent_history)
        next_action = Action(next_action)
        self.history.append(next_action)
        return next_action

    def update_opponent_history(self, opp_action):
        self.opponent_history.append(opp_action)

    def reset_policy(self):
        self.history = []
        self.opponent_history = []

def simulate_turn(action_one, action_two):
    if action_one == action_two:
        return Result.DRAW
    else:
        if action_one == (action_two + 1) % 3:
            return Result.PLAYER_ONE
        else:
            return Result.PLAYER_TWO

def simulate_game(policy_one, policy_two, turns):
    player_one_wins = 0
    player_two_wins = 0
    draws = 0
    for _ in range(turns):
        player_one_action = policy_one.get_next_move()
        player_two_action = policy_two.get_next_move()
        policy_one.update_opponent_history(player_two_action)
        policy_two.update_opponent_history(player_one_action)
        winner = simulate_turn(player_one_action, player_two_action)
        if winner == Result.DRAW:
            draws += 1
        elif winner == Result.PLAYER_ONE:
            player_one_wins += 1
        else:
            player_two_wins += 1
    print("After simulating " + str(turns) + " turns of RPS, " + str(policy_one.name) + " won " + str(player_one_wins) + " games, " + str(policy_two.name) + " won " + str(player_two_wins) + " and " + str(draws) + " were draws")

def move_func_rock(history, opponent_history):
    return 0

def move_func_paper(history, opponent_history):
    return 1

def move_func_scissors(history, opponent_history):
    return 2

def move_func_copycat(history, opponent_history):
    if not opponent_history: return np.random.randint(3)	# random on the first turn
    last = opponent_history[-1]
    return last

def move_func_random(history, opponent_history):
    return np.random.randint(3)

def move_func_aggressive(history, opponent_history):
    if not opponent_history: return np.random.randint(3)	# random on the first turn
    last = opponent_history[-1]
    beat_last = (last + 1) % 3
    return beat_last

def move_func_passive(history, opponent_history):
    if not opponent_history: return np.random.randint(3)	# random on the first turn
    last = opponent_history[-1]
    lose_last = (last - 1) % 3
    return lose_last

fixed_rock_policy = RPSPolicy("fixed_rock", move_func_rock)
fixed_paper_policy = RPSPolicy("fixed_paper", move_func_paper)
fixed_scissors_policy = RPSPolicy("fixed_scissors", move_func_scissors)
copycat_policy = RPSPolicy("copycat", move_func_copycat)
random_policy = RPSPolicy("random", move_func_random)
aggressive_policy = RPSPolicy("aggressive", move_func_aggressive)
passive_policy = RPSPolicy("passive", move_func_passive)

policies = [
    fixed_rock_policy,
    fixed_paper_policy,
    fixed_scissors_policy,
    copycat_policy,
    random_policy,
    aggressive_policy,
    passive_policy,
]

for p1 in policies:
    for p2 in policies:
        if p1 == p2: continue
        simulate_game(p1, p2, 100)
