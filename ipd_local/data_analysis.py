import numpy as np
import pandas as pd
import json
import copy
import gspread
import gspread_dataframe

from output_locations import *


# gets clean set of data from json of raw simulation output
# outputs dictionary of dictionaries, where each key (for both dimensions) is a strategy. the values of the nested dictionaries are pairs of scores for the two functions, in a list.
# the first value in the pair is the function of the outer dictionary key, while the second is the inner one.
# for example, clean_data["f1"]["f2"] = [0,10] means f1 scored 0 and f2 scored 10.
def get_clean_data():
    
    # read data from json where raw output is logged
    raw_data = {}
    with open(RAW_OUT_LOCATION, 'r') as fp:
        raw_data = json.load(fp)
    
    # create copy of this data that excludes the exact scores per round
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


# returns pairwise scores for all functions as a pandas dataframe.
# column is first function, row is second function.
def get_pairwise():
    clean_data = get_clean_data()
    pairwise = pd.DataFrame.from_dict(clean_data)
    return pairwise


# returns functions ranked by total score as pandas dataframe
# also lists each function's average score and average margin (how much higher do they score compared to opponent)
def get_ranking():
    
    clean_data = get_clean_data()
    all_stats = []

    # calculates statistics for each function
    for strategy in clean_data.keys():
        strategy_stats = {}
        strategy_stats["Strategy"] = strategy
        
        # retrive scores
        scores = []
        opponent_scores = []
        for strat2 in clean_data[strategy].keys():
            scores.append(clean_data[strategy][strat2][1])
            opponent_scores.append(clean_data[strategy][strat2][0])
        
        # calculate each metric
        total_points = np.sum(scores)
        average_points = total_points/len(scores)
        # average_margin = np.sum(np.asarray(scores)-np.asarray(opponent_scores))/len(scores)

        strategy_stats["Total Points"] = total_points
        strategy_stats["Average Points"] = average_points
        # strategy_stats["Average Margin"] = average_margin

        all_stats.append(strategy_stats)
    
    ranked = sorted(all_stats, key=lambda d: d['Total Points'], reverse=True) # sorts functions by total score
    ranking = pd.DataFrame.from_dict(ranked)
    return ranking

# returns summary of game as pandas dataframe
# summary items include noise (true/false), noise level, number of rounds, and score matrix
def get_summary():
    specs = {}
    with open(SPECS_JSON_LOCATION, 'r') as fp:
        specs = json.load(fp)
    summary = pd.DataFrame.from_dict(specs, orient="index")
    return summary

# retrieves all statistics (pairwise, ranking, and summary) and updates them on google spreadsheet.
# this spreadsheet can be found here: https://docs.google.com/spreadsheets/d/138rZ0hdy4MfFmvb1wZqgmeckGUpNl0N0T4wpAPXWeZE/edit?usp=sharing
def update_sheet():
    
    print("Updating results spreadsheet...")
    
    # accesses correct google spreadsheet for results
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open("IPD LATEST RUN Results")

    # updates summary
    summary_sheet = spreadsheet.worksheet("Summary Statistics")
    summary_sheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet=summary_sheet,dataframe=get_summary(),include_index=True,include_column_header=False,resize=True)

    # updates ranking
    ranking_sheet = spreadsheet.worksheet("Ranking")
    ranking_sheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet=ranking_sheet,dataframe=get_ranking(),include_index=False,include_column_header=True,resize=True)

    # updates pairwise scores
    pairwise_sheet = spreadsheet.worksheet("Pairwise Scores")
    pairwise_sheet.clear()
    
    # reverse order of score reporting
    clean_data = get_pairwise()
    for k in list(clean_data.keys()):
        for j in list(clean_data[k].keys()):
            # reverse first and second element
            rev = []
            rev.append(clean_data[k][j][1])
            rev.append(clean_data[k][j][0])
            clean_data[k][j] = rev
    
    gspread_dataframe.set_with_dataframe(worksheet=pairwise_sheet,dataframe=clean_data,include_index=True,include_column_header=True,resize=True)
    
    print("Updated results spreadsheet.")
