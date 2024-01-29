from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from pathlib import Path
import os

from gui.SelectPlayerFrames import MinmaxFrame, AlphaZeroFrame

import pygame
from gui.GameUI import GameUI, WIDTH, HEIGHT

from MinMaxPlayer import MinMaxPlayer
from AlphaZeroPlayer import AlphaZeroPlayer
from RandomPlayer import RandomPlayer


script_folder_path = Path(__file__).parent
FILES_PATH = os.path.join(script_folder_path, "Files")

class MainFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent

        image = Image.open(os.path.join(FILES_PATH,'quixo_logo.png'))
        im_size = image.size
        ratio = im_size[0] / self.parent.window_height
        newsize = (int(im_size[0]/ratio), int(im_size[1]/ratio))
        image = image.resize(newsize)
        image = ImageTk.PhotoImage(image)

        image_label = Label(self, image=image)
        image_label.photo = image
        image_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        button1 = ttk.Button(self, text="Play", command=self.parent.get_players)
        button1.place(relx=0.5, rely=0.5, anchor=CENTER)
        button2 = ttk.Button(self, text="How to play", command=self.parent.how_to_play)
        button2.place(relx=0.5, rely=0.7, anchor=CENTER)
        button3 = ttk.Button(self, text="Quit", command=self.parent.exit_game)
        button3.place(relx=0.5, rely=0.9, anchor=CENTER)

class SelectPlayer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        image = Image.open(os.path.join(FILES_PATH,'quixo_logo.png'))
        im_size = image.size
        ratio = im_size[0] / self.parent.window_height
        newsize = (int(im_size[0]/ratio), int(im_size[1]/ratio))
        image = image.resize(newsize)
        image = ImageTk.PhotoImage(image)

        image_label = Label(self, image=image)
        image_label.photo = image
        image_label.grid(row=0, column=0, columnspan=2)


        label1 = Label(self, text="Player 1:")
        label1.grid(row=1, column=0)

        dropdown_options = ["Select Player 1", "Human", "Random", "MinMax", "AlphaZero"]
        self.current_frame_p1 = None
        self.p1_frames = [MinmaxFrame(self), AlphaZeroFrame(self)]
        self.var1 = StringVar(value=dropdown_options[0])
        p1_dropdown = ttk.OptionMenu(self, self.var1, *(dropdown_options), \
                                     command=lambda x: self.dropdown_callback(x, \
                                                                              current_frame=self.current_frame_p1, \
                                                                                list_frames=self.p1_frames, \
                                                                                row=2))
        p1_dropdown.grid(row=1, column=1)


        label2 = Label(self, text="Player 2:")
        label2.grid(row=3, column=0)
        
        dropdown2_options = ["Select Player 2", "Human", "Random", "MinMax", "AlphaZero"]
        self.current_frame_p2 = None
        self.p2_frames = [MinmaxFrame(self), AlphaZeroFrame(self)]
        self.var2 = StringVar(value=dropdown2_options[0])
        p2_dropdown = ttk.OptionMenu(self, self.var2, *(dropdown2_options), \
                                     command=lambda x: self.dropdown_callback(x, \
                                                                        current_frame=self.current_frame_p2, \
                                                                        list_frames=self.p2_frames, \
                                                                        row=4))
        p2_dropdown.grid(row=3, column=1)


        
        button_done = ttk.Button(self, text="Back", command=self.parent.main_menu)
        button_done.grid(row=5, column=0)

        button_done = ttk.Button(self, text="Play", command=self.parent.play)
        button_done.grid(row=5, column=1)

    def get_players(self):
        p1_str = self.var1.get()
        p2_str = self.var2.get()
        p1 = self.create_player(p1_str, self.p1_frames)
        p2 = self.create_player(p2_str, self.p2_frames)
        return (p1, p2)
    
    def create_player(self, player_str, list_frames):
        if player_str == "Human":
            return "human"
        elif player_str == "Random":
            return RandomPlayer()
        elif player_str == "MinMax":
            depth = list_frames[0].get_values()["depth"]
            if depth == None:
                return None
            return MinMaxPlayer(depth=depth)
        elif player_str == "AlphaZero":
            num_searches = list_frames[1].get_values()["num_searches"]
            c = list_frames[1].get_values()["c"]
            print(list_frames[1].get_values())
            if num_searches == None or c == None:
                return None
            return AlphaZeroPlayer(num_searches=num_searches, C=c)
        else:
            raise Exception(f"Player not recognized {player_str}")

    def dropdown_callback(self, var, current_frame, list_frames, row):
        print(f"the variable has changed to '{var}'")
        for f in list_frames:
            f.grid_forget()
            
        if var == "MinMax":
            current_frame = list_frames[0]
            current_frame.grid(row=row, column=0, columnspan=2)
        elif var == "AlphaZero":
            current_frame = list_frames[1]
            current_frame.grid(row=row, column=0, columnspan=2)
        else: 
            current_frame = None
        




class Menu(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.window_height = 200
        self.window_width = 200

        self.title("Quixo")
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)

        self.game_size = (WIDTH, HEIGHT)

        self.frames = [MainFrame(self), 
                       SelectPlayer(self)]
        self.frames[0].pack(fill=BOTH, expand=True)

        
    def unpack_all(self):
        for f in self.frames:
            f.pack_forget()

    def main_menu(self):
        self.unpack_all()
        self.frames[0].pack(fill=BOTH, expand=True)

    def get_players(self):
        self.unpack_all()
        self.frames[1].pack(fill=BOTH, expand=True)


    def how_to_play(self):
        messagebox.showinfo("How to play","You can take a piece by selecting it and then selecting the direction you want to move it in. \n")

    
    def play(self):
        p1,p2 = self.frames[1].get_players()
        print(p1,p2)
        if p1 is None or p2 is None:
            return
        
        # Initialize Pygame
        self.withdraw()

        print("Welcome to Quixo!")
        pygame.init()
        print("Initializing Pygame...")
        screen = pygame.display.set_mode(self.game_size)
        pygame.display.set_caption('Quixo Game')
        g = GameUI(screen)    
        winner = g.play(p1, p2)
        print(f"Winner: Player {winner}")

        self.update()
        self.deiconify()
        self.main_menu()



    def exit_game(self):
        self.destroy()