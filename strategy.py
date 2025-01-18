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


