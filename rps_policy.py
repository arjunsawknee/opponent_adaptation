from enum import Enum

class Action(Enum):
	ROCK = 0
	PAPER = 1
	SCISSORS = 2

class Result(Enum):
	DRAW = 0
	PLAYER_ONE = 1
	PLAYER_TWO = 2

class RPSPolicy:

	def __init__(self, name, move_function):
		self.name = name
		self.history = []
		self.move_function = move_function
		self.opponent_history = []

	def get_next_move(self):
		next_action = self.move_function(self.history, self.opponent_history)
		self.history.append(self.convert_index_to_action(next_action))
		return self.convert_index_to_action(next_action)

	def update_opponent_history(self, opp_action):
		self.opponent_history.append(opp_action)

	def convert_index_to_action(self, index):
		if index == 0:
			return Action.ROCK
		elif index == 1:
			return Action.PAPER
		elif index == 2:
			return Action.SCISSORS
		else:
			return None

	def reset_policy(self):
		self.history = []
		self.opponent_history = []

def simulate_turn(action_one, action_two):
	if action_one == action_two:
		return Result.DRAW
	else:
		if (action_one == Action.ROCK and action_two == Action.SCISSORS) or (action_one == Action.PAPER and action_two == Action.ROCK) or (action_one == Action.SCISSORS and action_two == Action.PAPER):
			return Result.PLAYER_ONE
		else:
			return Result.PLAYER_TWO

def simulate_game(policy_one, policy_two, turns):
	player_one_wins = 0
	draws = 0
	player_two_wins = 0
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


name_rock = "fixed_rock"
def move_func_rock(history, opponent_history):
	return 0

name_paper = "fixed_paper"
def move_func_paper(history, opponent_history):
	return 1

fixed_rock_policy = RPSPolicy(name_rock, move_func_rock)
fixed_paper_policy = RPSPolicy(name_paper, move_func_paper)
simulate_game(fixed_rock_policy, fixed_paper_policy, 100)
