import pytest

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


def test_count_solutions_returns_zero_for_an_invalid_board():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert sudoku_logic.count_solutions(board) == 0


def test_count_solutions_returns_one_for_a_solved_board():
    board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert sudoku_logic.count_solutions(board) == 1


def test_count_solutions_stops_at_two_for_a_multiple_solution_board():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert sudoku_logic.count_solutions(board, limit=2) == 2


def test_generated_puzzle_has_exactly_one_solution_and_requested_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )


def test_generate_puzzle_rejects_invalid_clue_counts():
    for clues in (16, 82):
        with pytest.raises(ValueError):
            sudoku_logic.generate_puzzle(clues)
