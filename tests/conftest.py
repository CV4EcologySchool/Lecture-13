# -*- coding: utf-8 -*-
import logging
import pytest

log = logging.getLogger('pytest.conftest')  # pylint: disable=invalid-name


@pytest.fixture()
def config():
    return 'cv4e_lecture13/configs/mnist_resnet18.yaml'


@pytest.fixture()
def cfg(config):
    from cv4e_lecture13 import utils
    log = utils.init_logging()
    cfg = utils.init_config(config, log)

    cfg['output'] = 'cv4e_lecture13/%s' % (cfg['output'], )

    return cfg


@pytest.fixture()
def device(cfg):
    device = cfg.get('device')

    return device


@pytest.fixture()
def net(cfg):
    from cv4e_lecture13 import model
    net, _, _ = model.load(cfg)
    net.eval()

    return net
