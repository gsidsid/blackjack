# Blackjack

### Running Instructions:
Begin the game by running the script `blackjack.py`.

### Rules:
Standard blackjack rules, with functionality for doubling down, splitting, and payout tracking over multiple rounds.

### Design:

#### Process:
I decided to use Python for its simplicity in implementation and prototyping speed. No formal test structure is used, albeit testing was conducted iteratively in-script as the codebase was built out. 

Before starting development of the blackjack ruleset/game code, I wrote out some requirements and raw output in `design.txt` to visualize some scenarios for how the game could look and operate. This helped clarify what features needed to be implemented and what cases needed to be covered, at least on a high level.

#### Code:
`playcards.py` was written to provide a rudimentary playing card deck interface that could be simply generalized to be used with any card game implemented. By passing functions to the Player class, rather than blackjack specific constants, player behavior can be updated in different ways for different games.

`blackjack.py` defines the rules and player decisions specific to blackjack and enables the game to be played using a simple interface. To keep controlling the player state simple, it reduces the game to three rounds: betting, decisions, and payout. Each round transitions to another via a system of flags, and some edge cases are handled where cards are split or 21 is reached early on in the decisions round. 

Because this was a project focusing on the development of the card game, the `qprompt` library is used in this project to handle input prompts without having to focus too much on the aesthetics of print statements and minutia of keypress detection.
