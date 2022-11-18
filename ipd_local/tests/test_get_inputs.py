import ipd_local
from ipd_local.get_inputs import *
from ipd_local.default_functions import rat, titFortat

import os
import random

import pandas as pd
from . import *

def test_get_spreadsheet_data():
    contents = pd.DataFrame(
        [["65", "41", "a"], ["66", "42", "b"], ["67", "43", "c"]],
        columns=["Decimal", "Char", "Hex"]
    )
    set_temp_sheet("Test get_spreadsheet_data()", contents, tab_name="ASCII")
    df = get_spreadsheet_data("Test get_spreadsheet_data()", "ASCII")
    assert df == [["Decimal", "Char", "Hex"], ["65", "41", "a"], ["66", "42", "b"], ["67", "43", "c"]]

def test_get_pastebin():
    assert get_pastebin("invalid link") == None
    assert get_pastebin("pastebin.com/somethin") == None
    assert get_pastebin("https://xkcd.com/327/") == None
    assert get_pastebin("https://pastebin.com/as76d7ww9") == None
    assert get_pastebin("https://pastebin.com/(((())))") == None
    assert get_pastebin("https://pastebin.com/raw/") == None
    assert get_pastebin("https://pastebin.com/raw/a|") == None
    assert get_pastebin("https://pastebin.com/J1XqZQ25") == "Testing 123"
    assert get_pastebin("https://pastebin.com/raw/J1XqZQ25") == "Testing 123"

    assert os.path.exists("./cache")
    assert os.path.exists("./cache/J1XqZQ25")

    # asking to read from cache should return the contents of the corresponding cached file
    f = open("./cache/J1XqZQ25", "w")
    f.write("test")
    f.close()
    assert get_pastebin("https://pastebin.com/raw/J1XqZQ25", cache=True) == "test"

def test_check_functions_io():
    def verybad():
        pass
    def invalid_code(mymoves, theirmoves, r):
        return mymoves[1000]
    def good(mymoves, theirmoves, r):
        return random.choice([True, False])

    assert (
        check_functions_io([verybad, invalid_code, good, rat, titFortat])
        ==
        ([good, rat, titFortat], [verybad, invalid_code])
    )

def test_get_and_load_functions():
    contents = [
        [None, "Student", "Regular", "Noise" ],
        [None, "Quackary", "https://pastebin.com/gue8xdjr", "https://pastebin.com/EevQk4ph" ],
        [None, "huxely. ", "https://pastebin.com/bjthjeT6", "https://pastebin.com/bjthjeT6" ],
        [None, "Jackary!", "https://pastebin.com/0fqA2Wtd", "https://pastebin.com/0fqA2Wtd" ],        
    ]
    functions = get_and_load_functions(contents, noise=False)
    assert len(functions) == 5
    assert [callable(f) for f in functions] == [True]*5

    functions = get_and_load_functions(contents, noise=True)
    assert len(functions) == 4
    assert [callable(f) for f in functions] == [True]*4

    nastier_contents = [
        [None, "Student",  None, "Regular", None, "Noise" ],
        [None, "Quackary", None, "https://pastebin.com/gue8xdjr", None,  "https://pastebin.com/EevQk4ph" ],
        [None, "huxely. ", None, "https://pastebin.com/bjthjeT6", None, "https://pastebin.com/bjthjeT6" ],
        [None, "Jackary!", None, "https://pastebin.com/0fqA2Wtd", None, "https://pastebin.com/0fqA2Wtd" ],        
    ]

    functions = get_and_load_functions(nastier_contents, name_col=1, regular_col=3, noise_col=5, noise=False)
    assert len(functions) == 5
    assert [callable(f) for f in functions] == [True]*5

    functions = get_and_load_functions(nastier_contents, name_col=1, regular_col=3, noise_col=5, noise=True)
    assert len(functions) == 4
    assert [callable(f) for f in functions] == [True]*4

def test_inputs_subsystem():
    contents = [
        ['', "Student", "Regular", "Noise" ],
        ['', "Quackary", "https://pastebin.com/gue8xdjr", "https://pastebin.com/EevQk4ph" ],
        ['', "huxely. ", "https://pastebin.com/bjthjeT6", "https://pastebin.com/bjthjeT6" ],
        ['', "Jackary!", "https://pastebin.com/0fqA2Wtd", "https://pastebin.com/0fqA2Wtd" ],        
    ]
    set_temp_sheet(
        "Test input subsystem",
        pd.DataFrame(contents[1:], columns=contents[0]),
        tab_name="Form Responses"
    )
    fetched = get_spreadsheet_data("Test input subsystem", "Form Responses")

    assert fetched[:4] == contents
    
    functions = get_and_load_functions(fetched, noise=False)
    assert len(functions) == 5
    assert [callable(f) for f in functions] == [True]*5
    assert (
        [f.__name__ for f in functions]
        ==
        ["rat", "titFortat", "titForTwotats", "nukeFortat", "nukeForTwotats"]
    )
