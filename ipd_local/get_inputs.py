import gspread
import requests
from tqdm import tqdm
import types

from game_specs import *
from default_functions import *
from simulation import *
from output_locations import *


# retrieve latest list of submissions from google sheets
# link to the sheet: https://docs.google.com/spreadsheets/d/1YZZQFShRcYO4p3pCqBY5LPZf4pO9zfmt6b6BNItVb3g/edit?usp=sharing
def get_spreadsheet_data():
    print("Retrieving spreadsheet data...")
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open("IPD Player Strategies")
    worksheet = spreadsheet.worksheet("Form Responses 1")
    print("Retrieved spreadsheet data.")
    return worksheet.get_all_values()


# returns an array of dictionary objects, each being a student
# student format: {name, link, function_names, code}
#                 where function_names is a list
def get_students_and_code():

    data = get_spreadsheet_data()
    students = []

    print("Retrieving student code...")
    
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("---\nPROBLEMS!!!\n---\n***\n---\n\n")
    bad_submission = []
    bad_parse = []

    for i in tqdm(range(1, len(data))):
        student = {}
        student["student_name"] = data[i][1]

        # accessing and parsing code from pastebin
        index = 2
        if NOISE:
            index = 3
        link = data[i][index]
        if not "https://pastebin.com/" in link:
            bad_submission.append(data[i][1])
            # with open(PROBLEMS_LOG_LOCATION, "a") as f:
            #     warning = data[i][1] + " did not submit a valid pastebin link for this tournament.\n"
            #     f.write(warning)            
            # print(data[i][1], " did not submit a pastebin link for this tournament.") # handles incorrect form filling out
            continue
        link = "https://pastebin.com/raw/" + link.split("pastebin.com/")[-1] # link to raw text on pastebin
        code = requests.get(link).text # retrieves the text

        # getting function names
        lines=code.split('\n')
        function_names = []
        for line in lines:
            if len(line)>4 and line[0:4]=="def":
                try:
                    function_names.append(line.split()[1].split("(")[0]) # splits at space by default
                except Exception as e:
                    code_issue = student["student_name"] + " could not parse. Error: " + e
                    bad_parse.append(code_issue)
                    # print(student["student_name"], "ERROR: ", e)

        student["link"] = link
        student["function_names"] = function_names
        student["code"] = code
        
        # print("---", student["student_name"], "'s code retrieved.")
        students.append(student)

    # log problems
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("BAD SUBMISSION\nThe following students did not submit a valid pastebin link:\n\n")
        for name in bad_submission:
            s = name+"\n"
            f.write(s)
        f.write("\n---\n***\n---\n\nCANNOT PARSE\nThe following students wrote code that could not be parsed into functions:\n\n")
        for issue in bad_parse:
            s = issue+"\n"
            f.write(s)
        f.write("\n---\n***\n---\n\n")
        
    print("Retrieved all student code.")
    return students


# load all the functions that will actually be playing
# error handling: returns list of bad_kids whose code had issues in the pastebin
def get_functions():
    
    students = get_students_and_code()
    functions = []
    bad_kids = []


    # log problems
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("BAD CODE (COMPILE)\nThe following students had errors in their code that prevented compiling (check syntax):\n\n")

    for i in tqdm(range(len(students))):
        # print("Loading student's functions:", students[i]["student_name"])
        try:
            exec(students[i]["code"])
            # print("this is okay")
            for function_name in students[i]["function_names"]:
                functions.append(eval(function_name))
        except Exception as e:
            error = students[i]["student_name"] + "\nError: " + str(e) + "\n"
            with open(PROBLEMS_LOG_LOCATION, "a") as f:
                f.write(error)
            # print("---\n Student code error")
            # print(students[i]["student_name"])
            # print(e)
            # print("---")
            bad_kids.append(students[i]["student_name"])

    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("\n---\n***\n---\n\n")
    
    loaded_functions = [f for f in locals().values() if type(f) == types.FunctionType]
    
    # print("These", len(bad_kids), "students messed up their code somehow: ", bad_kids)

    good, bad = filter_functions(loaded_functions)
    loaded_functions = good

    print("Removed", len(bad), "functions for being bad.")

    print("Loaded", len(loaded_functions), " good functions.")
    return loaded_functions

def filter_functions(functions):
    good_functions = []
    bad_functions = []
    
    # log problems
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("BAD CODE (IN/OUT)\nThe following functions had errors related to input or output:\n\n")
    
    for function in functions:
        try:
            with suppress_stdout():
                output = function([True]*10,[False]*10,10)
                if output==None:
                    raise Exception("function returned None (make sure you are returning something)")
                if output:
                    pass
                good_functions.append(function)
        except Exception as e:
            error = function.__name__ + "\nError: " + str(e) + "\n"
            with open(PROBLEMS_LOG_LOCATION, "a") as f:
                f.write(error)
            # print("Bad function:", function.__name__)
            # print(e)
            bad_functions.append(function)

    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("\n---\n***\n---\n\n")

    return good_functions, bad_functions


# config for running game
def get_game_inputs():
    strats = all_default_functions + get_functions()
    rounds = ROUNDS
    blindness = []
    if NOISE:
        blindness = [NOISE_LEVEL, NOISE_LEVEL]
    else:
        blindness = [0,0]
    return strats, rounds, blindness

