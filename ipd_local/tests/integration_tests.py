import ipd_local
from ipd_local.default_functions import *

import os
import random

import pandas as pd
from . import *


def test_rat():
    """
    Verifies all inputs of different edge cases return True.
    """
    assert silent([], [], 0) == True # tests function works for initial round
    silent([True], [True], sys.maxint) == True # tests function behaviour if round number and number of moves do not line up
    assert silent([True], [True], 1) == False # tests normal round
    assert silent([True, False, True, False], [True, True, True, True], 5) # tests nontrivial number of rounds


def test_silent():
    """
    Verifies all inputs of different edge cases return false.
    """
    assert silent([], [], 0) == False # tests function works for initial round
    silent([True], [True], sys.maxint) == False # tests function behaviour if round number and number of moves do not line up
    assert silent([True], [True], 1) == False # tests normal round
    assert silent([True, False, True, False], [True, True, True, True], 5) # tests nontrivial number of rounds
