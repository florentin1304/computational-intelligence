import random
import tqdm
from game import Game, Move, Player

from AlphaZeroPlayer import AlphaZeroPlayer
from MinMaxPlayer import MinMaxPlayer

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


if __name__ == '__main__':
    
    wins = 0
    tot_games = 0
    num_games = 2

    t = tqdm.tqdm(range(num_games//2), desc="Playing games [MyPlayer 1st]")
    for i in t:
        g = Game()
        player1 = AlphaZeroPlayer(num_searches=2500, C=2, verbose=False)
        # player1 = AlphaZeroPlayer(policy_only=True)
        # player2 = RandomPlayer()
        player2 = MinMaxPlayer(depth=3)

        winner = g.play(player1, player2)
        wins += 1 if winner == 0 else 0
        tot_games += 1
        t.set_postfix(Winrate=wins/(tot_games))
    t.close()

    t = tqdm.tqdm(range(num_games//2), desc="Playing games [MyPlayer 2nd]")
    for i in t:
        g = Game()
        # player1 = RandomPlayer() 
        player1 = MinMaxPlayer(depth=3)
        player2 = AlphaZeroPlayer(num_searches=2500, C=2, verbose=False)
        # player2 = AlphaZeroPlayer(policy_only=True)

        winner = g.play(player1, player2)
        wins += 1 if winner == 1 else 0
        tot_games += 1
        t.set_postfix(Winrate=wins/(tot_games))
    t.close()

    print(f"Average Winrate {player2.__class__.__name__} vs {player1.__class__.__name__} over {num_games} games: {100*wins/num_games}%")
