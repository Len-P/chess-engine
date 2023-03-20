from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.chess_utility import ChessUtility, TranspositionTable
import time
import chess.polyglot
import random

"""An example search agent with two implemented methods to determine the next move"""


class ChessAgent(Agent):

    # Initialize your agent with whatever parameters you want
    def __init__(self, utility: ChessUtility(), time_limit_move: float, depth: int) -> None:
        super().__init__(utility, time_limit_move, depth)
        self.name = "Chess search agent"
        self.author = "LFA"

        self.start_time = None
        self.depth = depth
        self.grandmaster_moves = [chess.Move.from_uci('e2e4'), chess.Move.from_uci('e7e5')]

    def legal_moves(self, board: chess.Board):
        # Generate a list of all legal moves
        return list(board.legal_moves)

    def ab_pruning(self, board: chess.Board, alpha, beta, dpth, maximum: bool, transposition_table = TranspositionTable()):
        value = transposition_table.lookup(board)
        if value is not None:
            return value

        if dpth == 0 or time.time() - self.start_time > 0.97 * self.time_limit_move:
            value = self.utility.board_value(board)
            transposition_table.store(board, value)
            return value

        if maximum:
            best_value = -float("inf")
            for move in self.legal_moves(board):
                board.push(move)
                best_value = max(best_value, self.ab_pruning(board, alpha, beta, dpth - 1, False))
                board.pop()
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value

        else:
            best_value = float("inf")
            for move in self.legal_moves(board):
                board.push(move)
                best_value = min(best_value, self.ab_pruning(board, alpha, beta, dpth - 1, True))
                board.pop()
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def calculate_move(self, board: chess.Board):
        self.start_time = time.time()
        moves = self.legal_moves(board)

        if self.grandmaster_moves[0] in moves and board.turn:
            return self.grandmaster_moves[0]
        elif self.grandmaster_moves[1] in moves and not board.turn:
            return self.grandmaster_moves[1]
        else:

            best_value = float("-inf")
            best_move = None

            for move in moves:
                board.push(move)
                value = self.ab_pruning(board, float("-inf"), float("inf"), self.depth - 1, False)
                print(value)
                board.pop()
                if value >= best_value:
                    best_value = value
                    best_move = move
                    print(best_value, move)
            return best_move
