'''
    Model implementation.
    We'll be using a "simple" ResNet-18 for image classification here.

    2022 Benjamin Kellenberger
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import glob
import os
from os.path import split, splitext, exists


class SmallModel(nn.Module):

    @classmethod
    def load(cls, cfg):
        log = cfg.get('log')

        net = cls()

        epoch = 0
        best_loss = np.inf

        output = cfg.get('output')

        filepaths = sorted(glob.glob(f'{output}/*.pt'))

        if len(filepaths) > 1:
            filepaths = [
                filepath 
                for filepath in filepaths 
                if 'best.pt' not in filepath
            ]

        if len(filepaths):
            filepath = filepaths[-1]

            log.info(f'Resuming from {filepath}')

            state = torch.load(open(filepath, 'rb'), map_location='cpu')
            net.load_state_dict(state['model'])

            filename = split(filepath)[1]
            try:
                epoch = int(splitext(filename)[0])
            except ValueError:
                pass
                
            filepath = f'{output}/best.pt'
            if exists(filepath):
                state = torch.load(open(filepath, 'rb'), map_location='cpu')
                best_loss = state['loss_val']
        else:
            log.info('Starting new network model')

        device = cfg.get('device')
        net.to(device)

        return net, epoch, best_loss

    def __init__(self):
        super(SmallModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 5)
        self.conv2 = nn.Conv2d(16, 32, 5)
        self.fc1 = nn.Linear(32 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = torch.flatten(x, 1) 
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def save(self, cfg, epoch, stats, best=False):
        output = cfg.get('output')

        os.makedirs(output, exist_ok=True)

        stats['model'] = self.state_dict()

        torch.save(stats, open(f'{output}/{epoch:04d}.pt', 'wb'))

        if best:
            torch.save(stats, open(f'{output}/best.pt', 'wb'))


def load(cfg):
    return SmallModel.load(cfg)
