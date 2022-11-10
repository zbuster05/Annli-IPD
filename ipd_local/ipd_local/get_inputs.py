import gspread
import requests
from tqdm import tqdm
import types

from loguru import logger

from .game_specs import *
from .default_functions import *
from .simulation import *
from .output_locations import *

# gets all game inputs
# outputs list of functions, number of rounds, and blindness level
# blindness is how much noise each player has, which we assume to be symmetric
def get_game_inputs():

    # retrieve latest list of submissions from google sheets
    # link to the sheet: https://docs.google.com/spreadsheets/d/1YZZQFShRcYO4p3pCqBY5LPZf4pO9zfmt6b6BNItVb3g/edit?usp=sharing
    # returns all data on the spreadsheet
    def get_spreadsheet_data():
        print("Retrieving spreadsheet data...")
        service_account = gspread.service_account(filename="service_account.json")
        spreadsheet = service_account.open("IPD Player Strategies")
        worksheet = spreadsheet.worksheet("Form Responses 1")
        print("Retrieved spreadsheet data.")
        return worksheet.get_all_values()

    # gets spreadsheet data
    spreadsheet_data = get_spreadsheet_data()


    # returns an array of dictionary objects, each being a student
    # student format: {name, link, function_names, code}
    #                 where function_names is a list
    def get_students_and_code():

        data = spreadsheet_data
        students = []

        print("Retrieving student code...")

        # iterate through all submissions (every student)
        for i in tqdm(range(1, len(data))):
            student = {}
            student["student_name"] = data[i][1]

            # accessing and parsing code from pastebin
            index = 2 # index of column for pastebin links in the spreadsheet. index of 2 is for the no noise data
            if NOISE:
                index = 3 # column index 3 (which is column D) contains links to submissions for tournament with noise
            link = data[i][index]
            if not "https://pastebin.com/" in link: # checks that valid pastebin link is submitted
                logger.error(f"Could not parse {data[i][1]}'s pastebin link")
                continue
            link = "https://pastebin.com/raw/" + link.split("pastebin.com/")[-1] # link to raw text on pastebin
            code = requests.get(link).text # retrieves the raw text from pastebin

            # getting function names
            lines = code.split('\n') # splits code into lines
            function_names = []
            for line in lines:
                if len(line)>4 and line[0:4]=="def": # find the beginning of a function
                    try:
                        function_names.append(line.split()[1].split("(")[0]) # splits at space by default
                    except Exception as e:
                        logger.error(f"Could not parse {student['student_name']}'s code: {str(e)}")

            student["link"] = link
            student["function_names"] = function_names
            student["code"] = code

            # print("---", student["student_name"], "'s code retrieved.")
            students.append(student)

        print("Retrieved all student code.")
        return students

    # gets all students
    all_valid_students = get_students_and_code()


    # load all the functions that will actually be playing
    def load_functions():

        students = all_valid_students
        functions = []
        bad_kids = []

        # iterate through all students (that are still valid)
        for i in tqdm(range(len(students))):
            # print("Loading student's functions:", students[i]["student_name"])
            try:
                exec(students[i]["code"]) # execute the student's code
                for function_name in students[i]["function_names"]:
                    functions.append(eval(function_name)) # append the actual function object to the student's list of functions
            except Exception as e:
                logger.error(f"Failed to execute {students[i]['student_name']}'s code: {str(e)}")
                # add student to list of students whose functions did not compile
                bad_kids.append(students[i]["student_name"])

        # get all the functions that have been loaded without issue
        loaded_functions = [f for f in locals().values() if type(f) == types.FunctionType]

        # filter for functions that pass basic input/output check
        good, bad = test_io_functions(loaded_functions)
        loaded_functions = good

        print("Removed", len(bad), "functions for bad IO.")
        print("Loaded", len(loaded_functions), " good functions.")
        return loaded_functions


    # final filter of functions that don't work properly (throw errors during actual simulation)
    # these functions are stored in blacklist.txt
    def filter_blacklist(all_functions):

        # reloads blacklist using latest functions if user wants to reload blacklist (recommended)
        if RELOAD_BLACKLIST:
            print("Reloading blacklisted functions...")
            if NOISE:
                blindness = [NOISE_LEVEL, NOISE_LEVEL]
            else:
                blindness = [0,0]
            if INCLUDE_DEFAULTS:
                reload_blacklist(all_default_functions + all_functions, ROUNDS, blindness) # reloads blacklist. this function is defined in simulation.py because it is essentially running the simulation
            else:
                reload_blacklist(all_functions, ROUNDS, blindness)
            print("Reloaded blacklisted functions.")

        # removes blacklisted functions from list of functions
        functions_dict = {}
        for func in all_functions: # converts function list to dictionary for easier indexing
            functions_dict[func.__name__] = func
        blacklist = []
        with open(BLACKLIST, "r") as f:
            blacklist = f.readlines() # reads all functions that need to be blacklisted
            for func in blacklist:
                func = func[:-1]
                del(functions_dict[func]) # removes function from list of valid functions
        print("Removed", len(blacklist), "functions from blacklist.")

        return list(functions_dict.values())


    # tests function input and outputs
    # input must be three arguments: your past moves, opponent's past moves, and round number
    def test_io_functions(functions):
        good_functions = []
        bad_functions = []

        # iterates through each function
        for function in functions:
            try:
                with suppress_stdout(): # ignore all printed statements from these functions
                    output = function([True]*10,[False]*10,10) # run the function
                    if output==None:
                        raise Exception("function returned None (make sure you are returning something)")
                    if output:
                        pass # ensure output is boolean value (or int 0 or 1)
                    good_functions.append(function)
            except Exception as e:
                logger.error(f"Testing I/O of {function.__name__} failed: {str(e)}")
                bad_functions.append(function)
        
        return good_functions, bad_functions


    # returns list of function objects that will be participating in tournament
    def get_functions():
        all_functions = load_functions() # load all functions that compile and pass input/output
        good_functions = filter_blacklist(all_functions) # filter away blacklisted functions
        return good_functions


    # config for running game
    # returns list of functions (strats), number of rounds, and blindness
    strats = get_functions()
    if INCLUDE_DEFAULTS: # include default functions if user desires
        strats = all_default_functions + strats
    rounds = ROUNDS
    blindness = []
    if NOISE:
        blindness = [NOISE_LEVEL, NOISE_LEVEL]
    else:
        blindness = [0,0]
    return strats, rounds, blindness
