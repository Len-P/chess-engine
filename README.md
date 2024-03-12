---
Author: Faber Pas, Len Pasic, Ayoub Elgharrafi
Date: December 2022
Title: "Chess AI"
---

# Introduction

Chess is a vast game with an awful lot of possibilities. A
chess AI will therefore not only have to go through many possible moves,
but also have to be able to quickly calculate for each move how good that move is.
To do this, one uses a utility function. This is a
function that calculates for each move what the value of that move is based
based on some features. It is mainly those features and their
implementation that will determine the strength of the AI.

# Features

The code behind the features discussed in this section is
found in chessutility.py.

## Material value

A first and very important feature introduced is the value
of the pieces on the board. It is important not to lose any
pieces, which is intuitively obvious. Different pieces
have different values, listed below:

- Pawn: value 1

- Knight, bishop: value 3

- Rook: value 5

- Queen: value 9

This is implemented in a fairly simple way: the *materialscore*
function looks at which pieces are left on the board by color, and subtracts the
value of the black pieces from that of the white pieces. The
returned value is thus the utility for white. The relative values of the
pieces were multiplied by 100, e.g. 300 for a knight.

## Position value

The position of the pieces on the board is also important, of course. A
king should not be in the middle of the field, but somewhere protected
in a corner. A pawn is not worth much, but can turn into a
lady when it crosses the field. In general, the values
one can earn for good positioning are an order of magnitude
smaller than the values of the pieces themselves.

To implement this, we use piece-square table (PST):

An example of a PST for the horse is shown in the figure.

![An example of a piece-square table for the knight. On the left are the
values given to the computer, on the right a graphical illustration](https://github.com/Len-P/chess-engine/blob/master/PST.png?raw=true)

## Castle score

Castling is a special move in chess, and should carry great value
as it moves the king to safety and puts the rook in a
good position. Indirectly, this is in the PSTs since the
king and rook get good scores on the positions where they end up
after castling, but this more often causes the engine to move the king manually to the corner, rather than castling. That's why a separate
feature that rewards castling was implemented.

The implementation works as follows:
- Check if castling with 1 of the rooks is possible in the current position. This is a conditional statement that first of all requires castling rights (castling is not always allowed) and second, the position of the rooks is taken into account.
  
- Return a reward of 90 if the conditions are met. This
  value is chosen because there should be a strong emphasis on the
  importance of castling, while it is not desirable for a pawn to be
  equal to the action of castling.

- Give no reward, but also no punishment (reward 0) if the
  conditions are not met. At first glance, one would think
  that a penalty would apply here, but this would result
  in a penalty as soon as castling is completed. Because castling cannot
  be possible after it is executed, the engine would now receive a penalty on every subsequent move.
  Rather, it is desired that castling be
  pursued and once it is executed that one continue as
  usual and skip the full Castle Score method.

## Check score

By putting the opponent in check you force them to respond. You also put pressure on the structure around the king. A chess player should
thus try to look for opportunities to put the opponent in check. A feature was therefore built in that prompts the engine to check the
opponent.

The implementation works as follows:

- Check whether the king of the player whose turn it is, is already in check.

- Give a penalty of -90 if the king is in check.

- Do nothing if the king is not in check.

- Based on this, the agent will search for the position where the
  opponent is in check. The position in which he himself is in check
  will be avoided. Similar to Castle Score,
  a value of 90 is chosen with the same reasoning.

## Chance of material losses

A situation that occurs regularly is that a piece is both attacked and
covered, and here of course it is important that the number of
covering pieces is greater than the number of attackers. The *materialscore*
function just discussed will to some extent take care of this,
but in order to keep the program fast enough we usually look
only 3-4 moves into the future, so certain scenarios will not
be fully computed. Therefore, a feature was implemented
that specifically calculates whether a piece is still covered enough.

The implementation is pretty straight-forward, with a few subtleties.

- Fewer coverers than attackers: in this case, the defender would, in
  case he does play the move, lose all the coverers and the piece that is
  being played. We assume that the attacker will first attack
  with all his worst pieces. So he will lose his
  worst pieces, and as many as there are coverers. Furthermore,
  an exception must be made if there is a king among the pieces.
  He will no longer be able to participate because you are not allowed to
  check yourself, of course. The required values are calculated
  and the net loss is given. The loss can still
  be negative (i.e. the defender can make a profit) if the covering pieces are
  are for example two pawns and a knight, while the attackers are 4
  queens.

- As many coverers as attackers: first we check whether there is
  a king among the attackers, because all attackers will die in the
  potential duel. Among the deckers there may be a king,
  it will take last. The net loss is calculated by
  assuming that the attacker loses all attackers, and the
  defender loses all the decks except the most valuable one
  (with which he takes last) and the piece he set.

- More coverers than attackers: here the same reasoning is
  applied as in the first situation, with then the roles of the attacker
  and defender reversed.

## Board value

The *Boardvalue* function calculates all the features just discussed
for a given move, and provides the total value. It will be called
by the chess agent (see section 3).

## Transposition table class

Since the value calculation of a board is not trivial, as can be seen
from all the features just discussed, it is useful to have a
transposition table. This table records every board (and its value) that is
encountered while exploring. When that same
board comes back again later, due to a different move combination, one can
simply extract the value of this board from the table. The implementation is
very basic and will not be discussed further here. In order to
identify boards, one uses the python-chess *board.epd()* function that converts a
board to a string.

# The implementation

The code behind the things discussed in this section is
found in chessagent.py.

During play, the chess agent will look ahead a few moves at a time
and calculate the board value for all legal moves at that
moment. Eventually it will play the move with the largest value. This
value is determined using the minimax algorithm with
alpha-beta pruning.

## Grandmaster moves

Chess engines are often given a list of grandmaster moves.
These are moves that, according to various grandmasters, are always the best in
particular situations. These moves are usually at the
beginning of the game. Here, these moves were limited to the very first
move of the game; there will always be opened with e4 or e5, depending
on the position in which is started.

## Alpha-beta pruning

The abpruning method is the implementation of the minimax algorithm with
alpha-beta pruning. It takes a chessboard, two floats representing the alpha
and beta values, an integer representing the search depth,
a boolean representing whether the search is maximizing or minimizing, and a transposition table. The alpha-beta pruning algorithm is
used to improve the efficiency of the minimax search by
cutting off branches of the search tree that cannot
influence the final decision.

The implementation is done as follows:

- The method first checks whether the value of the sign is already
  stored in the transposition table. If so, the
  stored value is given to avoid recalculation.

- If the search depth is equal to 0 or the elapsed time since
  the start of the search has exceeded the time limit,
  the method returns the board value using the
  boardvalue method (from chessutility.py).

- If the search is a maximizing search, the legal moves are
  traversed and the value of each move is calculated by calling the abpruning
  method recursively until the already mentioned final conditions
  are reached. It stores the maximal value and updates the value
  of alpha. If the beta value is less than or equal to the
  alpha value, the search is aborted.

- If the query is a minimizing query, the same is done,
  but with the minimum value and the beta value.

# Unimplemented ideas

Coming up with good features was not an easy task. It would have
have been nice to build a neural network that takes recorded
chess games as input and derives certain features from that. There are
in fact, undoubtedly good features that by sheer reasoning are
impossible to come up with. A computer that sees patterns
where a human sometimes does not could thus prove useful.

Also, the grandmaster moves could have been more extensive, but there was no
time to implement this further. This could have been done by for example
listing certain boards and linking them directly to a move.

Finally, it would have been possible to improve the search algorithm
by searching deeper into branches with a higher potential
risk (quiescent search).
