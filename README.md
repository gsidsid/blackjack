# Blackjack

### Running Instructions:
To begin the game, run the command `python blackjack.py`.

### Rules:
Standard blackjack rules, with functionality for doubling down, splitting, and payout tracking over multiple rounds.

### Design:
`playcards.py` was written to provide a rudimentary playing card deck interface that could be simply generalized to be used with any card game implemented. `blackjack.py` defines the rules and player decisions specific to blackjack and enables the game to be played using a simple interface. Input prompts were largely handled by `qprompt`, a library used in this project.
