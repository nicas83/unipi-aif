from utils import is_valid_position, manhattan_distance

heuristic_weights = {
    'distance': 1.0,  # Peso per la distanza dall'obiettivo
    'short_distance': 2.0,  # Peso per la distanza ravvicinata dall'obiettivo
    'target': 5.0,
    'monster': 1.0,  # Peso per l'evitamento del mostro
    'you_died': 5.0,
    'lava': 3.0,  # Peso per l'evitamento della lava
    'corridor': 0.5  # Peso per preferire corridoi sicuri
}


def calculate_combined_heuristic(pos, goal_pos, chars_map, monster_pos):
    """
    Calcola un'euristica combinata che considera multipli fattori.
    Score alto = posizione favorevole
    Score basso = posizione sfavorevole
    """
    h_score = 0
    weights = heuristic_weights

    # 1. Componente distanza dall'obiettivo
    base_distance = manhattan_distance(pos, goal_pos)
    try:
        if base_distance == 0:
            # Siamo sull'obiettivo, massimo punteggio
            h_score += weights['target']
        else:
            # Più siamo lontani, più il punteggio diminuisce
            # Usiamo una funzione decrescente inversamente proporzionale alla distanza
            distance_score = weights['distance'] / base_distance  # +1 per evitare divisione per zero

            # Bonus aggiuntivo se siamo molto vicini all'obiettivo (< 3 celle)
            if base_distance <= 3:
                distance_score *= 1.5  # aumentiamo del 50% il punteggio

            h_score += distance_score

    except Exception as e:
        print(f"Error during distance calculation: {e}")

    # 2. Componente mostro
    if monster_pos is not None:
        monster_distance = manhattan_distance(pos, monster_pos)
        try:
            # Base safety score: più siamo lontani dal mostro, più punti prendiamo
            monster_score = (monster_distance * weights['monster']) / 10  # dividiamo per 10 per normalizzare
            #monster_score = weights['monster']/monster_distance
            if monster_distance==0:
                h_score -= weights['you_died']
            # Penalità pesante se siamo troppo vicini al mostro (< 3 celle)
            elif monster_distance < 2:
                monster_score = weights['monster'] / monster_distance  # penalità inversamente proporzionale

            # Se siamo più vicini all'obiettivo che al mostro, riduciamo la penalità
            if base_distance < monster_distance:
                monster_score *= 0.7  # riduciamo del 30% la penalità

            h_score -= monster_score

        except Exception as e:
            print(f"Error during monster calculation: {e}")

    return h_score

def calculate_combined_heuristic2(pos, goal_pos, chars_map, monster_pos):
    """Calcola un'euristica combinata che considera multipli fattori."""
    h_score = 0
    weights = heuristic_weights

    # 1. Distanza base (Manhattan con diagonali)
    base_distance = manhattan_distance(pos, goal_pos)
    try:
        if base_distance == 0:
            h_score += weights['target']
        else:
            h_score = weights['distance'] / base_distance
            # if base_distance <= 5:
            #     # agevolo i path che sono più vicini al target
            #     h_score += (base_distance * weights['distance']) / base_distance
            # else:
            #     h_score -= (base_distance * weights['distance']) / base_distance
            #
            # # incremento il peso per le distanze più ravvicinate
            # if base_distance <= 3:
            #     h_score += (base_distance * weights['short_distance']) / base_distance
    except Exception as e:
        print(f"Error during euristics calculation: {e}")



    # 2. Componente mostro
    if monster_pos is not None:
        monster_distance = manhattan_distance(pos, monster_pos)
        # calcolare bene l'euristica... se la distanza dall'obiettivo è minore rispetto al mostro, riduco la penalità
        # if monster_distance < 2:
            # Penalità esponenziale per avvicinarsi al mostro
        # monster_penalty = monster_distance ** 2
        result = monster_distance/weights['monster']
        h_score = h_score-result

    # 3. Componente lava
    # lava_penalty = calculate_lava_penalty(pos, chars_map)
    # h_score -= lava_penalty * weights['lava']

    # 4. Componente corridoio sicuro
    corridor_bonus = calculate_corridor_safety(pos, chars_map)
    h_score += corridor_bonus * weights['corridor']

    return h_score


def calculate_lava_penalty(pos, chars_map):
    """Calcola una penalità basata sulla vicinanza alla lava."""
    penalty = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            check_pos = (pos[0] + dx, pos[1] + dy)
            if chars_map[check_pos] == 125:  # Lava
                # Penalità maggiore per lava adiacente
                if dx == 0 and dy == 0:
                    penalty += 1000  # Sulla lava
                elif abs(dx) + abs(dy) == 1:
                    penalty += 50  # Adiacente
                else:
                    penalty += 10  # Diagonale
    return penalty


def calculate_corridor_safety(pos, chars_map):
    """Calcola un bonus per posizioni in corridoi sicuri."""
    safe_neighbors = 0
    total_neighbors = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            check_pos = (pos[0] + dx, pos[1] + dy)
            if is_valid_position(check_pos, chars_map):
                total_neighbors += 1
                if chars_map[check_pos] == 46:  # Pavimento sicuro
                    safe_neighbors += 1

    # Restituisce un rapporto di sicurezza
    return safe_neighbors / max(1, total_neighbors)

def calculate_risk_cost(pos, monster_pos, mode):
    """Calcola il costo di rischio basato sulla modalità e distanza dal nemico."""
    if not monster_pos:
        return 0

    distance = abs(pos[0] - monster_pos[0]) + abs(pos[1] - monster_pos[1])

    # Differenti pesi di rischio basati sulla modalità
    risk_weights = {
        'safe': 10.0,  # Alto peso al rischio, evita fortemente il nemico
        'cautious': 5.0,  # Peso moderato al rischio
        'aggressive': 2.0  # Basso peso al rischio
    }

    weight = risk_weights.get(mode, 5.0)

    # Il rischio aumenta esponenzialmente quando ci si avvicina al mostro
    if distance < 3:
        risk = weight * (3 - distance) ** 2
    else:
        risk = weight / (distance + 1)

    return risk

def calculate_terrain_cost(pos, chars_map):
    """Calcola il costo del terreno per una data posizione."""
    terrain_costs = {
        46: 1,  # Pavimento normale
        125: 1000,  # Lava (dovrebbe essere evitata dalla validazione)
        32: 1000,  # Muro (dovrebbe essere evitato dalla validazione)
        37: 0, # target
        '<': 2,  # Scale su (costo extra per evitare confusione con l'obiettivo)
        '>': 2  # Scale giù (costo extra per evitare confusione con l'obiettivo)
    }
    value = chars_map[pos]
    return terrain_costs.get(value, 1)
