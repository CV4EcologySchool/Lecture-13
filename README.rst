======================================================================
Lecture 13: Serving, Hosting, and Deploying Models and Quality Control
======================================================================

|Tests| |Wheel| |Docker| |ReadTheDocs| |Huggingface|

.. contents:: Quick Links
    :backlinks: none

.. sectnum::

Introduction
------------

.. image:: https://github.com/CV4EcologySchool/Lecture-13/raw/main/intro.jpg
    :target: https://drive.google.com/drive/u/0/folders/1zozC7vTKU0KMnAcMPt_vR8m7QBPO2UYK
    :alt: "Lecture 13: Serving, Hosting, and Deploying Models and Quality Control"

This repository holds the lecture materials for the `Computer Vision for Ecology workshop at CalTech <https://cv4ecology.caltech.edu>`_.  The goal of this lecture is to describe how to deploy a machine learning model for others to use, and how best to perform quality control.

The associated slides for this lecture can be viewed by clicking on the image above.

How to Install
--------------

You need to first install Anaconda on your machine.  Below are the instructions on how to install Anaconda on an Apple macOS machine, but it is possible to install on a Windows and Linux machine as well.  Consult the `official Anaconda page <https://www.anaconda.com>`_ to download and install on other systems.  For Windows computers, it is highly recommended that you intall the `Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install>`_.

.. code:: bash

   # Install Homebrew
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Anaconda and expose conda to the terminal
   brew install anaconda
   export PATH="/opt/homebrew/anaconda3/bin:$PATH"
   conda init zsh
   conda update conda

Once Anaconda is installed, you will need an environment and the following packages installed

.. code:: bash

   # Create Environment
   conda create --name cv4e
   conda activate cv4e

   # Install Python dependencies
   conda install pip

   conda install -r requirements.txt
   conda install pytorch torchvision -c pytorch-nightly

How to Run
----------

The lecture materials will run as a single executable.  The MNIST dataset must be downloaded from the internet for this script to run correctly, so Internet access is required at first to download the files once.  It is recommended to use `ipython` and to copy sections of code into and inspecting the

.. code:: bash

   # Run the training script
   cd cv4e_lecture13/
   python train.py

   # Run the live demo
   python app.py

Docker
------

The application can also be built into a Docker image and hosted on Docker Hub.

.. code:: bash

    docker build . -t bluemellophone/cv4e:lecture13
    docker push bluemellophone/cv4e:lecture13

To run:

.. code:: bash

    docker run \
       -it \
       --rm \
       -p 7860:7860 \
       --name cv4e \
       bluemellophone/cv4e:lecture13

Unit Tests
----------

You can run the automated tests in the `tests/` folder by running `pytest`.  This will give an output of which tests have failed.  You may also get a coverage percentage by running `coverage html` and loading the `coverage/html/index.html` file in your browser.
pytest

Building Documentation
----------------------

There is Sphinx documentation in the `docs/` folder, which can be built with the code below:

.. code:: bash

    cd docs/
    sphinx-build -M html . build/

Logging
-------

The script uses Python's built-in logging functionality called `logging`.  All print functions are replaced with `log.info` within this script, which sends the output to two places: 1) the terminal window, 2) the file `lecture.log`.  Get into the habit of writing text logs and keeping date-specific versions for comparison and debugging.

Code Formatting
---------------

It's recommended that you use ``pre-commit`` to ensure linting procedures are run
on any code you write. (See also `pre-commit.com <https://pre-commit.com/>`_)

Reference `pre-commit's installation instructions <https://pre-commit.com/#install>`_ for software installation on your OS/platform. After you have the software installed, run ``pre-commit install`` on the command line. Now every time you commit to this project's code base the linter procedures will automatically run over the changed files.  To run pre-commit on files preemtively from the command line use:

.. code:: bash

    git add .
    pre-commit run

    # or

    pre-commit run --all-files

The code base has been formatted by Brunette, which is a fork and more configurable version of Black (https://black.readthedocs.io/en/stable/).  Furthermore, try to conform to PEP8.  You should set up your preferred editor to use flake8 as its Python linter, but pre-commit will ensure compliance before a git commit is completed.  This will use the flake8 configuration within ``setup.cfg``, which ignores several errors and stylistic considerations.  See the ``setup.cfg`` file for a full and accurate listing of stylistic codes to ignore.

See Also
--------

- https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
- https://pytorch.org/vision/stable/models.html#quantized-models
- https://dvc.org/blog/scipy-2020-dvc-poster
- https://godatadriven.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/
- https://neptune.ai/blog/machine-learning-model-management
- https://neptune.ai/blog/mlops
- https://github.com/readthedocs-examples/example-sphinx-basic/
- https://github.com/CV4EcologySchool/ct_classifier
- https://docs.python.org/3/distutils/setupscript.html

Troubleshooting
---------------
If you experience issues running the gradio app on macOS, try the following:

.. code:: bash

    brew install openssl

.. |Tests| image:: https://github.com/CV4EcologySchool/Lecture-13/actions/workflows/testing.yml/badge.svg?branch=main
    :target: https://github.com/CV4EcologySchool/Lecture-13/actions/workflows/testing.yml
    :alt: GitHub CI

.. |Wheel| image:: https://github.com/CV4EcologySchool/Lecture-13/actions/workflows/python-publish.yml/badge.svg
    :target: https://github.com/CV4EcologySchool/Lecture-13/actions/workflows/python-publish.yml
    :alt: Python Wheel

.. |Docker| image:: https://img.shields.io/docker/image-size/bluemellophone/cv4e/lecture13
    :target: https://hub.docker.com/r/bluemellophone/cv4e
    :alt: Docker

.. |ReadTheDocs| image:: https://readthedocs.org/projects/cv4ecology-lecture-13/badge/?version=latest
    :target: https://cv4ecology-lecture-13.readthedocs.io/en/latest/?badge=latest
    :alt: ReadTheDocs

.. |Huggingface| image:: https://img.shields.io/badge/HuggingFace-Running-yellow
    :target: https://huggingface.co/spaces/CV4EcologySchool/Lecture-13
    :alt: Huggingface
