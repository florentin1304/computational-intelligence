import logging
import os
import sys
from collections import deque
from pickle import Pickler, Unpickler
from random import shuffle
import threading
import multiprocessing

import numpy as np
from tqdm import tqdm

from Arena import Arena
from MCTS import MCTS
from quixo.QuixoRandomPlayer import RandomPlayer

log = logging.getLogger(__name__)


class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.trainExamplesHistory = []  # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    def executeEpisode(self, mcts):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard, currPlayer, pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []
        board = self.game.getInitBoard()
        curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard = self.game.getCanonicalForm(board, curPlayer)
            temp = 1.25*int(episodeStep < self.args.tempThreshold)

            pi = mcts.getActionProb(canonicalBoard, temp=temp)
            sym = self.game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            board, curPlayer = self.game.getNextState(board, curPlayer, action)

            r = self.game.getGameEnded(self.game.getCanonicalForm(board, curPlayer), 0)

            if r != 0:
                # board, probabilities, reward
                return [(x[0], x[2], r if (x[1] == curPlayer) else -r) for x in trainExamples]

    def executeEpisodes_thread(self, num, results, thread_i, pbar=None):
        for _ in range(num):
            mcts = MCTS(self.game, self.nnet, self.args)  # reset search tree
            results[thread_i].append(self.executeEpisode(mcts))

            if pbar is not None:
                pbar.update(1)


    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximum length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters + 1):
            # bookkeeping
            log.info(f'Starting Iter #{i} ...')
            # examples of the iteration
            if not self.skipFirstSelfPlay or i > 1:
                iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)

                if self.args['parallelSelfPlay']:
                    # Parallelize the self-play
                    num_workers = multiprocessing.cpu_count()
                    log.info(f"Starting selfplay with {num_workers} threads")

                    num_tot_episodes = self.args.numEps
                    episodes_per_worker = (num_tot_episodes // num_workers)
                    remaining_episodes = num_tot_episodes - (episodes_per_worker * num_workers)
                    pbar = tqdm(total=num_tot_episodes, desc="Self Play")

                    threads = [None for _ in range(num_workers)]
                    results = [[] for _ in range(num_workers)]

                    for j in range(num_workers):
                        threads[j] = threading.Thread(target=self.executeEpisodes_thread, args=(episodes_per_worker + (1 if j < remaining_episodes else 0), results, j, pbar))
                        threads[j].start()

                    for j in range(len(threads)):
                        threads[j].join()
                    pbar.close()

                    for result in results:
                        for ep in result:
                            iterationTrainExamples += ep
                else:
                    for _ in tqdm(range(self.args.numEps)):
                       mcts = MCTS(self.game, self.nnet, self.args)  # reset search tree
                       iterationTrainExamples += self.executeEpisode(mcts)



                # save the iteration examples to the history 
                self.trainExamplesHistory.append(iterationTrainExamples)

            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                log.warning(
                    f"Removing the oldest entry in trainExamples. len(trainExamplesHistory) = {len(self.trainExamplesHistory)}")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            self.saveTrainExamples(i - 1)
            log.info(f'Saving training examples (length={len(self.trainExamplesHistory)})')

            # shuffle examples before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.nnet.train(trainExamples)

            if self.args.pitVsRandom:
                self.pitVsRandom()

            pwins, draws, nwins = self.pitVsOld()
            
            if pwins + nwins == 0 or float(nwins) / (pwins + nwins) < self.args.updateThreshold:
                log.info('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                log.info('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')


    def pitVsOld_thread(self, num, reverse_players, results, thread_i, pbar):
        for _ in range(num):
            nmcts = MCTS(self.game, self.nnet, self.args)
            pmcts = MCTS(self.game, self.pnet, self.args)

            if not reverse_players:
                arena = Arena(lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                            lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                            self.game)
                            
                winner = arena.playGame()
            else:
                arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                              lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                              self.game)
                            
                winner = arena.playGame()
                winner = -1 * winner 
            
            results[thread_i][1 + winner] += 1
            pbar.update(1)

    def pitVsOld(self):
        log.info('PITTING AGAINST PREVIOUS VERSION')

        if self.args['parallelArena']:
            final_result = [0,0,0]
            
            for reverse in [False, True]:
                num_tot_episodes = self.args.arenaCompare // 2
                num_workers = min(num_tot_episodes, multiprocessing.cpu_count())
                episodes_per_worker = (num_tot_episodes // num_workers)
                remaining_episodes = num_tot_episodes - (episodes_per_worker * num_workers)
                pbar = tqdm(total=num_tot_episodes, desc=f"Arena.playgame [{reverse=}]")

                threads = [None for _ in range(num_workers)]
                results = [[0,0,0] for _ in range(num_workers)]

                for j in range(num_workers):
                    threads[j] = threading.Thread(target=self.pitVsOld_thread, 
                                                  args=(episodes_per_worker + (1 if j < remaining_episodes else 0), reverse, results, j, pbar))
                    threads[j].start()

                for j in range(len(threads)):
                    threads[j].join()
                    
                pbar.close()

                for result in results:
                    for i in range(len(final_result)):
                        final_result[i] += result[i]
                
            pwins, draws, nwins = final_result
        else:
            nmcts = MCTS(self.game, self.nnet, self.args)
            pmcts = MCTS(self.game, self.pnet, self.args) 
            arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), self.game)
            pwins, nwins, draws = arena.playGames(self.args.arenaCompare)

        
        log.info('NEW/OLD WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
        return pwins, draws, nwins

    def pitVsRandom_thread(self, num, reverse_players, results, thread_i, pbar):
        for _ in range(num):
            nmcts = MCTS(self.game, self.nnet, self.args)
            random_player = RandomPlayer(game=self.game)

            if not reverse_players:
                arena = Arena(lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                            lambda x: random_player.play(x),
                            self.game)
                            
                winner = arena.playGame()
            else:
                arena = Arena(lambda x: random_player.play(x),
                              lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                              self.game)
                            
                winner = arena.playGame()
                winner = -1 * winner 
            
            results[thread_i][1 + winner] += 1
            pbar.update(1)

    def pitVsRandom(self):
        log.info('PITTING AGAINST RANDOM')

        if self.args['parallelArena']:
            final_result = [0,0,0]
            
            for reverse in [False, True]:
                num_tot_episodes = self.args.arenaCompare // 2
                num_workers = min(num_tot_episodes, multiprocessing.cpu_count())
                episodes_per_worker = (num_tot_episodes // num_workers)
                remaining_episodes = num_tot_episodes - (episodes_per_worker * num_workers)
                pbar = tqdm(total=num_tot_episodes, desc=f"Arena.playgame [{reverse=}]")

                threads = [None for _ in range(num_workers)]
                results = [[0,0,0] for _ in range(num_workers)]

                for j in range(num_workers):
                    threads[j] = threading.Thread(target=self.pitVsRandom_thread, 
                                                  args=(episodes_per_worker + (1 if j < remaining_episodes else 0), reverse, results, j, pbar))
                    threads[j].start()

                for j in range(len(threads)):
                    threads[j].join()

                pbar.close()

                for result in results:
                    for i in range(len(final_result)):
                        final_result[i] += result[i]
                
            pwins, draws, nwins = final_result
        else:
            nmcts = MCTS(self.game, self.nnet, self.args)
            random_player = RandomPlayer(game=self.game)
            arena = Arena(lambda x: random_player.play(x),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), self.game)
            pwins, nwins, draws = arena.playGames(self.args.arenaCompare)
        
        log.info('AlphaZero/Random WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
        return pwins, draws, nwins

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile + ".examples"
        if not os.path.isfile(examplesFile):
            log.warning(f'File "{examplesFile}" with trainExamples not found!')
            r = input("Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            log.info("File with trainExamples found. Loading it...")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            log.info('Loading done!')

            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
