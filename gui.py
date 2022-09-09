import pygame
from pygame.color import THECOLORS
from pygame.locals import *

from TTT import TTT
from minmax import TTTMinMax

pygame.init()
W, H = 800, 600


def render_grid(screen):
	# vertical lines
	for i in range(2):
		x_coord = W // 3 * (i + 1)
		pygame.draw.line(screen, THECOLORS['green'], (x_coord, 0), (x_coord, H), 10)
	# horizontal lines
	for i in range(2):
		y_coord = H // 3 * (i + 1)
		pygame.draw.line(screen, THECOLORS['green'], (0, y_coord), (W, y_coord), 10)


def mouse_pos_to_grid_coord(mouse_pos):
	x, y = mouse_pos

	for i in range(2):
		if x < W // 3 * (i + 1):
			coord_x = i
			break
	else:
		coord_x = 2

	for i in range(2):
		if y < H // 3 * (i + 1):
			coord_y = i
			break
	else:
		coord_y = 2

	return coord_y, coord_x


def render_board(screen, board):
	for row_i, row in enumerate(board):
		for col_i, elem in enumerate(row):
			if elem is TTT.P1:
				draw_x(screen, row_i, col_i)
			if elem is TTT.P2:
				draw_o(screen, row_i, col_i)


def pos_of_center_of_coord(row_i, col_i):
	width_of_col = W / 3
	width_of_row = H / 3
	x = round(width_of_col * col_i + width_of_col / 2)
	y = round(width_of_row * row_i + width_of_row / 2)
	return x, y


def draw_x(screen, row_i, col_i):
	x, y = pos_of_center_of_coord(row_i, col_i)
	size = 30
	pygame.draw.line(screen, THECOLORS['red'], (x - size, y - size), (x + size, y + size), 10)
	pygame.draw.line(screen, THECOLORS['red'], (x + size, y - size), (x - size, y + size), 10)


def draw_o(screen, row_i, col_i):
	x, y = pos_of_center_of_coord(row_i, col_i)
	size = 30
	pygame.draw.circle(screen, THECOLORS['red'], (x, y), size, width=5)


def send_to_game(ttt, r, c):
	state = TTT.BoardState.IN_PROGRESS
	try:
		state = ttt.play(r, c)
	except ValueError as e:
		print(e)

	if state is TTT.BoardState.P1_WON:
		print(f"{TTT.P1} won")
	elif state is TTT.BoardState.P2_WON:
		print(f"{TTT.P2} won")
	elif state is TTT.BoardState.TIE:
		print("Tie")

	return state is not TTT.BoardState.IN_PROGRESS


def main():
	screen = pygame.display.set_mode((W, H))
	ttt = TTT()
	mm = TTTMinMax(ttt, plays=TTT.P2)

	game_over = False
	running = True
	while running:
		screen.fill(THECOLORS['black'])

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == K_r:
					ttt = TTT()
					mm.ttt = ttt
					if mm.player == TTT.P1:
						mm.generate_tree()
					else:
						mm.tree = None
					game_over = False

			elif event.type == MOUSEBUTTONDOWN:
				if not game_over and ttt.playing is not mm.player:
					r, c = mouse_pos_to_grid_coord(event.pos)
					game_over = send_to_game(ttt, r, c)

		render_grid(screen)
		render_board(screen, ttt.board)

		pygame.display.update()
		if not game_over and ttt.playing is mm.player:
			r, c = mm.find_next_move()
			game_over = send_to_game(ttt, r, c)


if __name__ == '__main__':
	main()
