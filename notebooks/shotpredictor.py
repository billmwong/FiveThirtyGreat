import requests
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, LogisticRegressionCV

from nba_py import player
import webscrape

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
    pred = ['Shot Dist.','Def Dist.', 'else', 'jump', 'layup', 'Made?']

    return new_shot_chart[pred]


def predictor(athlete, season):

    web_df = webscrape.getData(athlete, season)
    transformed_web = transform_web(web_df)
    logistic = LogisticRegression()

    predictors = transformed_web.columns[:-1]

    logistic.fit(transformed_web[predictors], transformed_web["Made?"])
    return logistic


def transform_big(data):

    data = data.copy()
    shot_type = pd.get_dummies(data["Shot Type"].apply(shot))
    data["Shot Dist."] = data["Shot Dist."].apply(lambda x : x.replace("ft.", ""))
    data["Shot Dist."] = data["Shot Dist."].apply(lambda x : 0 if x== "" else float(x))
    
    # shot_clock = data["Shot Clock"].apply(lambda x: 0 if x == "" else float(x))
    # touch_time = data["Touch Time"].apply(lambda x: float(x))
    # drib = data["Drib."].apply(lambda x: int(x))
    data["Def Dist."] = data["Def Dist."].apply(lambda x: float(x))

    def_dist_c = pd.get_dummies(data["Def Dist."].apply(def_dist))
    
    player_c = pd.get_dummies(data["Player"])

    shot_dist_c = pd.get_dummies(data["Shot Dist."].apply(shot_dist))
    
    con = [player_c, shot_type , data["Def Dist."],
           def_dist_c, shot_dist_c, data["Shot Dist."],(data["Made?"]=="Yes").astype(int)]
    
#     con = [player_c, shot_type, shot_clock, touch_time, drib, 
#            shot_dist_c, data["Shot Dist."],(data["Made?"]=="Yes").astype(int)]
        
    new_shot_chart = pd.concat(con , axis=1)

    pred = player_c.columns[:len(player_c)].tolist()+ ['Shot Dist.', 'Def Dist.', 'else', 'jump', 'layup', 'Made?']

    return new_shot_chart[pred]

def getDataFrame(lst):
    app = []
    for player in lst:
        app.append(webscrape.getData(player, "2014"))
    print "done"
    df_a = pd.concat(app)
    df_a.reset_index(drop=True, inplace =True)
    return transform_big(df_a)

guards_100 = [
    "James Harden","Damian Lillard","Chris Paul","John Wall","Eric Bledsoe","Joe Johnson","Kyrie Irving","Monta Ellis",
     "Tyreke Evans","Ben McLemore","Ty Lawson","Goran Dragic","Stephen Curry","Kentavious Caldwell-Pope","Victor Oladipo",
     "Jimmy Butler","Arron Afflalo","Elfrid Payton","Klay Thompson","Avery Bradley","Kyle Korver","Kyle Lowry",
     "JJ Redick","Mario Chalmers","Courtney Lee","Gerald Henderson","Danny Green","Russell Westbrook","Trey Burke",
     "Reggie Jackson","Evan Turner","Jarrett Jack","Jeff Teague","Mike Conley","Dion Waiters","Michael Carter-Williams",
     "Kemba Walker","Deron Williams","Bradley Beal","DeMar DeRozan","J.R. Smith","Andre Iguodala","Brandon Knight",
     "Wesley Matthews","Eric Gordon","Rajon Rondo","Lou Williams","Greivis Vasquez","Mo Williams","Dwyane Wade","D.J. Augustin",
     "Tony Parker","Jeremy Lin","Zach LaVine","Aaron Brooks","Rodney Stuckey","Shane Larkin","Bojan Bogdanovic","CJ Miles",
     "Norris Cole","Dante Exum","Marcus Smart","Anthony Morrow","Quincy Pondexter","Hollis Thompson","Alan Anderson",
     "Patrick Beverley","Isaiah Thomas","Jerryd Bayless","Jamal Crawford","O.J. Mayo","Devin Harris","Tim Hardaway",
     "Wayne Ellington","Evan Fournier","Tony Allen","Jason Terry","Kirk Hinrich","Manu Ginobili","Lance Stephenson",
     "Darren Collison","Austin Rivers","Iman Shumpert","Derrick Rose","Steve Blake","Dennis Schroder","Rasual Butler",
     "Beno Udrih","Jordan Clarkson","Shaun Livingston","Jodie Meeks","Langston Galloway","Gerald Green","Cory Joseph",
     "Ray McCallum","CJ Watson","Tony Snell","Jameer Nelson","Marco Belinelli","Matthew Dellavedova"
]

