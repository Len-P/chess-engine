import chess
import chess.polyglot
board = chess.Board()
with chess.polyglot.open_reader("human.bin") as reader:
  grandmaster_moves = []
  for entry in reader.find_all(board):
    grandmaster_moves.append(entry.move)
  print(grandmaster_moves)

