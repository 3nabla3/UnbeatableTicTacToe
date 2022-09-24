from enum import Enum, auto


class InvalidInitialBoardException(ValueError):
	""" Exception used when the user gives an invalid initial state to the TTT game """

	def __init__(self, coord=None):
		self.coord = coord

	def __str__(self):
		return "Unexpected initial value" + f" at {self.coord}" if self.coord else ''


class InvalidCoordinateException(ValueError):
	""" Exception used when the user enters an invalid coordinate """

	def __init__(self, coord):
		self.coord = coord

	def __str__(self):
		return f"The coordinate {self.coord} is not in the range [0:0] to [2:2]"


class UnavailableCoordinateException(ValueError):
	""" Exception that occurs when the user enters a coordinate with an existing value """

	def __init__(self, coord, value):
		self.coord = coord
		self.value = value

	def __str__(self):
		return f"The coordinate {self.coord} already has the value {self.value}"


class Board:
	def __init__(self, initial=None):
		if initial:
			self.check_init_board(initial)

			for i, row in enumerate(initial):
				# if the board is a list of strings, convert it to a list of lists
				if isinstance(row, str):
					initial[i] = list(row)

		# if no initial state was given, set the board to a 3x3 empty grid
		self._board_elem = initial or [[TTT.AVAIL for _ in range(3)] for _ in range(3)]

	@staticmethod
	def check_init_board(init_board):
		""" Checks if the given initial board is valid """
		if len(init_board) != 3:
			raise InvalidInitialBoardException()

		valid = (TTT.P1, TTT.P2, TTT.AVAIL)
		for i, row in enumerate(init_board):
			if len(row) != 3:
				raise InvalidInitialBoardException()
			for j, elem in enumerate(row):
				if elem not in valid:
					raise InvalidInitialBoardException((i, j))

	def __getitem__(self, coord):
		r, c = coord
		return self._board_elem[r][c]

	def __setitem__(self, key, value):
		r, c = key
		# check that the coordinates are valid and the spot is free
		if not 0 <= r < 3 or not 0 <= c < 3:
			raise InvalidCoordinateException((r, c))
		if (val := self._board_elem[r][c]) != TTT.AVAIL:
			raise UnavailableCoordinateException((r, c), val)
		self._board_elem[r][c] = value

	def __iter__(self):
		return iter(self._board_elem)

	def __copy__(self):
		new_board = [row.copy() for row in self._board_elem]
		return Board(new_board)

	def __eq__(self, other):
		for row, other_row in zip(self, other):
			if row != other_row:
				return False
		return True

	def __str__(self):
		res = ""
		for row in self._board_elem:
			for elem in row:
				res += f'{elem}\t'
			res += '\n'
		return res


class TTT:
	""" Class that contains the TicTacToe game logic """
	P1 = 'x'
	P2 = 'o'
	AVAIL = '-'

	class GameState(Enum):
		""" Enum which contains the four possible game states """
		IN_PROGRESS = auto()
		TIE = auto()
		P1_WON = auto()
		P2_WON = auto()

	def __init__(self, *, init_board=None, starting=None):
		self._playing = starting or self.P1
		self.board = Board(init_board)
		self._state = self.GameState.IN_PROGRESS

	@property
	def playing(self):
		return self._playing

	@property
	def state(self):
		return self._state

	@staticmethod
	def get_board_state(board):
		""" Static method used to analyse a given board, used by the minmax algo """
		temp = TTT()
		temp.board = board
		temp.update_state()
		return temp.state

	def check_won(self, player):
		""" Check if the given player has three in a row """
		# check rows
		for row in self.board:
			if row.count(player) == 3:
				return True

		# check column
		for col in range(3):
			count = 0
			for i in range(3):
				if self.board[i, col] == player:
					count += 1
			if count == 3:
				return True

		# check diags
		count1 = 0
		count2 = 0
		for i, row in enumerate(self.board):
			if row[i] == player:
				count1 += 1
			if row[2 - i] == player:
				count2 += 1
		if count1 == 3 or count2 == 3:
			return True

		return False

	def check_board_full(self):
		""" Check if there are no available spots on the board """
		for row in self.board:
			if row.count(self.AVAIL) > 0:
				return False
		return True

	def _switch_turn(self):
		""" Toggle the currently playing player """
		if self._playing == self.P1:
			self._playing = self.P2
		else:
			self._playing = self.P1

	def update_state(self):
		""" Update the state of the board by analyzing it """
		if self.check_won(self.P1):
			self._state = self.GameState.P1_WON
		elif self.check_won(self.P2):
			self._state = self.GameState.P2_WON

		elif self.check_board_full():
			# if no one won and there are no more free spots, it is a tie
			self._state = self.GameState.TIE

	def play(self, r, c):
		""" Update the board and the game state with a given move from the playing player """
		self.board[r, c] = self._playing

		self.update_state()
		self._switch_turn()
		return self._state

	def main_loop(self, *, algo=None, algo_plays=None):
		""" Runs a main loop which continuously plays until the game is won or tied
		Can optionally be given an algorithm to play as a given player """

		while self._state is TTT.GameState.IN_PROGRESS:
			print(self)
			if algo and self._playing == algo_plays:
				r, c = algo.find_next_move()
				print(f"{self._playing}'s turn -- Algo played {r}{c}")
			else:
				r, c = map(int, input(f"{self._playing}'s turn -- Enter coordinate: "))
			try:
				self._state = self.play(r, c)
			except ValueError as e:
				print(e)
		print(self)

		if self.state is TTT.GameState.P1_WON:
			print(f"{self.P1} won")
		elif self.state is TTT.GameState.P2_WON:
			print(f"{self.P2} won")
		elif self.state is TTT.GameState.TIE:
			print("Tie")

	def __str__(self):
		return str(self.board)


if __name__ == '__main__':
	def main():
		ttt = TTT()
		ttt.main_loop()


	main()
