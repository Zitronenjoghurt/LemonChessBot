import re
from pydantic import BaseModel, Field
from src.constants.color import ChessColor

SAN_PATTERNS = [
    (r'([a-h][1-8])$', "Pawn moves to {}"),
    (r'([a-h])x([a-h][1-8]) e\.p\.$', "Pawn captures on {} en passant"),
    (r'([a-h])x([a-h][1-8])Q$', "Pawn captures on {} and promotes to Queen"),
    (r'([a-h])x([a-h][1-8])$', "Pawn captures on {}"),
    (r'([a-h][1-8])Q$', "Pawn moves to {} and promotes to Queen"),
    (r'([QRBN])([a-h][1-8])$', "{} moves to {}"),
    (r'([QRBN])x([a-h][1-8])$', "{} captures on {}")
]

PIECE_NAMES = {
    'Q': 'Queen',
    'R': 'Rook',
    'B': 'Bishop',
    'N': 'Knight'
}

class GameState(BaseModel):
    chess_board: object
    next_to_move: int
    half_move_counter: int
    full_move_counter: int
    initial_pawn_masks: list[str]
    available_moves: list
    check_states: list[bool]
    en_passant_indices: list[int]
    kingside_castling_rights: list[bool]
    queenside_castling_rights: list[bool]
    can_castle_kingside: list[bool]
    can_castle_queenside: list[bool]
    king_indices: list[int]
    kingside_rook_indices: list[int]
    queenside_rook_indices: list[int]
    winner: int
    draw: bool
    checkmate: bool
    resign: bool
    stalemate: bool
    remis: bool
    move_log: list
    san_log: list[str]
    tick: int = Field(default = 0)

    def is_ongoing(self) -> bool:
        return self.winner == 2 and not self.draw
    
    def last_san_to_description(self) -> str:
        if len(self.san_log) == 0:
            return "*no move yet*"
        
        last_color = ChessColor.WHITE if self.next_to_move == 1 else ChessColor.BLACK

        last_san = self.san_log[-1]
        for pattern, desc in SAN_PATTERNS:
            match = re.match(pattern, last_san)
            if match:
                groups = match.groups()
                # Replace piece letters with full names if present
                groups = tuple(PIECE_NAMES.get(g, g) for g in groups)
                return f"{last_color.name.capitalize()} " + desc.format(*groups)
            
        return last_san