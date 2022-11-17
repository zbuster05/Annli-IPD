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

def test_get_pairwise():
    assert str(get_pairwise().to_dict()) == str({'rat': {'silent': [531.0, 0.0], 'titFortat': [113.88, 52.14], 'rat': float("nan")}, 'silent': {'silent': float("nan"), 'titFortat': [265.8, 318.36], 'rat': [0.0, 531.0]}, 'titFortat': {'silent': [318.36, 265.8], 'titFortat': float("nan"), 'rat': [52.14, 113.88]}})
    

