import numpy as np
import pandas as pd
import json
import copy
import gspread
import gspread_dataframe

from output_locations import *

def get_clean_data():
    raw_data = {}
    with open(RAW_OUT_LOCATION, 'r') as fp:
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
    return clean_data

def get_pairwise():
    clean_data = get_clean_data()
    pairwise = pd.DataFrame.from_dict(clean_data)
    return pairwise

def get_ranking():
    clean_data = get_clean_data()
    all_stats = []
    for strategy in clean_data.keys():
        strategy_stats = {}
        strategy_stats["Strategy"] = strategy
        
        scores = []
        opponent_scores = []
        for strat2 in clean_data[strategy].keys():
            scores.append(clean_data[strategy][strat2][0])
            opponent_scores.append(clean_data[strategy][strat2][1])
        
        total_points = np.sum(scores)
        average_points = total_points/len(scores)
        average_margin = np.sum(np.asarray(scores)-np.asarray(opponent_scores))/len(scores)

        strategy_stats["Total Points"] = total_points
        strategy_stats["Average Points"] = average_points
        strategy_stats["Average Margin"] = average_margin

        all_stats.append(strategy_stats)
    ranked = sorted(all_stats, key=lambda d: d['Total Points'], reverse=True)
    ranking = pd.DataFrame.from_dict(ranked)
    return ranking

def get_summary():
    specs = {}
    with open(SPECS_JSON_LOCATION, 'r') as fp:
        specs = json.load(fp)
    summary = pd.DataFrame.from_dict(specs, orient="index")
    return summary

def update_sheet():
    
    print("Updating results spreadsheet...")
    
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open("IPD LATEST RUN Results")

    summary_sheet = spreadsheet.worksheet("Summary Statistics")
    summary_sheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet=summary_sheet,dataframe=get_summary(),include_index=True,include_column_header=False,resize=True)

    ranking_sheet = spreadsheet.worksheet("Ranking")
    ranking_sheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet=ranking_sheet,dataframe=get_ranking(),include_index=False,include_column_header=True,resize=True)

    pairwise_sheet = spreadsheet.worksheet("Pairwise Scores")
    pairwise_sheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet=pairwise_sheet,dataframe=get_pairwise(),include_index=True,include_column_header=True,resize=True)
    

    print("Updated results spreadsheet.")
        
# update_sheet()

