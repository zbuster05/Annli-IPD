import pandas as pd
import json
from IPython.display import display

print("hi")

def produce_clean_data():
    raw_data = {}
    with open('./latest_raw_out.json', 'r') as fp:
        raw_data = json.load(fp)
    print(raw_data["rat"])
