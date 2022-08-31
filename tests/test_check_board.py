import pytest
from TTT import TTT, InvalidInitialBoardException


def test_no_avail():
	state = ['xx-', 'oo-', 'xxx']
	assert TTT(init_board=state).check_board_full() is False
	state = ['xxx', '---', '---']
	assert TTT(init_board=state).check_board_full() is False
	state = ['ooo', 'xxx', 'xxx']
	assert TTT(init_board=state).check_board_full() is True


def test_board_valid():
	state = ['xxxx', 'ooo', 'xxx']
	with pytest.raises(InvalidInitialBoardException):
		TTT(init_board=state)
	state = ['ooo', 'xxx', '***']
	with pytest.raises(InvalidInitialBoardException):
		TTT(init_board=state)
	state = ['ooo', 'xxx', '---']
	TTT(init_board=state)

