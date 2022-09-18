from TTT import TTT


def test_won_default():
	assert TTT().check_won('x') is False
	assert TTT().check_won('o') is False

	state = ['-x-', '-ox', 'xoo']
	ttt = TTT(init_board=state)
	assert ttt.check_won('o') is False
	assert ttt.check_won('x') is False


def test_won_row():
	state = ['xx-', 'xoo', 'xxx']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is True
	assert ttt.check_won('o') is False

	state = ['oxx', 'ooo', '---']
	ttt = TTT(init_board=state)
	assert ttt.check_won('o') is True
	assert ttt.check_won('x') is False

	state = ['oxx', 'ooo', 'xxx']
	ttt = TTT(init_board=state)
	assert ttt.check_won('o') is True
	assert ttt.check_won('x') is True


def test_won_column():
	state = ['xxo', '-xo', 'ox-']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is True
	assert ttt.check_won('o') is False

	state = ['xoo', 'o-o', 'x-o']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is False
	assert ttt.check_won('o') is True

	state = ['xoo', 'x-o', 'xxo']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is True
	assert ttt.check_won('o') is True


def test_won_diag():
	state = ['xo-', 'oxx', '--x']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is True
	assert ttt.check_won('o') is False

	state = ['-ox', 'oxx', 'x--']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is True
	assert ttt.check_won('o') is False

	state = ['o--', 'xox', 'x-o']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is False
	assert ttt.check_won('o') is True

	state = ['--o', 'xox', 'o-x']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is False
	assert ttt.check_won('o') is True

	state = ['xxo', '-o-', 'ox-']
	ttt = TTT(init_board=state)
	assert ttt.check_won('x') is False
	assert ttt.check_won('o') is True
