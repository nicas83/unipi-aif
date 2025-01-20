# Artificial Intelligence Course A.A 2024-2025

The project is based on the MiniHack-Skill-Custom-v0 environment and uses the LevelGenerator to create a more complex environment 
within which the agent will have to move. It is about finding an optimal path using a few steps from the starting point to the target point, 
while escaping the danger of crossing the path with the wolf (the monster) and navigating around the lava cell (obstacles). 

This project has a dual purpose. On the one hand, we calculate the agent's moves based on the best possible path, through the use of an informed search algorithm 
based on a heuristic and information that defines the distance from the goal. On the other hand, we considered the minihack environment as a competitive game in which 
the best move made by the agent also depends on what it observes of the environment and the other agents (the wolf in the case of minihack). 

To do this, two algorithms were used, **Astar-search** for the “dynamic” pathfinding and **MinMax** for the competitive environment.

For a correct execution of the code it is necessary to install the 3.10 version of python (it is mandatory for nle).   
In a Linux environment follow the installation steps in the notebook in the **Environment Configuration** section

In a MacOS environment it is suggested to activate conda environment using the **minihack_env.yml** provided, following these instructions:

```bash
conda env create -f minihack_env.yml
conda activate minihack