import ipd_local
from ipd_local.default_functions import *
import pytest

import os
import random
import sys

import pandas as pd
from . import *


def test_rat():
    """
    Verifies all inputs of different edge cases return True.
    """
    assert rat([], [], 0) == True # tests function works for initial round
    with pytest.raises(Exception):
        rat([True], [True], sys.maxsize) == True # tests function behaviour if round number and number of moves do not line up
    assert rat([True], [True], 1) == True # tests normal round
    assert rat([True, False, True, False], [True, True, True, True], 5)  == True # tests nontrivial number of rounds


def test_silent():
    """
    Verifies all inputs of different edge cases return false.
    """
    assert silent([], [], 0) == False # tests function works for initial round
    with pytest.raises(Exception):
        silent([True], [True], sys.maxsize) == False # tests function behaviour if round number and number of moves do not line up
    assert silent([True], [True], 1) == False # tests normal round
    assert silent([True, False, True, False], [True, True, True, True], 5) == False # tests nontrivial number of rounds
