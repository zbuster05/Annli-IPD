import ipd_local
import random
import pandas as pd
import gspread
import gspread_dataframe

random.seed(0)

def set_temp_sheet(name: str, contents: pd.DataFrame, tab_name: str = None):
    gc = gspread.service_account(filename = "./service_account.json")
    try: 
        sh = gc.open(name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(name)

    if tab_name:
        try:
            worksheet = sh.worksheet(tab_name)
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=tab_name, rows=10, cols=10)
    else:
        if sh.worksheets == []:
            worksheet = sh.add_worksheet(title="Untitled", rows=10, cols=10)
        else:
            worksheet = sh.worksheets[0]
    gspread_dataframe.set_with_dataframe(worksheet, contents)
    
