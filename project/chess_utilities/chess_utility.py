import chess
from project.chess_utilities.utility import Utility

class ChessUtility(Utility):

    def __init__(self):
        pass

    def material_score(self, board: chess.Board):
        white_pieces = 0
        white_pieces += 100 * len(board.pieces(piece_type=chess.PAWN, color=chess.WHITE))
        white_pieces += 300 * len(board.pieces(piece_type=chess.BISHOP, color=chess.WHITE))
        white_pieces += 300 * len(board.pieces(piece_type=chess.KNIGHT, color=chess.WHITE))
        white_pieces += 500 * len(board.pieces(piece_type=chess.ROOK, color=chess.WHITE))
        white_pieces += 900 * len(board.pieces(piece_type=chess.QUEEN, color=chess.WHITE))

        black_pieces = 0
        black_pieces += 100 * len(board.pieces(piece_type=chess.PAWN, color=chess.BLACK))
        black_pieces += 300 * len(board.pieces(piece_type=chess.BISHOP, color=chess.BLACK))
        black_pieces += 300 * len(board.pieces(piece_type=chess.KNIGHT, color=chess.BLACK))
        black_pieces += 500 * len(board.pieces(piece_type=chess.ROOK, color=chess.BLACK))
        black_pieces += 900 * len(board.pieces(piece_type=chess.QUEEN, color=chess.BLACK))

        return white_pieces - black_pieces

    def PST_score(self, board: chess.Board, piece: chess.Piece):
        # PST = Piece-Square Table
        pawn_PST = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        knight_PST = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 0, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        bishop_PST = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        rook_PST = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        queen_PST = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        king_PST = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

        dictionary = {  # integers komen overeen meet piece_type e.g. chess.PAWN = 1
            1: pawn_PST,
            2: knight_PST,
            3: bishop_PST,
            4: rook_PST,
            5: queen_PST,
            6: king_PST
        }

        white = 0
        black = 0
        for i in board.pieces(piece, chess.WHITE):
            PST = dictionary[piece]
            white += PST[i]
        for i in board.pieces(piece, chess.BLACK):
            PST = dictionary[piece]
            black -= PST[chess.square_mirror(i)]  # chess.square_mirror() spiegelt het speelvlak horizontaal: zo kunnen de PSTs ook gebruikt worden voor zwart
        return white + black

    def castle_score(self, board: chess.Board):
        if board.turn:
            if ( board.castling_rights & chess.BB_H1 and (chess.BB_G1 & board.occupied) == 0 and (chess.BB_F1 & board.occupied) == 0 ) or ( board.castling_rights & chess.BB_A1 and (chess.BB_B1 & board.occupied) == 0 and (chess.BB_C1 & board.occupied) == 0 and (chess.BB_D1 & board.occupied) == 0 ):  # castlen met 1 van de rooks mogelijk?
                score = 90
            else:
                score = 0
            return score

        else:
            if ( board.castling_rights & chess.BB_H8 and (chess.BB_G8 & board.occupied) == 0 and (chess.BB_F8 & board.occupied) == 0 ) or ( board.castling_rights & chess.BB_A8 and (chess.BB_B8 & board.occupied) == 0 and (chess.BB_C8 & board.occupied) == 0 and (chess.BB_D8 & board.occupied) == 0 ):
                score = 90
            else:
                score = 0
            return -score

    def check_score(self, board: chess.Board):
        if board.turn:
            if board.is_check():
                return -90
            else:
                return 0
        else:
            if board.is_check():
                return 90
            else:
                return 0

    def get_piece_worth(self, piece: chess.Piece):
        if piece.piece_type == chess.PAWN:
            return 100
        elif piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT:
            return 300
        elif piece.piece_type == chess.ROOK:
            return 500
        elif piece.piece_type == chess.QUEEN:
            return 900
        elif piece.piece_type == chess.KING:
            return 1000

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
                effective_attacker_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in sorted(attackers)[0:len(defenders)])  # dit zijn de attackers die de attacker gaat gebruiken
                loss = defender_worth + self.get_piece_worth(last_moved_piece) - effective_attacker_worth  # defender verliest alle defenders en het stuk dat hij naar voor zet
                return loss
            elif len(attackers) == len(defenders):
                effective_defender_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in sorted(defenders)[0:len(defenders)-1])
                loss = -attacker_worth + self.get_piece_worth(last_moved_piece) + effective_defender_worth
                return loss
            elif len(attackers) < len(defenders):
                if chess.KING in attackers:
                    attackers.remove(chess.KING)
                effective_defender_worth = sum(self.get_piece_worth(board.piece_at(s)) for s in sorted(defenders)[0:len(attackers)])  # dit zijn de defenders die de defender gaat gebruiken
                loss = effective_defender_worth + self.get_piece_worth(last_moved_piece) - attacker_worth  # attacker verliest alle attackers
                return loss
            else:
                return 0
        return 0

    def board_value(self, board: chess.Board):
        if board.is_checkmate():
            if board.turn:  # chess.WHITE = True
                return -float("inf")
            else:
                return float("inf")
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        material = self.material_score(board)

        pawn_PST = self.PST_score(board, chess.PAWN)
        knight_PST = self.PST_score(board, chess.KNIGHT)
        bishop_PST = self.PST_score(board, chess.BISHOP)
        rook_PST = self.PST_score(board, chess.ROOK)
        queen_PST = self.PST_score(board, chess.QUEEN)
        king_PST = self.PST_score(board, chess.KING)
        PST = pawn_PST + knight_PST + bishop_PST + rook_PST + queen_PST + king_PST

        castle = self.castle_score(board)

        check = self.check_score(board)

        danger = self.danger_score(board)

        board_value = material + PST + castle + check + danger

        if not board.turn:
            return board_value
        else:
            return -board_value

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, board):
        key = self.get_key(board)
        if key in self.table:
            return self.table[key]
        return None

    def store(self, board, value):
        key = self.get_key(board)
        self.table[key] = value

    def get_key(self, board):
        return board.epd()

