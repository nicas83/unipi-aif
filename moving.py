from search import Astar_search, minMax_search

class DynamicPathfindingAgent:
    def __init__(self, map_width=11, map_height=11):

        self.current_path = None
        self.fallback_modes = ['safe', 'cautious', 'aggressive']
        self.current_mode = 'safe'
        self.map_width = map_width
        self.map_height = map_height

        self.direction_to_action = {
            (-1, 0): 0,  # Moving N
            (0, 1): 1,  # Moving E
            (1, 0): 2,  # Moving S
            (0, -1): 3,  # Moving W
            (-1, 1): 4,  # Moving NE
            (1, 1): 5,  # Moving SE
            (1, -1): 6,  # Moving SW
            (-1, -1): 7,  # Moving NW
            (0, 0): 46  # Rest
        }


    def convert_to_action(self, current, next_pos):
        """Converte una mossa in un indice di azione."""
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        return self.direction_to_action.get((dx, dy))

    def get_next_move(self, chars_map, hero_pos, monster_pos, goal_pos, algorithm='astar'):
        # Trova il percorso
        #
        if algorithm == 'astar':
            path = Astar_search(chars_map, hero_pos, monster_pos, goal_pos)
        else:
            path = minMax_search(chars_map, hero_pos, monster_pos, goal_pos, 4)

        if path and len(path) > 1:
            next_pos = path[1]
            action = self.convert_to_action(path[0], next_pos)
            if action is not None:
                return action, path
        # Se non troviamo un percorso sicuro, resta fermo
        return 46  # agent rest