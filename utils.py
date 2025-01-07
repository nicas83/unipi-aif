forbidden_cells = {32, 125, 100} #125=L, 32=Muro, 100=wolf
directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinali
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonali
        ]
def manhattan_distance(start, goal):
    x = abs(start[0] - goal[0])
    y = abs(start[1] - goal[1])
    #return  max(x,y) #considera la distanza diagonale
    return x+y

def normalize_coordinates(pos):
    """Normalizza le coordinate alla dimensione della mappa."""
    # x = pos[0] % self.map_height
    # y = pos[1] % self.map_width
    # return (x, y)
    return pos[0], pos[1]

def is_valid_position(pos, chars_map):
    """Verifica se una mossa è valida, usando coordinate normalizzate."""
    pos = normalize_coordinates(pos)
    h, w = chars_map.shape

    if not (0 <= pos[0] < h and 0 <= pos[1] < w):
        return False

    cell_content = chars_map[pos]
    return cell_content not in forbidden_cells

def is_path_safe(path, chars_map, monster_pos):
    """Verifica che il percorso sia sicuro."""
    if not path:
        return False

    for pos in path:
        # Verifica collisione con lava o altri oggetti non ammessi
        if chars_map[pos] in forbidden_cells:  # L
            return False

        # Verifica distanza dal mostro
        if monster_pos and manhattan_distance(pos, monster_pos) < 2:
            return False

    return True

