# Ideas

## Perception
Information a human player sees at a glance.

- **Change since your last turn:** the two pieces placed since the player last moved (its own and the opponent's reply). A human sees what changed without comparing boards.
- **Newest piece marked on the grid:** the last piece played is shown distinctly in the grid itself, as a human watched it drop.
- **Groups of adjacent pieces:** each player's pieces that touch in a row, column, or diagonal, listed as groups. A human sees clusters as shapes. Borderline: grouping adjacency is perception, but naming what a group threatens is not, and only the former would be provided.

## Memory and learning
Information a human player remembers.

- **Plan review after each game:** the notes update sees the model's private plans from the game alongside what happened. A human can recall what they intended and compare it with the outcome.
- **Post-game analysis with `play_out`:** the notes update may use the analysis board to examine positions from the finished game, as a human replays a game on a board afterward.
- **Persistence across reloads:** records and notes saved in the browser, so a reload doesn't erase memory a human would retain across sessions.
- **Notes size:** revisit the 300-word limit for long series; a human's memory of a long rivalry is richer than a few paragraphs.
