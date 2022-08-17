#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The lecture materials for Lecture 1: Dataset Prototyping and Visualization
"""
import click
import torch
import torch.nn as nn
from torch.optim import Adam
from tqdm import trange

from cv4e_lecture13 import dataset, model, utils

log = None


def inference(cfg, dataloader, net, optimizer, criterion, update):
    '''
    Our actual training function.
    '''
    device = cfg.get('device')

    torch.set_grad_enabled(update)
    net.train() if update else net.eval()
    type_str = 'Train' if update else 'Val'

    loss, accuracy = 0.0, 0.0
    total = len(dataloader)

    prog = trange(total)
    for index, (data, labels) in enumerate(dataloader):
        data, labels = data.to(device), labels.to(device)

        prediction = net(data)
        gradient = criterion(prediction, labels)

        if update:
            optimizer.zero_grad()
            gradient.backward()
            optimizer.step()

        # log statistics
        loss += gradient.item()
        label_ = torch.argmax(prediction, dim=1)
        accuracy += torch.mean((label_ == labels).float()).item()

        prog.set_description(
            '[{:s}] Loss: {:.2f}; Acc: {:.2f}%'.format(
                type_str, loss / (index + 1), 100.0 * accuracy / (index + 1)
            )
        )
        prog.update(1)
    prog.close()

    loss /= total
    accuracy /= total

    return loss, accuracy


@click.command()
@click.option(
    '--config', help='Path to config file', default='configs/mnist_resnet18.yaml'
)
def lecture(config):
    """
    Main function for Lecture 1: Dataset Prototyping and Visualization
    """
    global log

    log = utils.init_logging()

    cfg = utils.init_config(config, log)

    # init random number generator seed (set at the start)
    utils.init_seed(cfg.get('seed', None))

    ################################################################################
    # Load MNIST
    train, test = dataset.load(cfg)

    net, epoch, best_loss = model.load(cfg)

    optimizer = Adam(
        net.parameters(),
        lr=cfg.get('learning_rate'),
        weight_decay=cfg.get('weight_decay'),
    )
    criterion = nn.CrossEntropyLoss()

    epochs = cfg.get('max_epochs')
    while epoch < epochs:
        log.info(f'Epoch {epoch}/{epochs}')

        loss_train, accuracy_train = inference(
            cfg, train, net, optimizer, criterion, update=True
        )
        loss_test, accuracy_test = inference(
            cfg, test, net, optimizer, criterion, update=False
        )

        # combine stats and save
        stats = {
            'loss_train': loss_train,
            'loss_val': loss_test,
            'accuracy_train': accuracy_train,
            'accuracy_test': accuracy_test,
        }

        best = loss_test < best_loss
        net.save(cfg, epoch, stats, best=best)
        if not best:
            log.warning('Stopping early')
            break

        best_loss = loss_test
        epoch += 1


if __name__ == '__main__':
    # Common boiler-plating needed to run the code from the command line as `python lecture.py` or `./lecture.py`
    # This if condition will be False if the file is imported
    lecture()
