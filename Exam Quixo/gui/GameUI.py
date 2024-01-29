import pygame
import sys
from pathlib import Path

from game import Game, Player, Move
from copy import deepcopy

from tkinter import *
from tkinter import messagebox

import time
import concurrent.futures #threading

import os

# Constants
WIDTH, HEIGHT = 505, 505  # Adjusted to fit the lines properly

ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS
LINE_WIDTH = 5


script_folder_path = Path(__file__).parent
FILES_PATH = os.path.join(script_folder_path, "Files")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

class GameUI(Game):
    def __init__(self, screen) -> None:
        super().__init__()
        
        self.screen = screen
        self._board_memory = None
        self.font = pygame.font.Font(os.path.join(FILES_PATH, "04B30.TTF"), 40)
        
    def __draw_board(self):
        self.screen.fill(WHITE)
        # Draw vertical lines between the squares
        for i in range(1, COLS):
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        # Draw horizontal lines between the squares
        for i in range(1, ROWS):
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        # Draw X and O marks
        for row in range(ROWS):
            for col in range(COLS):
                mark = self._board[row][col]
                if mark == 0:
                    pygame.draw.line(self.screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                    ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 3)
                    pygame.draw.line(self.screen, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                    (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 3)
                elif mark == 1:
                    pygame.draw.circle(self.screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                    CELL_SIZE // 2 - 20, 3)
                elif mark in [ord('T'), ord('B'), ord('L'), ord('R')]:
                    pygame.draw.rect(self.screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    if self._board_memory[row][col] == 0:
                        pygame.draw.line(self.screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                                    ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 3)
                        pygame.draw.line(self.screen, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                                        (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 3)
                    if self._board_memory[row][col] == 1:
                        pygame.draw.circle(self.screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                        CELL_SIZE // 2 - 20, 3)
        
        pygame.display.flip()
    
    def __draw_winner(self, winner):
        if winner != 10:
            pygame.mixer.music.load(os.path.join(FILES_PATH, "win_sound.mp3"))
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(os.path.join(FILES_PATH, "wawawa_sound.mp3"))
            pygame.mixer.music.play()

        display_string = f"Player {winner + 1} wins!" if winner != 10 else "Draw"
        print(display_string)
        self.screen.fill(WHITE)
        if winner == 0:
            pygame.draw.rect(self.screen, RED, (0, 0, WIDTH, HEIGHT), 5)
        else:
            pygame.draw.rect(self.screen, BLUE, (0, 0, WIDTH, HEIGHT), 5)
    

        text_surface = self.font.render(display_string, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
    
    def __draw_goodbye(self):
        print("Goodbye!")
        self.screen.fill(WHITE)
        text_surface = self.font.render("Goodbye!", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
                                        

    def __reset_board(self, from_pos):
        self._board[0, from_pos[0]] = self._board_memory[0, from_pos[0]]
        self._board[4, from_pos[0]] = self._board_memory[4, from_pos[0]]
        self._board[from_pos[1], 0] = self._board_memory[from_pos[1], 0]
        self._board[from_pos[1], 4] = self._board_memory[from_pos[1], 4]
    
    def __choose_slide(self, from_pos):
        possible_slide = self.possible_slide((from_pos[1], from_pos[0]))
        if possible_slide is None:
            return None
        self._board_memory = deepcopy(self._board)
        if Move.TOP in possible_slide:
            self._board[0, from_pos[0]] = ord('T')
        if Move.BOTTOM in possible_slide:
            self._board[4, from_pos[0]] = ord('B')
        if Move.LEFT in possible_slide:
            self._board[from_pos[1], 0] = ord('L')
        if Move.RIGHT in possible_slide:
            self._board[from_pos[1], 4] = ord('R')
        self.__draw_board()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Pygame
                    self.__draw_goodbye()
                    pygame.time.wait(1000)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = pygame.mouse.get_pos()
                    row = row // CELL_SIZE; col = col // CELL_SIZE
                    if self._board[row, col] == ord('T'):
                        self.__reset_board(from_pos)
                        return Move.TOP
                    elif self._board[row, col] == ord('B'):
                        self.__reset_board(from_pos)
                        return Move.BOTTOM
                    elif self._board[row, col] == ord('L'):
                        self.__reset_board(from_pos)
                        return Move.LEFT
                    elif self._board[row, col] == ord('R'):
                        self.__reset_board(from_pos)
                        return Move.RIGHT
            self.__draw_board()

    def wait_for_player_action(self, player):
        ok = False
        while not ok:
            from_pos, slide = player.make_move(self)
            ok = self.move(from_pos, slide, self.current_player_idx)
        self.current_player_idx = 1 if self.current_player_idx == 0 else 0
        winner = self.check_winner()

        return winner

    def play(self, player1: Player | str, player2: Player | str) -> int:
        '''Play the game. Returns the winning player'''
        history = []
        players = [player1, player2]
        winner = -1
        self.current_player_idx = 0
        while True:
            history.append(self.get_hashed_state())
            if len(history) > 6 and len(set(history[-6:])) == 2 and player1 != "human" and player2 != "human":
                winner = 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Pygame
                    self.__draw_goodbye()
                    pygame.time.wait(1000)
                    pygame.quit()
                    sys.exit()

                if winner < 0:
                    pygame.event.pump()
                    if players[self.current_player_idx] == "human":
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            row, col = pygame.mouse.get_pos()
                            row = row // CELL_SIZE; col = col // CELL_SIZE
                            from_pos = (row, col)
                            # choose the slide
                            slide = self.__choose_slide(from_pos)
                            if slide is None:
                                print("Mossa non valida")
                                Tk().wm_withdraw() #to hide the main window
                                messagebox.showinfo('Quixo Game','Mossa non valida')
                                continue
                            ok = self.move(from_pos, slide, self.current_player_idx)
                            if ok:
                                pygame.time.wait(200)
                                pygame.mixer.music.load(os.path.join(FILES_PATH, "pawn_sound.mp3"))
                                pygame.mixer.music.play()
                                self.current_player_idx = 1 if self.current_player_idx == 0 else 0
                                winner = self.check_winner()
                            else:
                                print("Mossa non valida")
                                Tk().wm_withdraw() #to hide the main window
                                messagebox.showinfo('Quixo Game','Mossa non valida')
                    else:
                        current_player = players[self.current_player_idx]
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            player_thread = executor.submit(self.wait_for_player_action,  #func
                                                            current_player) #args

                            while(player_thread.running()):
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        # Quit Pygame
                                        self.__draw_goodbye()
                                        pygame.time.wait(1000)
                                        pygame.quit()
                                        sys.exit()
                                pygame.event.pump()
                                self.__draw_board()

                            winner = player_thread.result()
                            e = pygame.event.Event(pygame.USEREVENT)
                            pygame.event.post(e)

            pygame.event.pump()
            self.__draw_board()
            
            if winner >= 0:
                pygame.time.wait(1000)
                self.__draw_winner(winner)
                pygame.time.wait(4000)
                break
        pygame.quit()
        #sys.exit()

        return winner