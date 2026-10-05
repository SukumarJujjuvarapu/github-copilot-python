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
