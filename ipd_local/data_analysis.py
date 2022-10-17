import pandas as pd
import json
import copy
from IPython.display import display

print("hi")

def produce_clean_data():
    raw_data = {}
    with open('./latest_raw_out.json', 'r') as fp:
        raw_data = json.load(fp)
    
    clean_data = copy.deepcopy(raw_data)
    for k in list(clean_data.keys()):
        for j in list(clean_data[k].keys()):
          if (type(clean_data[k][j])== dict):
            for key in list(clean_data[k][j].keys()):
                if key == "details":
                    del clean_data[k][j][key]
    for k in list(clean_data.keys()):
        for j in list(clean_data[k].keys()):
          if (type(clean_data[k][j])== dict):
            clean_data[k][j] = list(clean_data[k][j].values())[0]
    return(clean_data)

produce_clean_data()
