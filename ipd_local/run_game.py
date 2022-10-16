import gspread
import requests




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
# student format: {name, {link, function_names, code} for no noise and noise}
#                 where function_names is a list
# error handling: returns list of students whose code had issues in the pastebin
def get_students_and_code():
    
    data = get_spreadsheet_data()
    students = []
    for i in range(1, len(data)):
        student = {}
        student["student_name"] = data[i][1]
        
        # accessing and parsing code from pastebin
        for j in range(2):
            link = data[i][2+j]
            link = "https://pastebin.com/raw/" + link.split("pastebin.com/")[-1]
            code = requests.get(link).text

            # getting function names
            lines=code.split('\n')
            function_names = []
            for line in lines:
                if line!="" and line[0]!=" " and line[0]!="#" and len(line)>1:
                    try:
                        function_names.append(line.split()[1].split("(")[0]) # splits at space by default
                    except Exception as e:
                        print("ERROR: ", e)

            student_strategies = {}
            student_strategies["link"] = link
            student_strategies["function_names"] = function_names
            student_strategies["code"] = code

            if j == 0:
                student["noise_false"] = student_strategies
            else:
                student["noise_true"] = student_strategies
        
        students.append(student)
    
    return students





get_students_and_code()

# wks.update("A3", "student 2 updated!")

