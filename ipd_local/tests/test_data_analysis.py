from ipd_local.data_analysis import *
from ipd_local.default_functions import *
from ipd_local.output_locations import *
from ipd_local.simulation import run_simulation
import pytest

from math import nan
import os
import random
import sys

import pandas as pd
from . import *

def test_get_pairwise() -> None:
    assert str(get_pairwise().to_dict()) == str({'rat': {'silent': [531.0, 0.0], 'titFortat': [113.88, 52.14], 'rat': float("nan")}, 'silent': {'silent': float("nan"), 'titFortat': [265.8, 318.36], 'rat': [0.0, 531.0]}, 'titFortat': {'silent': [318.36, 265.8], 'titFortat': float("nan"), 'rat': [52.14, 113.88]}})
    
def test_get_ranking() -> None:
    assert get_ranking().to_dict() == {'Strategy': {0: 'silent', 1: 'titFortat', 2: 'rat'}, 'Total Points': {0: 849.36, 1: 379.68, 2: 52.14}, 'Average Points': {0: 424.68, 1: 189.84, 2: 26.07}}

def test_get_summary() -> None:
    assert get_summary().to_dict() == {0: {'Noise': True, 'Noise Level (if applicable)': 0.1, 'Noise Games Played Before Averaging (if applicable)': 50, 'Number of Rounds': 59, 'Points when both rat': 1, 'Points for winner when different': 9, 'Points for loser when different': 0, 'Points when both cooperate': 5, 'Debug mode (fixed random seed - should be off)': True}}

def test_update_sheet() -> None:
    pass#update_sheet()
