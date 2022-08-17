# -*- coding: utf-8 -*-
'''
    Various utility functions used (possibly) across scripts.

    2022 Benjamin Kellenberger
'''

import logging
import random
from logging.handlers import TimedRotatingFileHandler

import torch
import yaml
from torch.backends import cudnn

DAYS = 21


def init_logging():
    """
    Setup Python's built in logging functionality with on-disk logging, and prettier logging with Rich
    """
    # Import Rich
    import rich
    from rich.logging import RichHandler
    from rich.style import Style
    from rich.theme import Theme

    name = 'lecture'

    # Setup placeholder for logging handlers
    handlers = []

    # Configuration arguments for console, handlers, and logging
    console_kwargs = {
        'theme': Theme(
            {
                'logging.keyword': Style(bold=True, color='yellow'),
                'logging.level.notset': Style(dim=True),
                'logging.level.debug': Style(color='cyan'),
                'logging.level.info': Style(color='green'),
                'logging.level.warning': Style(color='yellow'),
                'logging.level.error': Style(color='red', bold=True),
                'logging.level.critical': Style(color='red', bold=True, reverse=True),
                'log.time': Style(color='white'),
            }
        )
    }
    handler_kwargs = {
        'rich_tracebacks': True,
        'tracebacks_show_locals': True,
    }
    logging_kwargs = {
        'level': logging.INFO,
        'format': '[%(name)s] %(message)s',
        'datefmt': '[%X]',
    }

    # Add file-baesd log handler
    handlers.append(
        TimedRotatingFileHandler(
            filename=f'{name}.log',
            when='midnight',
            backupCount=DAYS,
        ),
    )

    # Add rich (fancy logging) log handler
    rich.reconfigure(**console_kwargs)
    handlers.append(RichHandler(**handler_kwargs))

    # Setup global logger with the handlers and set the default level to INFO
    logging.basicConfig(handlers=handlers, **logging_kwargs)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log = logging.getLogger(name)

    return log


def init_seed(seed):
    if seed is not None:
        random.seed(seed)
        # numpy.random.seed(seed)       # we don't use NumPy in this code, but you would want to set its random number generator seed, too
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        cudnn.benchmark = True
        cudnn.deterministic = True


def init_config(config, log):
    # load config
    log.info(f'Using config "{config}"')
    cfg = yaml.safe_load(open(config, 'r'))

    cfg['log'] = log

    # check if GPU is available
    device = cfg.get('device')
    if device not in ['cpu']:
        if torch.cuda.is_available():
            cfg['device'] = 'cuda'
        elif torch.backends.mps.is_available():
            cfg['device'] = 'mps'
        else:
            log.warning(
                f'WARNING: device set to "{device}" but not available; falling back to CPU...'
            )
            cfg['device'] = 'cpu'

    device = cfg.get('device')
    log.info(f'Using device "{device}"')

    return cfg
