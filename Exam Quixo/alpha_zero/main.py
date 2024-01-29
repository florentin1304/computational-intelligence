import logging

import coloredlogs

from Coach import Coach
from quixo.QuixoGame import QuixoGame as Game
from quixo.pytorch.QuixoNetWrapper import QuixoNetWrapper as nn
from utils import *

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 25,       # Temperature for exploration in training
    'updateThreshold': 0.55,    # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 128_000,   # Number of game examples to train the neural networks.
    'numMCTSSims': 50,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 30,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 2,             
    
    'parallelSelfPlay': True,
    'parallelArena': True,
    'pitVsRandom': True,

    'load_model': True,
    'checkpoint': './temp/',
    'load_folder_file': ('temp','checkpoint_7.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def main():
    log.info('Loading %s...', Game.__name__)
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        #nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
