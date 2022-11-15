import gspread
import requests
from tqdm import tqdm

from typing import Optional, List, Callable, NewType, Tuple

from loguru import logger

from .game_specs import *
from .default_functions import *
from .simulation import *
from .output_locations import *
import os
import urllib

Strategy = NewType("Strategy", Callable[[List[bool], List[bool]], int])

def get_spreadsheet_data(sheet: str, tab: str) -> List[List[str]]:
    """
    Retrieve latest list of submissions from Google Sheet.
    Link: https://docs.google.com/spreadsheets/d/1YZZQFShRcYO4p3pCqBY5LPZf4pO9zfmt6b6BNItVb3g/edit?usp=sharing

    Arguments:
    - `sheet`: the name of the spreadsheet to query.
    - `tab`: the tab of the spreadsheet the data is in.
    
    Returns: list of lists containing spreadsheet data in column-row format.
    """
    print("Retrieving spreadsheet data...")
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open(sheet)
    worksheet = spreadsheet.worksheet(tab)
    print("Retrieved spreadsheet data.")
    return worksheet.get_all_values()

def get_pastebin(link: str, cache: bool = False) -> Optional[str]:
    """
    Downloads content of pastebin link and returns it.
    Caches content for optional faster future lookups (assuming code has not changed).

    Arguments:
    - `link`: the pastebin link to query
    - 'cache`: whether or not to pull from a cached copy (if applicable).

    Returns: the contents of the pastebin as a string.
    """
    url = urllib.parse.urlparse(link)
    if url.netloc != "pastebin.com":
        return None
    ident = parse.parse("/raw/{}", url.path)
    if ident == None:
        ident = parse.parse("/{}", url.path)
        link = f"https://pastebin/raw/{ident}"
    if len(ident) != 8 or not ident.isalnum(): # pastebin IDs are always 8 alphanumeric chars
        return None
    
    if not os.path.exists("./cache"):
        os.mkdir("./cache")
    if cache:
        if os.path.exists(f"./cache/{ident}"):
            return open(f"./cache/{ident}").read()

    code = requests.get(link)
    if not cache: # no need to re-write cache's contents to itself
        open(f"./cache/{ident}").write(code)
    return code

def get_and_load_functions(data: List[List[str]]) -> List[Strategy]:
    """
    Downloads, loads, and filters all of the python code in the provided pastebin links.
    Filtering of functions is done via `test_io_functions`
    """
    print("Retrieving student code...")

    # iterate through all submissions (every student)
    for i in tqdm(range(1, len(data))):
        link = data[i][NOISE_STRAT_COL if NOISE else REGULAR_STRAT_COL]

        if not (code := get_pastebin(link)):
            logger.error(f"Could not parse pastebin link for {data[i][STUDENT_NAME_COL]}!")
            continue

        for i in tqdm(range(len(students))):
            try:
                exec(students[i]["code"]) # execute the student's code
            except Exception as e:
                logger.error(f"Failed to execute code: {str(e)}")

        # get all the functions that have been loaded without issue
        loaded_functions = [f for f in locals().values() if callable(f)]

    # filter for functions that pass basic input/output check
    good, bad = test_io_functions(loaded_functions)
    loaded_functions = good

    print("Removed", len(bad), "functions for bad IO.")
    print("Loaded", len(loaded_functions), " good functions.")
    return loaded_functions

def test_io_functions(functions: List[Strategy]) -> Tuple[List[Strategy], List[Strategy]]:
    """
    Tests a list of functions on sample inputs and outputs to see if they work.
    Functions must take three arguments (their moves, opponent's moves, round number) and return a boolean.
    
    Returns tuple of the good and bad functions (in that order).
    """
    good_functions = []
    bad_functions = []

    for function in functions:
        try:
            with suppress_stdout(): # ignore all printed statements from these functions
                output = function([True]*10,[False]*10,10) # run the function
                if not isinstance(output, bool):
                    continue
                good_functions.append(function)
        except Exception as e:
            logger.error(f"Testing I/O of {function.__name__} failed: {str(e)}")
            bad_functions.append(function)

    return good_functions, bad_functions
