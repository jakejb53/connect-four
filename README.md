# Connect Four · AI vs AI

A browser app in which two LLMs play Connect Four against each other in a continuous series. Each player is any OpenAI-compatible chat-completions endpoint. The page shows the board, a scoreboard, and each model's streamed reasoning and moves.

## Requirements

- Python 3 (standard library only)
- A modern browser
- Two OpenAI-compatible endpoints (they can be the same server)

## Running

1. From the repo directory, start the server:

       python3 serve.py

2. Open http://localhost:8000/connect-four.html (or the same path on `127.0.0.1:8000`). The page must be loaded from this server; opening the file directly will not work.
3. For each player, set **Endpoint** (a base URL such as `http://10.0.0.5:1234/v1`, or the full `/chat/completions` URL) and **Model**. API key, reasoning effort, max tokens, and streaming are optional.
4. Press **Start series**.

`serve.py` serves the page and relays its API calls to the endpoints, so the endpoints don't need to allow browser (CORS) requests. It listens only on `127.0.0.1:8000`.
