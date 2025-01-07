import heapq
from collections import deque
from strategy import calculate_terrain_cost, calculate_combined_heuristic
from utils import directions, forbidden_cells, manhattan_distance


def get_successors(current_pos, monster_pos, chars_map):
    valid_successors = []

    try:
        for dx, dy in directions:
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            cell_content = chars_map[next_pos]
            if cell_content not in forbidden_cells:
                valid_successors.append(next_pos)
    except:
        print("Errore: ")

    valid_successors.sort()
    return valid_successors

def BFS_search(chars_map, hero_pos, monster_pos, goal_pos):

    # Inizializza la coda per BFS: (posizione, percorso)
    queue = deque([(hero_pos, [hero_pos])])
    visited = {hero_pos}  # Set di posizioni visitate

    while queue:
        current_pos, path = queue.popleft()

        # Se abbiamo raggiunto l'obiettivo
        if current_pos == goal_pos:
            return path

        # Esplora tutte le direzioni possibili
        successors = get_successors(current_pos, monster_pos, chars_map)
        for next_pos in successors:
            # # Controlla la distanza dal mostro se presente
            if monster_pos:
                monster_dist = manhattan_distance(next_pos, monster_pos)
                if monster_dist <= 1:  # Distanza di sicurezza dal mostro
                    continue

            # Aggiungi la nuova posizione alla coda
            if next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return None  # Nessun percorso trovato


def Astar_search(chars_map, hero_pos, monster_pos, goal_pos):

    # Inizializza la coda di priorità con: (f_score, g_score, pos, path)
    start = hero_pos
    pq = [(0, 0, 0, start, [start])]
    visited = {start: 0}  # position -> g_score

    while pq:
        f, path_len, g, current, path = heapq.heappop(pq)

        # Obiettivo raggiunto
        if current == goal_pos:
            # if is_path_safe(path, chars_map, monster_pos):
            return path
            # continue

        # Esplora i successori
        successors = get_successors(current, monster_pos, chars_map)
        for next_pos in successors:
            # Calcola nuovo g_score
            new_g = g + 1
            new_path_len = path_len + 1

            # Applica penalità basate sul terreno
            terrain_cost = calculate_terrain_cost(next_pos, chars_map)
            new_g += terrain_cost

            # Se troviamo un percorso migliore
            if next_pos not in visited or new_g < visited[next_pos]:
                visited[next_pos] = new_g

                # Calcola l'euristica combinata
                h = calculate_combined_heuristic(next_pos, goal_pos, chars_map, monster_pos)

                f = new_g + h
                heapq.heappush(pq, (f, new_path_len, new_g, next_pos, path + [next_pos]))

    return None

def minMax_search(chars_map, hero_pos, monster_pos, goal_pos, max_depth=3):
    """A* integrato con MinMax per considerare le mosse del mostro."""

    def evaluate_state(pos, monster_pos, depth):
        """Valuta lo stato corrente considerando la posizione dell'eroe e del mostro."""
        return calculate_combined_heuristic(pos, goal_pos, chars_map, monster_pos)

    def minimax(pos, monster_pos, depth, alpha, beta, is_max):
        """Implementa MinMax con alpha-beta pruning."""
        if depth == 0:
            return evaluate_state(pos, monster_pos, depth)
        # 2. Controllo stati terminali
        if pos == goal_pos:
            return float('inf')  # Massimo punteggio possibile
        if pos == monster_pos:
            return float('-inf')  # Minimo punteggio possibile

        # 3. Controllo mosse disponibili
        if is_max:
            successors = get_successors(pos, monster_pos, chars_map)
        else:
            successors = get_monster_moves(monster_pos, chars_map)

        if not successors:
            return evaluate_state(pos, monster_pos)

        if is_max:  # Turno dell'eroe
            max_eval = float('-inf')
            successors = get_successors(pos, monster_pos, chars_map)
            for next_pos in successors:
                eval = minimax(next_pos, monster_pos, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # Turno del mostro
            min_eval = float('inf')
            monster_moves = get_monster_moves(monster_pos, chars_map)
            for next_monster_pos in monster_moves:
                eval = minimax(pos, next_monster_pos, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(pos, monster_pos, path):
        """Determina la migliore mossa considerando le possibili risposte del mostro."""
        best_score = float('-inf')
        best_move = None
        successors = get_successors(pos, monster_pos, chars_map)

        for next_pos in successors:
            score = minimax(next_pos, monster_pos, max_depth, float('-inf'), float('inf'), False)
            if score > best_score: #or best_score == float('-inf'):
                best_score = score
                best_move = next_pos

        return best_move

        # Trova la migliore mossa considerando la risposta del mostro
    path = [hero_pos]
    best_next_pos = get_best_move(path[0], monster_pos, path)
    path += [best_next_pos]

    return path

def get_monster_moves(monster_pos, chars_map):
    """Restituisce le possibili mosse del mostro."""
    moves = []
    x, y = monster_pos
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-direzioni

    for dx, dy in directions:
        next_pos = (x + dx, y + dy)
        cell_content = chars_map[next_pos]
        if cell_content not in forbidden_cells:
            moves.append(next_pos)

    return moves