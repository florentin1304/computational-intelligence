import os
import sys
import time

import numpy as np
from tqdm import tqdm

sys.path.append('../../')
from utils import *
from NeuralNet import NeuralNet

import torch
import torch.optim as optim

from .QuixoResNet import QuixoResNet as onnet


args = dotdict({
    'lr': 0.003,
    'epochs': 40,
    'batch_size': 128,
    'cuda': torch.cuda.is_available(),
    'num_resBlocks': 6,
    'num_hidden': 128
})



class QuixoNetWrapper(NeuralNet):
    """
    The neural network does not consider the current player, 
    and instead only deals with the canonical form of the board.
    """

    def __init__(self, game):
        self.nnet = onnet(game, args)

        self.game = game
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        
        if args.cuda:
            self.nnet.cuda()

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """
        optimizer = optim.Adam(self.nnet.parameters())

        for epoch in range(args.epochs):
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count = int(len(examples) / args.batch_size)
            sample_ids_shuffled = np.random.shuffle( list(range(len(examples))) )

            t = tqdm(range(batch_count), desc=f'EPOCH ::: {str(epoch + 1)}')
            for batch_id in t:
                sample_ids = sample_ids_shuffled[ batch_id*args.batch_size : min((batch_id+1)*args.batch_size, len(examples))]
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))

                boards = [self.game.getEncodedBoard(b) for b in boards] 
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                if args.cuda:
                    boards, target_pis, target_vs = boards.contiguous().cuda(), target_pis.contiguous().cuda(), target_vs.contiguous().cuda()

                # compute output
                out_pi, out_v = self.nnet(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                # record loss
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = self.game.getEncodedBoard(board)
        board = torch.FloatTensor(board.astype(np.float64))
        board = board.unsqueeze(0)

        if args.cuda: 
            board = board.contiguous().cuda()

        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(board)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise ("No model in path {}".format(filepath))
        map_location = None if args.cuda else 'cpu'
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])
