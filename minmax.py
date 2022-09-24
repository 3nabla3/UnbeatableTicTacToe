from TTT import TTT
import os
import pickle

# TODO: fix the fucking bug


class MinMaxTree:
	def __init__(self, board, player, max_depth=3, delta=None, children=None):
		self.board = board
		self._score = None
		# who plays next given the current board (p1 or p2)
		self.player = player
		# the coordinates of the last played move (the difference between the parent node and this node)
		self.delta = delta

		# the convention is X (p1) tries to maximise and O (p2) tries to minimise
		self.is_maximising = self.player == TTT.P1

		self.max_depth = max_depth
		self.children: list[MinMaxTree] = children or []
		state = TTT.get_board_state(self.board)
		if state is TTT.GameState.IN_PROGRESS:
			self._generate_tree(max_depth)

	def avail_spaces_coord(self):
		for i, row in enumerate(self.board):
			for j, elem in enumerate(row):
				if elem == TTT.AVAIL:
					yield i, j

	def _generate_tree(self, max_depth):
		if max_depth == 0:
			return

		# when the computer generates the tree, it assumes it is playing next
		# child_n = 0
		for r, c in self.avail_spaces_coord():
			# print(f"Analyzing {child_n=} {max_depth=}")
			# child_n += 1
			potential_board = self.board.__copy__()
			potential_board[r, c] = self.player
			next_player = TTT.P1 if self.player == TTT.P2 else TTT.P2
			child = MinMaxTree(potential_board, next_player, max_depth - 1, delta=(r, c))
			self.add_child(child)

	def add_child(self, child):
		self.children.append(child)

	def get_score(self):
		if self._score is not None:
			return self._score
		self._calculate_score()
		return self._score

	def _calculate_score(self):
		if not self.children:
			# If the board has no empty spaces left, it must be a tie, or a win
			state = TTT.get_board_state(self.board)
			# If X (p1) wins, the score is +1 because X tries to maximise
			if state is TTT.GameState.P1_WON:
				self._score = 1
			# If O (p2) wins, the score is -1 because O tries to minimise
			elif state is TTT.GameState.P2_WON:
				self._score = -1
			# if it is a tie, the score is 0
			elif state is TTT.GameState.TIE:
				self._score = 0
			else:
				raise ValueError("Invalid board state")

		else:
			children_scores = (child.get_score() for child in self.children)
			if self.is_maximising:
				self._score = max(children_scores)
			else:
				self._score = min(children_scores)

	def best_move(self):
		if self.is_maximising:
			max_child = max(self.children, key=lambda c: c.get_score())
			return max_child.delta
		else:
			min_child = min(self.children, key=lambda c: c.get_score())
			return min_child.delta

	def _str(self, pref="Root"):
		""" Recursively prints the nodes and labeling them with the path from the root """

		res = f"Node {pref} -- next to play: {self.player} (score {self._score})\n"
		res += str(self.board) + "\n"

		for i, child in enumerate(self.children):
			res += child._str(pref=pref + f":{i}")
		return res

	def __str__(self):
		return self._str()


class TTTMinMax:
	""" Algorithm that decides the next move to play depending on the current board state"""
	root_tree_cache = None
	cache_file = 'root_tree_cache.pickle'

	def __init__(self, ttt, *, plays=None):
		self.ttt = ttt

		# by default, the algo plays P2
		plays = plays or TTT.P2

		# make sure the given player is valid
		if plays not in (self.ttt.P1, self.ttt.P2):
			raise ValueError("Invalid player")

		self.player = plays
		self.tree = None

	def generate_tree(self, max_depth=-1, *, optimise=True):
		# the tree is very long to generate when the algo is the first to play
		# when it plays second, the generation is relatively fast

		# if the algo is first to play
		if self.player == TTT.P1 and optimise:
			# try recovering from ram cache first
			if self.root_tree_cache is not None:
				print("Loading tree from ram cache...")
				self.tree = self.root_tree_cache
			# try recovering from disk cache next
			elif os.path.exists(self.cache_file):
				print("Loading tree from disk cache...")
				with open(self.cache_file, 'rb') as cache:
					self.tree = pickle.load(cache)

		# if we still need to generate the tree
		if self.tree is None:
			print("Generating tree...")
			self.tree = MinMaxTree(self.ttt.board.__copy__(), self.player, max_depth)
			# save it to cache if it is the big tree (when algo plays first)
			if self.player == TTT.P1 and optimise:
				print("Writing the tree to disk cache...")
				with open(self.cache_file, 'wb') as cache:
					pickle.dump(self.tree, cache)

		# if the big tree has not been writen to ram yet
		if self.player == TTT.P1 and self.root_tree_cache is None and optimise:
			print("Writing the tree to ram cache...")
			self.root_tree_cache = self.tree

		print("Done!")

	def find_next_move(self, *, optimise=True):
		if self.tree is None:
			self.generate_tree(optimise=optimise)

		# check if the tree's current board matches the actual current board
		if self.tree.board != self.ttt.board:
			# find the current game board within the children of the last board
			current = None
			for child in self.tree.children:
				if child.board == self.ttt.board:
					current = child
			assert current is not None
			self.tree = current

		move = self.tree.best_move()

		# update the tree so it reflects the chosen move
		current = None
		for child in self.tree.children:
			if child.delta == move:
				current = child
		assert current is not None
		self.tree = current

		return move


if __name__ == '__main__':
	def main():
		ttt = TTT()
		mm = TTTMinMax(ttt, plays=TTT.P2)
		ttt.main_loop(algo=mm, algo_plays=TTT.P2)

	main()
