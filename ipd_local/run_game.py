import gspread

service_account = gspread.service_account(filename="service_account.json")
spreadsheet = service_account.open("IPD Player Strategies")
wks = spreadsheet.worksheet("Sheet1")

# TOURNAMENT SPECS
NOISE = False # whether or not this tournament has noise
NOISE_LEVEL = 0.1 # percentage noise; only used if NOISE is set to True



# print(wks.get_all_values())
# wks.update("A3", "student 2 updated!")

for i in range(10):
    print(i)
print(":)")