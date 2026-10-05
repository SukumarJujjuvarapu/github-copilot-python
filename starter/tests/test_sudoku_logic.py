import sudoku_logic


def test_create_empty_board_returns_a_zero_filled_9_by_9_board():
    board = sudoku_logic.create_empty_board()

    assert board == [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]


def test_fill_board_creates_a_complete_valid_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert all(sorted(row) == list(range(1, 10)) for row in board)
    assert all(
        sorted(board[row][column] for row in range(sudoku_logic.SIZE))
        == list(range(1, 10))
        for column in range(sudoku_logic.SIZE)
    )


def test_generate_puzzle_preserves_solution_and_requested_clue_count():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )
    assert all(sorted(row) == list(range(1, 10)) for row in solution)
