'''
    Model implementation.
    We'll be using a "simple" ResNet-18 for image classification here.

    2022 Benjamin Kellenberger
'''
import torch
from torchvision import datasets
from torchvision.transforms import Compose, Resize, ToTensor
from os.path import abspath


def load(cfg):
    """
    Load the MNIST dataset from PyTorch (download if needed) and return a DataLoader

    MNIST is a sample dataset for machine learning, each image is 28-pixels high and 28-pixels wide (1 color channel)
    """
    root = abspath('datasets')

    train = torch.utils.data.DataLoader(
        datasets.MNIST(
            root, 
            train=True, 
            transform=Compose([             
                Resize((cfg['image_size'])), 
                ToTensor()                   
            ]),
            download=True
        ), 
        batch_size=cfg.get('batch_size'), 
        shuffle=True, 
        num_workers=cfg.get('num_workers')
    )
    
    test = torch.utils.data.DataLoader(
        datasets.MNIST(
            root, 
            train=False, 
            transform=Compose([             
                Resize((cfg['image_size'])), 
                ToTensor()                   
            ]),
            download=True
        ), 
        batch_size=cfg.get('batch_size'), 
        shuffle=False, 
        num_workers=cfg.get('num_workers')
    )

    return train, test
