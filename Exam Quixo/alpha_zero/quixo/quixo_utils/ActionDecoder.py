import random
import numpy as np
from ..QuixoGameLogicWrapper import GameLogicWrapper
from ..QuixoGameLogicOrig import Move


class ActionDecoder:
    def __init__(self):
        slides = [Move.BOTTOM, Move.TOP, Move.RIGHT, Move.LEFT]

        self.valid_moves = []
        for i in range(5):
            for j in range(5):
                for s in slides:
                    g = GameLogicWrapper()
                    acceptable = g.move(from_pos=(i,j), slide=s, player_id=0)
                    if acceptable:
                        self.valid_moves.append( [ (i,j), s  ] )
        
        self.num_valid_moves = len(self.valid_moves)

        # self.flip_list_translate = []
        # for i in range(self.num_valid_moves):
        #     move = self.convert_move_flip(i)
        #     self.flip_list_translate.append(self.find_index(move))

        # self.rotate_list_translate = []
        # for i in range(self.num_valid_moves):
        #     move = self.convert_move_90(i)
        #     self.rotate_list_translate.append(self.find_index(move))

        self.flip_list_translate = [None for _ in range(self.num_valid_moves)]
        for i in range(self.num_valid_moves):
            move_flipped = self.convert_move_flip(i)
            self.flip_list_translate[ self.find_index(move_flipped) ] = i

        self.rotate_list_translate = [None for _ in range(self.num_valid_moves)]
        for i in range(self.num_valid_moves):
            move_rotated = self.convert_move_90(i)
            self.rotate_list_translate[self.find_index(move_rotated)] = i
            

    def convert_move_90(self, index): #-> tuple[int, int, Move]:
        # convert counter-clockwise 90 degrees
        assert index < self.get_num_valid_moves()
        action = self.valid_moves[index]
        if action[1] == Move.TOP:
            move = Move.LEFT
        elif action[1] == Move.LEFT:
            move = Move.BOTTOM
        elif action[1] == Move.BOTTOM:
            move = Move.RIGHT
        else:
            move = Move.TOP

        board = np.zeros((5,5), dtype=int)
        board[action[0][1], action[0][0]] = 1 
        board = np.rot90(board)
        i, j = np.where(board == 1)
        return ((j[0], i[0]), move)

    def convert_move_flip(self, index): #-> tuple[int, int, Move]:
        # vertical flip (flip on horizontal axis)

        assert index < self.get_num_valid_moves()
        action = self.valid_moves[index]
        if action[1] == Move.BOTTOM:
            move = Move.TOP
        elif action[1] == Move.TOP:
            move = Move.BOTTOM
        else: 
            move = action[1]

        board = np.zeros((5,5), dtype=int)
        board[action[0][1], action[0][0]] = 1 
        board = np.flipud(board)
        i, j = np.where(board == 1)
        return ((j[0], i[0]), move)
    
    def get_index_after_flip(self, index):
        return self.flip_list_translate[index]
    
    def get_index_after_rotate(self, index):
        return self.rotate_list_translate[index]

    def find_index(self, move: tuple[(int, int), Move]):
        ((c0,r0),slide0) = move
        for i in range(self.num_valid_moves):
            ((c,r),slide) = self.valid_moves[i]
            if c0 == c and r0 == r and slide0.value == slide.value:
                return i
        return -1


    def decode_action(self, index):
        """
        decodes the action
        returns: from_pos: tuple[int, int], slide: Move
        """
        assert index < self.get_num_valid_moves()
        action = self.valid_moves[index]
        return action[0], action[1]

    def get_num_valid_moves(self):
        return self.num_valid_moves

    def __call__(self, index):
        return self.decode_action(index)