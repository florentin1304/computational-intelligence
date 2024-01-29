from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import numpy as np
from copy import deepcopy

from .quixo_utils.ActionDecoder import ActionDecoder
from .quixo_utils.StateEncoder import StateEncoder
from .QuixoGameLogicWrapper import GameLogicWrapper

class QuixoGame(Game):
    """
    This class specifies the QuixoGame class.
    Use 1 for player1 and -1 for player2.
    """

    def __init__(self):
        self.row_count = 5
        self.column_count = 5

        self.state_encoder = StateEncoder()
        self.action_decoder = ActionDecoder()

        self.action_size = self.action_decoder.get_num_valid_moves()
        self.p_game_to_logic = {
                                0: -1, # empty here = 0, empty logic = -1 
                                1: 0, # p1 here = 1, p1 logic = 0
                                -1: 1 # p2 here = -1, p1 logic = 1
                                }

        self.p_logic_to_game = {
                                -1: 0, # empty here = 0, empty logic = -1 
                                0: 1, # p1 here = 1, p1 logic = 0
                                1: -1 # p2 here = -1, p1 logic = 1
                                }

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board at start game 
        """
        return np.zeros(shape=(self.row_count, self.column_count))

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.row_count, self.column_count)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return self.action_size

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """

        # Setup Game Logic
        game_logic_board = self.state_encoder.to_game(board, 0)
        game_logic = GameLogicWrapper()
        game_logic.set_state(game_logic_board)
        game_logic.current_player_idx = self.p_game_to_logic[player]

        # Decode action and move in logic        
        from_pos, slide = self.action_decoder(action)
        ok = game_logic.move(from_pos, slide, self.p_game_to_logic[player])

        if not ok:
            raise Exception(f"Get next state: invalid action {from_pos}, {slide}")

        new_game_logic_board = game_logic.get_board()
        new_game_board = self.state_encoder.to_neutral(new_game_logic_board, player_id=0)

        return new_game_board, -player

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        #canonical_board = self.getCanonicalForm(board, player)
        valid_moves = np.zeros(shape=self.action_size)
        for action_i in range(self.action_size):
            from_pos, slide = self.action_decoder(action_i)
            if board[from_pos[1], from_pos[0]] != -1:
                valid_moves[action_i] = 1

        return valid_moves

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        game_state = self.state_encoder.to_game(board, player_id=0)
        g = GameLogicWrapper()
        g.set_state(game_state)
        game_logic_winner = g.check_winner()

        return self.p_logic_to_game[game_logic_winner]
        
    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        return player*board

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        rotate_map = self.action_decoder.rotate_list_translate
        flip_map = self.action_decoder.flip_list_translate
        symmetries = [(board, pi)]

        rot_board = deepcopy(board)
        rot_pi = deepcopy(np.array(pi))

        for i in range(3):
            rot_board = deepcopy(np.rot90(rot_board))
            rot_pi = deepcopy(rot_pi[rotate_map])
            symmetries.append( (rot_board, rot_pi.tolist()) )

        flip_board = deepcopy( np.flipud(board) )
        flip_pi = deepcopy(np.array(pi)[flip_map])
        symmetries.append( (flip_board, flip_pi.tolist()) )

        for i in range(3):
            flip_board = deepcopy(np.rot90(flip_board))
            flip_pi = deepcopy(flip_pi[rotate_map])
            symmetries.append( (flip_board, flip_pi.tolist()) )

        return symmetries

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        square_content = {1: "X", -1:"O", 0:"="}
        board_s = "".join(square_content[square] for row in board for square in row)
        return board_s

    def getEncodedBoard(self, board):
        encoded_board = np.stack(
            (board == 1, board == 0, board == -1)
        ).astype(np.float32)

        return encoded_board
    
    def getOpponentValue(self, value):
        return -1*value