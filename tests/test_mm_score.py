from TTT import TTT
from minmax import TTTMinMax, MinMaxTree


def test_minimize():
	state = ['xxo', '-o-', '-x-']
	ttt = TTT(init_board=state)
	mm = TTTMinMax(ttt)
	mm.generate_tree(optimise=False)
	tree: MinMaxTree = mm.tree
	score = tree.get_score()
	assert score == -1
