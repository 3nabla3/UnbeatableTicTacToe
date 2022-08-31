import pytest
from TTT import TTT, InvalidCoordinateException, UnavailableCoordinateException


def test_invalid():
	with pytest.raises(InvalidCoordinateException):
		TTT().play(1, 3)
	with pytest.raises(InvalidCoordinateException):
		TTT().play(3, 0)
	with pytest.raises(InvalidCoordinateException):
		TTT().play(0, -1)


def test_unavailable():
	ttt = TTT()
	ttt.play(1, 1)
	assert ttt.playing == ttt.P2
	with pytest.raises(UnavailableCoordinateException):
		ttt.play(1, 1)
	assert ttt.playing == ttt.P2
	with pytest.raises(UnavailableCoordinateException):
		ttt.play(1, 1)
	assert ttt.playing == ttt.P2
