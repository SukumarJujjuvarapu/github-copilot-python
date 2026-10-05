# Sudoku Flask Project — Copilot Instructions

## Project Goal

Refactor the legacy Python Flask Sudoku application into a modern, maintainable, responsive Sudoku game while preserving existing functionality.

The final application must support:

* Easy, Medium, and Hard difficulty levels
* Sudoku puzzles with exactly one valid solution
* Locked prefilled cells
* Immediate invalid-entry feedback
* Check Puzzle functionality
* Hint functionality
* Timer
* Top 10 leaderboard using browser localStorage
* Difficulty and hint information in leaderboard entries
* Dark/light mode
* Responsive desktop and mobile layouts
* Accessible, readable UI
* Completion and congratulation feedback

## Technology

Use:

* Python 3
* Flask
* HTML5
* CSS3
* Vanilla JavaScript
* pytest for automated tests
* Browser localStorage for leaderboard persistence

Do not introduce unnecessary frameworks or dependencies.

## Code Quality

Prefer:

* Small, focused functions
* Single-responsibility modules
* Clear variable and function names
* Type hints where useful
* Helpful comments only where they explain non-obvious logic
* Consistent formatting
* Graceful error handling
* Reusable functions
* Separation of game logic, Flask routes, templates, CSS, and JavaScript

Avoid:

* Large monolithic functions
* Duplicate logic
* Global mutable state unless necessary
* Hard-coded values scattered throughout the code
* Unexplained magic numbers
* Unnecessary dependencies

## Sudoku Rules

Every generated puzzle must:

1. Be valid.
2. Be solvable.
3. Have exactly one solution.
4. Follow standard 9x9 Sudoku rules.
5. Lock all original/prefilled cells.
6. Respect the selected difficulty.

Never assume a generated board has a unique solution without explicitly validating it.

## Difficulty

Use three difficulty levels:

* Easy
* Medium
* Hard

Difficulty should primarily control how many cells are initially revealed.

Keep the difficulty configuration centralized rather than scattering values throughout the application.

## Validation

The application should distinguish between:

* A valid move
* An invalid/conflicting move
* An incomplete puzzle
* A completely solved puzzle

Invalid entries should receive immediate visual feedback.

The Check Puzzle feature should identify incorrect user entries without modifying correct entries.

## Hint

The Hint button must:

* Select an empty cell
* Insert the correct solution value
* Lock that cell
* Visually distinguish the hinted cell
* Increment the hint counter

Do not overwrite existing user-entered or original cells.

## Timer

The timer should:

* Begin when a puzzle starts
* Continue while the user is solving
* Stop when the puzzle is correctly completed
* Display elapsed time clearly
* Store the completion time in the leaderboard

## Leaderboard

Store the Top 10 fastest completed games in browser localStorage.

Each leaderboard entry should contain:

* Player name
* Time
* Difficulty
* Hints used

Sort entries by fastest completion time.

Keep only the best 10 entries.

Handle missing, malformed, or empty localStorage data gracefully.

## Dark Mode

Provide a clear light/dark mode toggle.

All important UI elements must remain readable in both themes.

Do not rely on color alone to communicate game state.

## Responsive Design

The interface must work on:

* Desktop
* Tablet
* Mobile

The Sudoku grid must remain usable without horizontal overflow.

Controls should remain readable and easy to click/tap on smaller screens.

## Sudoku Grid Styling

The 3x3 Sudoku boxes should have alternating visual styling while maintaining:

* Clear borders
* Good contrast
* No layout shifts
* Readability in dark and light modes

## Accessibility

Prefer WCAG 2.1 AA-friendly choices:

* Semantic HTML
* Labels for controls
* Keyboard-friendly interactions
* Visible focus states
* Sufficient contrast
* Buttons with descriptive names
* Avoid communicating important states through color alone

## Testing

Before modifying application behavior:

1. Create a pytest testing framework.
2. Write baseline tests for the existing application.
3. Run all baseline tests.
4. Confirm that they pass.
5. Do not change production behavior merely to make baseline tests pass.

After every significant feature/refactor:

* Run the full test suite.
* Fix regressions before continuing.
* Add tests for important new logic whenever practical.

## Copilot Workflow

When making changes:

1. Inspect the existing implementation first.
2. Explain the proposed approach before large changes.
3. Prefer small, reviewable changes.
4. Do not modify unrelated files.
5. Preserve working functionality unless the task explicitly changes it.
6. Ask for clarification about unfamiliar code when necessary.
7. Review generated code before accepting it.
8. Reject suggestions that violate these instructions.
9. Explain important implementation decisions in simple terms.

## Architecture Preference

Prefer this general separation:

* Flask routes/API: `app.py`
* Sudoku generation: `sudoku/generator.py`
* Sudoku solving: `sudoku/solver.py`
* Validation: `sudoku/validator.py`
* Game/state logic: `sudoku/game.py`
* Browser behavior: `static/js/game.js`
* Styling: `static/css/style.css`
* HTML: `templates/index.html`
* Automated tests: `tests/`

Do not force this structure if the existing repository requires a simpler compatible design, but keep responsibilities separated.

## Error Handling

User-facing errors should be understandable and non-technical.

Never expose stack traces to normal users.

Development/debugging errors may be logged for developers.

## Important

Do not blindly accept AI-generated code.

Review Copilot suggestions for:

* Correctness
* Security
* Maintainability
* Performance
* Compatibility with existing code
* Compliance with this instruction file
* Compliance with the Udacity project rubric

When a Copilot suggestion is rejected, document why in a code comment, README note, or project development notes when appropriate.
