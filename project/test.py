import chess
import random
from chess_utilities.chess_utility import ChessUtility
from math import ceil

# Create a board
board = chess.Board()
print(list(board.generate_legal_moves()))
board.push(chess.Move.from_uci('e2e4'))
board.push(chess.Move.from_uci('e7e5'))
board.push(chess.Move.from_uci('b2b4'))



def danger_score(self, board: chess.Board):
    last_move = board.peek()
    square = chess.Square(last_move.to_square)
    last_moved_piece = board.piece_at(square)
    color = last_moved_piece.color

    attackers = list(board.attackers(not color, square))
    defenders = list(board.attackers(color, square))

    attacker_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in attackers)
    defender_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in defenders)

    if attackers:
        if len(attackers) > len(defenders):
            if chess.KING in defenders:
                defenders.remove(chess.KING)
            effective_attacker_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in sorted(attackers)[0:len(
                defenders)])  # dit zijn de attackers die de attacker gaat gebruiken
            loss = defender_worth + self.get_piece_worth(
                last_moved_piece) - effective_attacker_worth  # defender verliest alle defenders en het stuk dat hij naar voor zet
            return loss
        elif len(attackers) == len(defenders):
            effective_defender_worth = sum(
                self.get_piece_worth(board.piece_at(s)) for s in sorted(defenders)[0:len(defenders) - 1])
            loss = -attacker_worth + self.get_piece_worth(last_moved_piece) + effective_defender_worth
            return loss
        elif len(attackers) < len(defenders):
            if chess.KING in attackers:
                attackers.remove(chess.KING)
            effective_defender_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in sorted(defenders)[0:len(
                attackers)])  # dit zijn de defenders die de defender gaat gebruiken
            loss = effective_defender_worth + self.get_piece_worth(
                last_moved_piece) - attacker_worth  # attacker verliest alle attackers
            return loss
        else:
            return 0
    return 0

print(danger_score(ChessUtility(), board))
