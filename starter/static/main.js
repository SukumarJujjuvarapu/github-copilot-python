// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_STORAGE_KEY = 'sudokuLeaderboard';
const MAX_LEADERBOARD_ENTRIES = 10;
const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
let puzzle = [];
let solution = [];
let hintsUsed = 0;
let timerInterval = null;
let timerStartedAt = 0;
let elapsedMilliseconds = 0;
let gameCompleted = false;

function formatElapsedTime(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText =
    `Time: ${formatElapsedTime(elapsedMilliseconds)}`;
}

function resetTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerStartedAt = 0;
  elapsedMilliseconds = 0;
  updateTimerDisplay();
}

function startTimer() {
  resetTimer();
  timerStartedAt = performance.now();
  timerInterval = setInterval(() => {
    elapsedMilliseconds = performance.now() - timerStartedAt;
    updateTimerDisplay();
  }, 250);
}

function stopTimer() {
  if (timerStartedAt) {
    elapsedMilliseconds = performance.now() - timerStartedAt;
    updateTimerDisplay();
  }
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerStartedAt = 0;
}

function loadLeaderboard() {
  try {
    const stored = localStorage.getItem(LEADERBOARD_STORAGE_KEY);
    if (!stored) return [];

    const entries = JSON.parse(stored);
    if (!Array.isArray(entries)) return [];

    return entries
      .filter(entry =>
        entry &&
        typeof entry.name === 'string' &&
        entry.name.trim() &&
        Number.isFinite(entry.timeMilliseconds) &&
        entry.timeMilliseconds >= 0 &&
        DIFFICULTIES.includes(entry.difficulty) &&
        Number.isInteger(entry.hintsUsed) &&
        entry.hintsUsed >= 0
      )
      .sort((a, b) => a.timeMilliseconds - b.timeMilliseconds)
      .slice(0, MAX_LEADERBOARD_ENTRIES);
  } catch (error) {
    return [];
  }
}

function saveLeaderboard(entries) {
  try {
    localStorage.setItem(LEADERBOARD_STORAGE_KEY, JSON.stringify(entries));
  } catch (error) {
    // Storage may be unavailable or full; gameplay should continue normally.
  }
}

function renderLeaderboard() {
  const container = document.getElementById('leaderboard-content');
  if (!container) return;

  const entries = loadLeaderboard();
  container.innerHTML = '';
  if (entries.length === 0) {
    const emptyMessage = document.createElement('p');
    emptyMessage.className = 'leaderboard-empty';
    emptyMessage.innerText = 'No completed games yet.';
    container.appendChild(emptyMessage);
    return;
  }

  const table = document.createElement('table');
  table.className = 'leaderboard-table';
  table.innerHTML = `
    <thead>
      <tr>
        <th scope="col">Rank</th>
        <th scope="col">Player</th>
        <th scope="col">Time</th>
        <th scope="col">Difficulty</th>
        <th scope="col">Hints</th>
      </tr>
    </thead>
  `;
  const body = document.createElement('tbody');
  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    [index + 1, entry.name, formatElapsedTime(entry.timeMilliseconds),
      entry.difficulty, entry.hintsUsed].forEach(value => {
      const cell = document.createElement('td');
      cell.innerText = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
  table.appendChild(body);
  container.appendChild(table);
}

function recordCompletion() {
  const name = window.prompt('Enter your name for the leaderboard:');
  if (!name || !name.trim()) return;

  const entries = loadLeaderboard();
  entries.push({
    name: name.trim(),
    timeMilliseconds: elapsedMilliseconds,
    difficulty: document.getElementById('difficulty').value,
    hintsUsed
  });
  entries.sort((a, b) => a.timeMilliseconds - b.timeMilliseconds);
  const topEntries = entries.slice(0, MAX_LEADERBOARD_ENTRIES);
  saveLeaderboard(topEntries);
  renderLeaderboard();
}

function completeGame() {
  if (gameCompleted) return;

  gameCompleted = true;
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  for (const input of inputs) {
    input.disabled = true;
  }
  stopTimer();
  const message = document.getElementById('message');
  message.style.color = '#388e3c';
  message.innerText = 'Congratulations! You solved it!';
  recordCompletion();
}

function getCurrentBoard() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function hasConflict(board, row, col) {
  const value = board[row][col];
  if (!value) return false;

  for (let i = 0; i < SIZE; i++) {
    if (i !== col && board[row][i] === value) return true;
    if (i !== row && board[i][col] === value) return true;
  }

  const boxRowStart = Math.floor(row / 3) * 3;
  const boxColStart = Math.floor(col / 3) * 3;
  for (let i = boxRowStart; i < boxRowStart + 3; i++) {
    for (let j = boxColStart; j < boxColStart + 3; j++) {
      if ((i !== row || j !== col) && board[i][j] === value) return true;
    }
  }
  return false;
}

function validateInput(input) {
  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const board = getCurrentBoard();
  input.classList.toggle('incorrect', hasConflict(board, row, col));
}

function checkForCompletion() {
  if (!solution.length) return;

  const board = getCurrentBoard();
  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      if (!board[row][col] || board[row][col] !== solution[row][col]) return;
    }
  }

  completeGame();
}

function isSafe(board, row, col, value) {
  for (let i = 0; i < SIZE; i++) {
    if (board[row][i] === value || board[i][col] === value) return false;
  }

  const boxRowStart = Math.floor(row / 3) * 3;
  const boxColStart = Math.floor(col / 3) * 3;
  for (let i = boxRowStart; i < boxRowStart + 3; i++) {
    for (let j = boxColStart; j < boxColStart + 3; j++) {
      if (board[i][j] === value) return false;
    }
  }
  return true;
}

function solveBoard(board) {
  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      if (board[row][col] !== 0) continue;
      for (let value = 1; value <= SIZE; value++) {
        if (!isSafe(board, row, col, value)) continue;
        board[row][col] = value;
        if (solveBoard(board)) return true;
        board[row][col] = 0;
      }
      return false;
    }
  }
  return true;
}

function updateHintCount() {
  document.getElementById('hint-count').innerText = `Hints used: ${hintsUsed}`;
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        validateInput(e.target);
        checkForCompletion();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  resetTimer();
  solution = [];
  hintsUsed = 0;
  gameCompleted = false;
  updateHintCount();
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  solution = data.puzzle.map(row => row.slice());
  solveBoard(solution);
  startTimer();
  document.getElementById('message').innerText = '';
}

function useHint() {
  if (!solution.length) return;

  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (input.disabled || input.value) continue;

    const row = parseInt(input.dataset.row, 10);
    const col = parseInt(input.dataset.col, 10);
    input.value = solution[row][col];
    input.disabled = true;
    input.className = 'sudoku-cell hinted';
    hintsUsed++;
    updateHintCount();
    checkForCompletion();
    return;
  }
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    completeGame();
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('difficulty').addEventListener('change', newGame);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', useHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  renderLeaderboard();
  // initialize
  newGame();
});