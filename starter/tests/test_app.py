import pytest

import sudoku_logic
from app import CURRENT


def test_index_renders_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku Game" in response.data
    assert b'id="new-game"' in response.data
    assert b'id="check-solution"' in response.data


def test_new_game_returns_and_stores_a_puzzle(client):
    response = client.get("/new?clues=81")

    assert response.status_code == 200
    puzzle = response.get_json()["puzzle"]
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(1 <= cell <= 9 for row in puzzle for cell in row)

    check_response = client.post("/check", json={"board": puzzle})
    assert check_response.status_code == 200
    assert check_response.get_json() == {"incorrect": []}


@pytest.mark.parametrize(
    ("difficulty", "expected_clues"),
    [("Easy", 45), ("Medium", 35), ("Hard", 25)],
)
def test_new_game_supports_difficulty_levels(client, difficulty, expected_clues):
    response = client.get(f"/new?difficulty={difficulty}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["difficulty"] == difficulty
    puzzle = data["puzzle"]
    assert sum(cell != 0 for row in puzzle for cell in row) == expected_clues
    assert sudoku_logic.count_solutions(puzzle) == 1
    solution = CURRENT["solution"]
    assert all(
        puzzle[row][column] in (0, solution[row][column])
        for row in range(9)
        for column in range(9)
    )


def test_new_game_without_parameters_defaults_to_medium_clue_count(client):
    response = client.get("/new")

    assert response.status_code == 200
    data = response.get_json()
    assert "difficulty" not in data
    assert sum(cell != 0 for row in data["puzzle"] for cell in row) == 35


def test_new_game_rejects_invalid_difficulty(client):
    response = client.get("/new?difficulty=Extreme")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "invalid difficulty 'Extreme'; choose one of: Easy, Medium, Hard"
    }


def test_new_game_rejects_clues_and_difficulty_together(client):
    response = client.get("/new?clues=35&difficulty=Medium")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "clues and difficulty cannot be used together"
    }


def test_check_requires_a_game_in_progress(client):
    response = client.post("/check", json={"board": [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}


def test_check_reports_cells_that_do_not_match_the_solution(client):
    new_game_response = client.get("/new?clues=81")
    puzzle = new_game_response.get_json()["puzzle"]
    puzzle[0][0] = 1 if puzzle[0][0] != 1 else 2

    response = client.post("/check", json={"board": puzzle})

    assert response.status_code == 200
    assert response.get_json()["incorrect"] == [[0, 0]]
