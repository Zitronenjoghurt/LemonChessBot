import re

CELL_PATTERN = r'^[a-h][1-8]$'

def is_valid_chess_cell(value: str) -> bool:
    return bool(re.match(CELL_PATTERN, value))