import time
from environment import create_level
from moving import DynamicPathfindingAgent
from search import minMax_search, Astar_search
from utils import is_path_safe, is_valid_position, manhattan_distance





def run_agent(env, game_map):
    agent = DynamicPathfindingAgent(map_width=11, map_height=11)
    done = False
    total_reward = 0

    try:
        # Visualizza lo stato iniziale
        print(f"\nPosizione iniziale eroe: {game_map.get_player_location()}")
        print(f"Posizione obiettivo: {game_map.get_goal_location()}")
        print(f"Posizione iniziale mostro: {game_map.get_monsters_location()}")
        while not done:
            # Visualizza lo stato corrente
            chars_map, hero_pos, monster_pos, goal_pos = game_map.get_map_state()
            if not is_valid_position(hero_pos, chars_map):
                print("ATTENZIONE: Posizione attuale non sicura!")
                break

            action, path = agent.get_next_move(game_map)
            print(f"Azione scelta: {action}")
            print(f"Path scelto: {path}")

            # Esegui l'azione
            state, reward, done, info = env.step(action)
            total_reward += reward
            # game_map = Map(state)
            env.render()
            # Breve pausa per vedere il rendering
            time.sleep(0.5)
            new_pos = game_map.get_player_location()
            current_hp = state["blstats"][21]
            max_hp = state["blstats"][22]
            print(f"HP: {current_hp}/{max_hp}")
            print(f"\nPosizione corrente eroe: {new_pos}")
            print(f"Posizione obiettivo: {goal_pos}")
            print(f"Posizione corrente mostro: {monster_pos}")

            if new_pos == goal_pos:
                print("Obiettivo raggiunto!")
                break

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        import traceback
        traceback.print_exc()
    finally:
        return total_reward

# Esempio di utilizzo
if __name__ == "__main__":
    game_map, env = create_level(11,11,2,(10,0),(2,0),(0,0))

    total_reward = run_agent(env, game_map)
    print(f"Reward totale: {total_reward}")