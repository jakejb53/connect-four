# Ideas

## Perception
Information a human player sees at a glance.

- **Line view:** every row and every diagonal of four or more cells shown as a sequence of cells, with empty squares marked as playable now or not yet playable. A human sees lines as lines; a language model reads sequences natively, so the same grouping becomes reading a string. Approved in direction; not yet implemented.
- **Line view in `play_out` results:** the same view after hypothetical moves, so imagining a move shows its lines as a human's visual imagination would.
- **Change since your last turn:** the two pieces placed since the player last moved (its own and the opponent's reply). A human sees what changed without comparing boards.
- **Newest piece marked on the grid:** the last piece played is shown distinctly in the grid itself, as a human watched it drop.
- **Groups of adjacent pieces:** each player's pieces that touch in a row, column, or diagonal, listed as groups. A human sees clusters as shapes. Borderline: grouping adjacency is perception, but naming what a group threatens is not, and only the former would be provided.

## Memory and learning
Information a human player remembers.

- **Private per-turn plan:** a short note the model writes for itself each move, carried to its next turn and hidden from the opponent. A human remembers what they were planning; the model currently starts every turn from nothing.
- **Plan review after each game:** the notes update sees the model's private plans from the game alongside what happened. A human can recall what they intended and compare it with the outcome.
- **Post-game analysis with `play_out`:** the notes update may use the analysis board to examine positions from the finished game, as a human replays a game on a board afterward.
- **Persistence across reloads:** records and notes saved in the browser, so a reload doesn't erase memory a human would retain across sessions.
- **Notes size:** revisit the 300-word limit for long series; a human's memory of a long rivalry is richer than a few paragraphs.
