import requests
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, LogisticRegressionCV

from nba_py import player
import webscrape

def create_dataFrame(shot_chart_url):
    response = requests.get(shot_chart_url)
    # Grab the headers to be used as column headers for our DataFrame
    headers = response.json()['resultSets'][0]['headers']
    # Grab the shot chart data
    shots = response.json()['resultSets'][0]['rowSet']
    return pd.DataFrame(shots, columns=headers)
    
def get_player_id(name):
    name = name.split(' ')
    return player.get_player(name[0], name[1], just_id=True)

def build_url(name, season):
    p_id = str(int(get_player_id(name)))
    url = "http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&Position=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season="+season+"&AheadBehind=&PlayerID="+ p_id+"&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID="
    return url


def shot(s_type):
    if "jump shot" in s_type.lower():
        return "jump"
    elif "layup shot" in s_type.lower():
        return "layup"
    else:
        return "else"
    
def shot_dist(dist):
    if dist < 8:
        return "less than 8"
    elif dist < 16:
        return "8-16"
    elif dist < 24:
        return "16-24"
    else:
        return "24+"
    
def def_dist(dist):
    if dist < 2:
        return "0-2"
    elif dist < 4:
        return "2-4"
    elif dist < 6:
        return "4-6"
    else:
        return "6+"

def transform_web(data):
    data = data.copy()
    shot_type = pd.get_dummies(data["Shot Type"].apply(shot))
    data["Shot Dist."] = data["Shot Dist."].apply(lambda x : float(x.replace("ft.", "")))
    shot_clock = data["Shot Clock"].apply(lambda x: float(x))
    touch_time = data["Touch Time"].apply(lambda x: float(x))
    drib = data["Drib."].apply(lambda x: int(x))
    data["Def Dist."] = data["Def Dist."].apply(lambda x: float(x))

    def_dist_c = pd.get_dummies(data["Def Dist."].apply(def_dist))

    
    shot_dist_c = pd.get_dummies(data["Shot Dist."].apply(shot_dist))
    # if "24+" not in shot_dist_c.columns:
    #     shot_dist_c["24+"] = 0
    
    con = [shot_type, shot_clock, data["Shot Dist."],touch_time, drib, data["Def Dist."],def_dist_c, shot_dist_c, (data["Made?"]=="Yes").astype(int)]
    new_shot_chart = pd.concat(con , axis=1)

    # pred = ['16-24', '24+', '8-16', 'less than 8', 'else', 'jump', 'layup', 'Made?']
    pred = ['Shot Dist.', 'else', 'jump', 'layup', 'Made?']

    return new_shot_chart[pred]


def predictor(athlete, season):

    web_df = webscrape.getData(athlete, season)
    transformed_web = transform_web(web_df)
    logistic = LogisticRegression()

    predictors = transformed_web.columns[:-1]

    logistic.fit(transformed_web[predictors], transformed_web["Made?"])
    return logistic
