import gspread
import requests
from tqdm import tqdm
import types




# TOURNAMENT SPECS
NOISE = False # whether or not this tournament has noise
NOISE_LEVEL = 0.1 # percentage noise; only used if NOISE is set to True




# retrieve latest list of submissions from google sheets
# link to the sheet: https://docs.google.com/spreadsheets/d/1YZZQFShRcYO4p3pCqBY5LPZf4pO9zfmt6b6BNItVb3g/edit?usp=sharing
def get_spreadsheet_data():
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open("IPD Player Strategies")
    worksheet = spreadsheet.worksheet("Form Responses 1")
    return worksheet.get_all_values()




# returns an array of dictionary objects, each being a student
# student format: {name, link, function_names, code}
#                 where function_names is a list
def get_students_and_code():

    data = get_spreadsheet_data()
    students = []
    for i in range(1, len(data)):
        student = {}
        student["student_name"] = data[i][1]

        # accessing and parsing code from pastebin
        index = 2
        if NOISE:
            index = 3
        link = data[i][index]
        link = "https://pastebin.com/raw/" + link.split("pastebin.com/")[-1] # link to raw text on pastebin
        code = requests.get(link).text # retrieves the text

        # getting function names
        lines=code.split('\n')
        function_names = []
        for line in lines:
            if line!="" and line[0]!=" " and line[0]!="#" and len(line)>1:
                try:
                    function_names.append(line.split()[1].split("(")[0]) # splits at space by default
                except Exception as e:
                    print("ERROR: ", e)

        student["link"] = link
        student["function_names"] = function_names
        student["code"] = code
        
        students.append(student)
    
    return students


# load all the functions that will actually be playing
# error handling: returns list of bad_kids whose code had issues in the pastebin
def get_functions():
    
    students = get_students_and_code()
    functions = []
    bad_kids = []

    for i in tqdm(range(len(students))):
        try:
            exec(students[i]["code"])
            for function_name in students[i]["function_names"]:
                functions.append(eval(function_name))
        except Exception as e:
            print("ERROR")
            print(e)
            print(students[i]["name"])
            print(students[i]["code"])
            bad_kids.append(students[i]["name"])
    
    loaded_functions = [f for f in locals().values() if type(f) == types.FunctionType]
    print("Total functions: ", len(loaded_functions))
    
    print("These", len(bad_kids), "students messed up their code somehow: ", bad_kids)

    return loaded_functions






get_functions()

# wks.update("A3", "student 2 updated!")

