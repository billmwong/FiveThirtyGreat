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

def combineData(api, web):
    web["TimeInt"] = web["Time"].apply(lambda x: int(x.replace(":", "")))    
    web.sort_values(["Game Date", "Q", "TimeInt"],ascending=[True, True, False])
    web.reset_index(drop=True, inplace =True)
    return pd.concat([api, web[["Shot Dist.","Opp.", "Drib.", "Shot Clock", "Touch Time","Defender", "Def Dist."]]], axis=1)

def transform_combined(data):
    
    action_type = pd.get_dummies(data.ACTION_TYPE)
    period = pd.get_dummies(data.PERIOD)
    shot_type = pd.get_dummies(data.SHOT_TYPE)
    shot_zone_basic = pd.get_dummies(data.SHOT_ZONE_BASIC)
    shot_zone_area = pd.get_dummies(data.SHOT_ZONE_AREA)
    shot_zone_range = pd.get_dummies(data.SHOT_ZONE_RANGE)

    shot_dist = data["Shot Dist."].apply(lambda x : x.replace("ft.", ""))
    # d_rating = data["Opp."].apply(lambda x: defensive_rating[x])
#     defender = pd.get_dummies(data["Defender"])
    
    new_shot_chart = pd.concat([ action_type, period, shot_type, shot_zone_basic, shot_zone_area, shot_zone_range, 
                                  data["Shot Clock"],data["Touch Time"],
                                data["Drib."],data["Def Dist."],
                                data.SHOT_MADE_FLAG], axis=1)
    return new_shot_chart


def testLogLoss_combined(transformed, model):
    predictors = transformed.columns[:-1]
    X_train, X_test, y_train, y_test = train_test_split(transformed, transformed.SHOT_MADE_FLAG, train_size=.5)
    print predictors
    model.fit(X_train[predictors], y_train)
    
    print "score",model.score(X_test[predictors], y_test)
    predicted = np.array(model.predict_proba(X_test[predictors]))
    print "Log_loss", log_loss(y_test, predicted)

def predictor(athlete, season):
	# athlete = "stephen curry"
	# season = "2014-15"
	web_df = webscrape.getData(athlete, season[:-3])
	# api_df = create_dataFrame(build_url(athlete, season))
	# combined = combineData(api_df, web_df)
	# transformed_combined = transform_combined(combined)
	web_df = web_df[["Shot Dist.", "Made?"]]
	web_df["Shot Dist."] = web_df["Shot Dist."].apply(lambda x : x.replace("ft.", ""))
	web_df["Made?"] = web_df["Made?"].apply(lambda x: 1 if x == "Yes" else 0)
	
	logistic = LogisticRegression()
	# predictors = transformed_combined.columns[:-1]
	# logistic.fit(transformed_combined[predictors], transformed_combined.SHOT_MADE_FLAG)
	
	predictors = web_df.columns[:-1]
	logistic.fit(web_df[predictors], web_df["Made?"])

	return logistic



