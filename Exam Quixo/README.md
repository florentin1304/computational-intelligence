# Quixo Game Project

## Overview
This project presents a comprehensive implementation of the Quixo board game, featuring different AI agents (MinMax and AlphaZero) and a graphical user interface (GUI) for an enhanced user experience. The project is structured into distinct packages, each specializing in a specific aspect of the game and its functionalities.

## Project Structure
The project is divided into the following main packages, each containing its own detailed README file:

1. **AlphaZero**: This package includes the implementation of the AlphaZero agent, utilizing deep learning and Monte Carlo Tree Search (MCTS) to provide a challenging AI opponent.

2. **MinMax**: Contains the implementation of the MinMax algorithm with Alpha-Beta pruning, offering a strategic AI opponent based on traditional game theory principles.

3. **GUI**: The graphical user interface package, offers an interactive way for users to play Quixo against different AI agents or human players.

Each package's README provides in-depth information about its contents, functionalities, and usage.

## Results Analysis
Alongside these packages, the project includes a Jupyter notebook (`matches.ipynb`) that serves to analyze and visualize the outcomes of matches played between different AI agents and the Random Player. 

The first table shows the data of matches played between our agents against a Random player. The results show that both AlphaZero and Minimax are able to win all matches against the Random Player, regardless of the number of MCTS searches or depth analysis performed. This is expected, as the Random Player makes random moves and does not utilize any strategy.

| Match | Player Settings | Winrate | Loserate | Drawrate | Number of Games |
|-------|-----------------|---------|----------|----------|-----------------|
| AlphaZero vs Random | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs AlphaZero | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| AlphaZero vs Random | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs AlphaZero | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| AlphaZero vs Random | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs AlphaZero | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| AlphaZero vs Random | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs AlphaZero | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 10 |
| MinMax vs Random | depth=1 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs MinMax | depth=1 | 100.0% | 0.0% | 0.0% | 10 |
| MinMax vs Random | depth=2 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs MinMax | depth=2 | 100.0% | 0.0% | 0.0% | 10 |
| MinMax vs Random | depth=3 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs MinMax | depth=3 | 100.0% | 0.0% | 0.0% | 10 |
| MinMax vs Random | depth=4 | 100.0% | 0.0% | 0.0% | 10 |
| Random vs MinMax | depth=4 | 100.0% | 0.0% | 0.0% | 10 |

In the results obtained here, it can be seen that the AlphaZero method performs much better than the Minimax method, being able to not lose any games to the latter. Furthermore, from the results it is possible to observe how the player who starts is probably at a greater advantage, Minimax being able to draw more frequently those games where it starts first and has a high depth analysis.

| Match | MinMax Settings | AlphaZero Settings | AlphaZero Winrate | MinMax Winrate | Drawrate | Number of Games |
|-------|-----------------|--------------------|---------|----------|----------|-----------------|
| AlphaZero vs MinMax | depth=1 | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=1 | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=2 | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=2 | num_searches=800, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=3 | num_searches=800, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| MinMax vs AlphaZero | depth=3 | num_searches=800, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=4 | num_searches=800, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=4 | num_searches=800, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=1 | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=1 | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=2 | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=2 | num_searches=1600, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=3 | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=3 | num_searches=1600, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=4 | num_searches=1600, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=4 | num_searches=1600, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=1 | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=1 | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=2 | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=2 | num_searches=2400, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=3 | num_searches=2400, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| MinMax vs AlphaZero | depth=3 | num_searches=2400, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=4 | num_searches=2400, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=4 | num_searches=2400, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| AlphaZero vs MinMax | depth=1 | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=1 | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=2 | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| MinMax vs AlphaZero | depth=2 | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=3 | num_searches=3200, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| MinMax vs AlphaZero | depth=3 | num_searches=3200, C=2 | 100.0% | 0.0% | 0.0% | 3 |
| AlphaZero vs MinMax | depth=4 | num_searches=3200, C=2 | 0.0% | 0.0% | 100.0% | 3 |
| MinMax vs AlphaZero | depth=4 | num_searches=3200, C=2 | 0.0% | 0.0% | 100.0% | 3 |





## Getting Started

### Prerequisites
The packages required to run the project are listed in the `requirements.txt` file. To install them, run the following command in the project's root directory:

```bash
pip install -r requirements.txt
```

### Running the Game
Ensure all dependencies are installed. Run `main_ui.py` to start the game. From the main menu, select the desired AI agent and configure settings if necessary. Click 'Start' to initiate the game. Have fun!