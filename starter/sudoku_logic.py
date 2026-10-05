import copy
import random

SIZE = 9
EMPTY = 0
MIN_UNIQUE_CLUES = 17
MAX_GENERATION_ATTEMPTS = 100
DIFFICULTY_CLUES = {
    "Easy": 45,
    "Medium": 35,
    "Hard": 25,
}
_DEFAULT_CLUES = object()
_DEFAULT_DIFFICULTY = object()

def deep_copy(board):
    return copy.deepcopy(board)


def clues_for_difficulty(difficulty):
    try:
        return DIFFICULTY_CLUES[difficulty]
    except (KeyError, TypeError):
        valid_levels = ", ".join(DIFFICULTY_CLUES)
        raise ValueError(
            f"invalid difficulty {difficulty!r}; choose one of: {valid_levels}"
        ) from None


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def _candidates(board, row, col):
    return [
        number
        for number in range(1, SIZE + 1)
        if is_safe(board, row, col, number)
    ]

def count_solutions(board, limit=2):
    """Return the number of solutions, capped at ``limit``."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if len(board) != SIZE or any(len(row) != SIZE for row in board):
        raise ValueError("board must be a 9x9 grid")
    if any(
        cell < EMPTY or cell > SIZE
        for row in board
        for cell in row
    ):
        raise ValueError("board values must be between 0 and 9")

    working_board = deep_copy(board)
    for row in range(SIZE):
        for col in range(SIZE):
            value = working_board[row][col]
            if value != EMPTY:
                working_board[row][col] = EMPTY
                if not is_safe(working_board, row, col, value):
                    return 0
                working_board[row][col] = value

    def search():
        best_cell = None
        best_candidates = None

        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] == EMPTY:
                    candidates = _candidates(working_board, row, col)
                    if not candidates:
                        return 0
                    if best_candidates is None or len(candidates) < len(best_candidates):
                        best_cell = (row, col)
                        best_candidates = candidates
                        if len(candidates) == 1:
                            break
            if best_candidates is not None and len(best_candidates) == 1:
                break

        if best_cell is None:
            return 1

        row, col = best_cell
        solutions = 0
        for candidate in best_candidates:
            working_board[row][col] = candidate
            solutions += search()
            working_board[row][col] = EMPTY
            if solutions >= limit:
                return limit
        return solutions

    return search()

def remove_cells(board, clues):
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)
    removals_needed = SIZE * SIZE - clues
    removals = 0

    for row, col in positions:
        if removals == removals_needed:
            break
        value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board, limit=2) == 1:
            removals += 1
        else:
            board[row][col] = value

    if removals != removals_needed:
        raise RuntimeError("unable to create a unique puzzle with this clue count")

def generate_puzzle(clues=_DEFAULT_CLUES, *, difficulty=_DEFAULT_DIFFICULTY):
    if difficulty is not _DEFAULT_DIFFICULTY:
        if clues is not _DEFAULT_CLUES:
            raise ValueError("clues and difficulty cannot be used together")
        clues = clues_for_difficulty(difficulty)
    elif clues is _DEFAULT_CLUES:
        clues = DIFFICULTY_CLUES["Medium"]

    if isinstance(clues, bool) or not isinstance(clues, int):
        raise ValueError("clues must be an integer")
    if clues < MIN_UNIQUE_CLUES or clues > SIZE * SIZE:
        raise ValueError(
            f"clues must be between {MIN_UNIQUE_CLUES} and {SIZE * SIZE}"
        )

    for _ in range(MAX_GENERATION_ATTEMPTS):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        try:
            remove_cells(board, clues)
        except RuntimeError:
            continue
        puzzle = deep_copy(board)
        return puzzle, solution

    raise RuntimeError("unable to create a unique puzzle with this clue count")