forwards_100 = [
    "Andrew Wiggins","Trevor Ariza","Pau Gasol","Gordon Hayward","Markieff Morris","Giannis Antetokounmpo","Kevin Love",
    "LaMarcus Aldridge","LeBron James","Draymond Green","Wilson Chandler","Anthony Davis","Jeff Green","Thaddeus Young",
    "Luol Deng","Rudy Gay","Paul Millsap","PJ Tucker","Solomon Hill","Nicolas Batum","Khris Middleton","Tobias Harris",
    "Blake Griffin","Harrison Barnes","Al Horford","Nerlens Noel","Zach Randolph","Josh Smith","Dirk Nowitzki",
    "Derrick Favors","Matt Barnes","Wesley Johnson","Tim Duncan","Tristan Thompson","DeMarre Carroll","Chandler Parsons",
    "Patrick Patterson","Serge Ibaka","Terrence Ross","Corey Brewer","Kenneth Faried","Marcus Morris","Donatas Motiejunas",
    "Marvin Williams","Kawhi Leonard","Jason Thompson","Boris Diaw","Amir Johnson","Robert Covington","Brandon Bass",
    "Paul Pierce","David West","Channing Frye","Ed Davis","Mike Dunleavy","Jason Smith","Mason Plumlee",
    "Kyle Singler","Tyler Zeller","Jared Dudley","Taj Gibson","Ryan Anderson","Joe Ingles","Luis Scola",
    "Nikola Mirotic","Dante Cunningham","Jae Crowder","Caron Butler","Michael Kidd-Gilchrist","Jared Sullinger","Trevor Booker",
    "Chris Bosh","Lance Thomas","Cody Zeller","Derrick Williams","Brandan Wright","Otto Porter","Anthony Tolliver",
    "Carmelo Anthony","Danilo Gallinari","Kelly Olynyk","Omri Casspi","JJ Hickson","Tayshaun Prince","Jerami Grant",
    "James Johnson","Al-Farouq Aminu","Kris Humphries","Ersan Ilyasova","Quincy Acy","Chase Budinger","Amar'e Stoudemire",
    "Richard Jefferson","Kevin Seraphin","Ryan Kelly","Jonas Jerebko","John Henson","Carl Landry"
]

centers_100 = [
    "DeAndre Jordan","Marc Gasol","Nikola Vucevic","Andre Drummond","Marcin Gortat","Tyson Chandler","Gorgui Dieng",
    "Rudy Gobert","Greg Monroe","Enes Kanter","Brook Lopez","Jonas Valanciunas","Joakim Noah","Timofey Mozgov",
    "DeMarcus Cousins","Al Jefferson","Omer Asik","Roy Hibbert","Jordan Hill","Steven Adams","Zaza Pachulia",
    "Robin Lopez","Andrew Bogut","Alex Len","Henry Sims","Chris Kaman","Kosta Koufos","Spencer Hawes","Bismack Biyombo",
    "Dwight Howard","Marreese Speights","Tarik Black","Miles Plumlee","Kendrick Perkins","Ian Mahinmi","Hassan Whiteside",
    "Robert Sacre","Aron Baynes","Jusuf Nurkic","Cole Aldrich","Alexis Ajinca","Meyers Leonard","Dewayne Dedmon",
    "Kyle O'Quinn","Nikola Pekovic","Justin Hamilton","Samuel Dalembert","Festus Ezeli","Ryan Hollins","Joel Anthony",
    "Jerome Jordan","Greg Smith","Jeff Withey","JaVale McGee","Bernard James","Earl Barron","Nazr Mohammed","Clint Capela"
]

def large_model(lst):
    df_guards = getDataFrame(lst)
    
    logistic = LogisticRegression()

    predictors = df_guards.columns[:-1]

    logistic.fit(df_guards[predictors], df_guards["Made?"])
    return logistic, predictors

def guards_m():
    return large_model(guards_100)

# guards_m()