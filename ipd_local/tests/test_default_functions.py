import ipd_local
from ipd_local.default_functions import *
import pytest

import os
import random
import sys

import pandas as pd
from . import *


def test_rat() -> None:
    """
    Verifies all inputs of different edge cases return True.
    """
    assert rat([], [], 0) == True # tests function works for initial round
    with pytest.raises(Exception):
        rat([True], [True], sys.maxsize) == True # tests function behaviour if round number and number of moves do not line up
    assert rat([True], [True], 1) == True # tests normal round
    assert rat([True, False, True, False], [True, True, True, True], 4)  == True # tests nontrivial number of rounds


def test_silent() -> None:
    """
    Verifies all inputs of different edge cases return false.
    """
    assert silent([], [], 0) == False # tests function works for initial round
    with pytest.raises(Exception):
        silent([True], [True], sys.maxsize) == False # tests function behaviour if round number and number of moves do not line up
    assert silent([True], [True], 1) == False # tests normal round
    assert silent([True, False, True, False], [True, True, True, True], 4) == False # tests nontrivial number of rounds

def test_rand() -> None:
    """
    Verifies random works to expected distribution and also returns bool on edge cases
    """
    assert round([rand([True * x], [False * x], x) for x in range(1000)].count(True)/1000, 1) == 0.5 # tests if matches distribution up to length/round 1000, also tests 0th edge case

def test_kindaRandom() -> None:
    assert round([kindaRandom([True * x], [False * x], x) for x in range(1000)].count(True)/1000, 1) == 0.9 # tests if matches distribution up to length/round 1000, also tests 0th edge case

def test_titFortat() -> None:
    assert titFortat([], [], 0) == False # tests 0th case
    assert titFortat([False], [True], 1) == True # tests basic case
    assert titFortat([False*100], [False * 99, True], 100) == True # tests more complicated case

def test_titForTwotats() -> None:
    pass
