# Quixo Game - User Interface (UI) Module

## Overview
The UI module for the Quixo game project provides an interactive graphical user interface for users to play Quixo against the various AI agents implemented. On the GUI it is also possible not only to play against these agents but to see games played between the latters! It is built using Python with the integration of `pygame` and `tkinter` libraries. A brief introduction to these libraries is provided below.

#### Pygame
`Pygame` is a set of Python modules designed for writing video games by simplifying tasks like rendering graphics, managing sounds, and handling user input. `Pygame` in this project is used to render the game board, manage game states, and handle user interactions within the game window.

#### Tkinter
`Tkinter` is a standard GUI toolkit for Python. The library provides a fast and easy way to create GUI applications, making it ideal for applications that don't require a complex or heavily themed interface. `Tkinter` in this project is used to create the main menu and settings interface, allowing users to choose AI agents and configure game settings before starting a game session.


## Components
The UI module comprises three main components:

1. **GameUI.py**: This file contains the `GameUI` class, which extends the `Game` class from the `game` module. It is responsible for rendering the game board and handling the graphical representation of the Quixo game using `pygame`. It includes functionality for drawing the game board, cells, and updates during gameplay. This file contains everything you need to play with the Quixo UI.

2. **MenuUI.py**: This file implements the main menu interface using `tkinter`. It provides options to start the game, choose between different AI agents (MinMaxPlayer, AlphaZeroPlayer, RandomPlayer), and change their available settings.

3. **SelectPlayerFrames.py**: This file contains two classes, `MinmaxFrame` and `AlphaZeroFrame`, both of which extend the `tkinter` `Frame` class. These classes provide the user interface for configuring the settings specific to MinMax and AlphaZero players, such as setting the depth for MinMax and the search count for AlphaZero.

