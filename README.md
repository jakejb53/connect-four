# Connect Four · AI vs AI

A browser app in which two LLMs play Connect Four against each other in a continuous series. Each player is any OpenAI-compatible chat-completions endpoint. The page shows the board, a scoreboard, and each model's streamed reasoning and moves.

<img width="3819" height="1427" alt="c4" src="https://github.com/user-attachments/assets/f0b8841c-3b1b-4579-a07d-9148980c144a" />

## What we're evaluating

General problem-solving capability of language models (not world knowledge), observed through gameplay:

- **Tactics:** finding and executing concrete short-term sequences — wins, blocks, forcing moves.
- **Strategy:** forming and pursuing longer-term plans and judging positions without forcing lines.
- **Psychology:** taunting, distracting, and misdirecting the opponent through table talk, and seeing through the opponent's attempts.
- **Learning and self-improvement:**
  - **About the game:** discovering principles not given to them.
  - **About their opponent:** recognizing and exploiting a specific opponent's tendencies.
  - **Between turns:** carrying analysis and plans forward within a game.
  - **Between games:** applying lessons from earlier games in a series.

How a model approaches a problem matters as much as the result.

## How we're doing it

### Human games
We use games designed for human players (currently Connect Four), so behavior can be judged against human understanding of the game.

### AI vs AI
Models play each other head-to-head; relative strength between specific models is a primary result. Both players always receive identical instructions, information, and limits, and the first move alternates between games.

### Compensate for deficiencies, not for the disadvantages they create
A language model lacks faculties a human player has, such as visual perception of the board and memory across sessions. We compensate for the missing faculty by providing the information it would supply, in a form a language model can use. We never compensate for the resulting disadvantage by supplying conclusions the faculty would only help a player reach.

**Test:** would a human player have this information just by looking at the board or remembering what happened? If yes, providing it is allowed. If producing it requires thinking about the position, it is not, regardless of form.

#### What we provide
- **Move list, last move, column stacks with landing rows, piece coordinates, grid:** what a human sees on the board, restated so no counting across grid lines is needed.
- **Line view:** every row and every diagonal of four or more cells as a sequence of cells, with each empty square marked as playable now or with how many pieces its column needs first. A human sees lines as lines, and sees the empty squares beneath a square; a language model reads sequences natively. It names no threats, and who will fill a column is left to the model.
- **Valid moves with their results:** for each legal move, the lines through its landing square with the piece already placed, and the square that becomes playable above it. A human pictures the piece in the square and sees the lines through it at once; the model would otherwise rebuild them for every move it considers. It names no threats and never says whether a move wins.
- **`play_out` analysis board:** stands in for visual imagination; it shows the position after hypothetical moves and adjudicates wins and draws by the rules, without evaluating. Calls per move are capped so search stays the model's own choice of lines.
- **Game records and notes:** stand in for memory of earlier games. Records are exact; notes are written by the model itself.
- **`save_plan` private plan:** stands in for remembering what you were planning between your own moves. The model writes it; only it sees it, on its next move in the same game.
- **How table talk is played:** players are told that table talk may taunt, distract, or misdirect, need not be truthful, and that psychological advantage often decides games. Like the rules, this describes the game, not the position.

#### What we don't provide
- **Threats, immediate wins, required blocks, or unsafe moves:** conclusions about the position, not perception.
- **Evaluations, suggested moves, or strategic advice** (e.g. "prefer the center"): conclusions, and they would remove the strategy being measured.
- **Prescribed reasoning procedures:** they shape how the model thinks rather than what it can perceive.
- **General code execution:** it would let a model write a solver, turning gameplay into a coding test.

### Observation
Each move's reasoning, tool use, plans, messages, and commentary are shown. Messages sent with `tell_opponent` become table talk both players see; `commentary` is for spectators only and reaches neither player. Results, notes, and failure counts (cut-off and fallback moves) are recorded.

## Non-goals
- World knowledge or memorized game theory.
- Coding ability.
- Strict output-format compliance; replies are parsed leniently where the intended move is unambiguous.

## Requirements

- Python 3 (standard library only)
- A modern browser
- Two OpenAI-compatible endpoints (they can be the same server)

## Running

1. From the repo directory, start the server:

       python3 serve.py

2. Open http://localhost:8000/connect-four.html (or the same path on `127.0.0.1:8000`). The page must be loaded from this server; opening the file directly will not work.
3. For each player, set **Endpoint** (a base URL such as `http://10.0.0.5:1234/v1`, or the full `/chat/completions` URL) and **Model**. API key, reasoning effort, max tokens, and streaming are optional.
4. Optionally set **Tool calls** (next to Countdown): the number of `play_out` calls each player may make per move. 0 turns `play_out` off; `save_plan`, `tell_opponent`, and `commentary` are always available.
5. Press **Start series**.

Settings (including API keys) and the series state — game records, notes, scores, plans, and the game in progress — are saved in the browser's localStorage. On reload the saved state is restored, and **Start series** resumes it: an interrupted move restarts from its beginning. **Clear state** discards the series state (and clears the logs) but keeps settings. Storage is per origin, so `localhost:8000` and `127.0.0.1:8000` keep separate saves. If a save fails validation it is not loaded and is left untouched for repair from devtools; Start stays disabled until it loads or is cleared.

`serve.py` serves the page and relays its API calls to the endpoints, so the endpoints don't need to allow browser (CORS) requests. It listens only on `127.0.0.1:8000`.

## Inspecting model calls

In the browser's devtools console, `calls()` returns every model call of the current game — the exact request body sent (model, parameters, all messages, all tools) and the parsed response — in a readable JSON-like layout with multi-line strings shown as written. `calls(i)` returns a single call. The record resets when each game starts; the notes updates after a game remain until the next one begins.
