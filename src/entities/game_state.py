from pydantic import BaseModel, Field

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