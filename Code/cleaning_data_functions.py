from path import Path
from uszipcode import SearchEngine
import mpu
import pandas as pd

team_acry = pd.read_csv(Path("../Data/misc_data/team_acry.csv"))

team_rooster = pd.read_csv(Path("../Data/misc_data/updated_team_rooster.csv"))
team_rooster.set_index("Player Name", inplace = True)



def clean_schedule_data(df, df1):
    
    # pulling only the columns we want from the pitching log dataframe
    df = df[["Game#", "Opp", "Result", "Starting Pitcher", "Opposing Pitcher"]]
    df.set_index("Game#", inplace = True)
    
    # pulling only the columns we want from the schedule log dataframe
    df1 = df1[["Hm/Aw", "Game#"]]
    df1.set_index("Game#", inplace = True)
    
    # combining into one dataframe to work with
    return_df = pd.merge(df, df1, left_index=True, right_index=True)
    return_df.dropna(inplace=True)
    
    # changing results from W/L to 1/0
    true_w = return_df["Result"].str.contains('W', na=True)
    binary_result = []
    for row in return_df.index:
        if true_w[row]:
            binary_result.append(1)
        else:
            binary_result.append(0)
        
    return_df["Result"] = binary_result
    
    
    # getting the distance between thw two clubs
    Home = []
    Away = []
    
    x = len(return_df)
    return_df.reset_index(inplace = True)
    return_df.drop(columns = "Game#", inplace = True)
    
    for number in return_df.index:
        if return_df.loc[number]["Hm/Aw"] == "Away":
            Home.append(return_df.loc[number]["Opp"])
            Away.append("HOU")
        else:
            Home.append("HOU")
            Away.append(return_df.loc[number]["Opp"])
            
    return_df["Home"] = Home
    return_df["Away"] = Away
        
    return_df["Distance"] = [get_home_away_distance_in_miles(home, away) for home, away in zip(return_df.Home, return_df.Away)]

    return_df['Distance'] = [distance * -1 if stadium == 'Home' else distance for stadium, 
                             distance in zip(return_df['Hm/Aw'], return_df['Distance'])]
    
    
    # setting index and dropping off columns we don't need anymore
    return_df.set_index("Opp", inplace = True)
    
    return_df.drop(columns = ["Hm/Aw", "Home", "Away"], inplace = True)
    
    return return_df


def clean_batting_data(df1):
    
    # dropping last two rows as they are average and total
    df1.drop(index = [30, 31], inplace = True)
    
    # setting index to team name
    df1.set_index("Tm", inplace = True)
    
    # setting index to match for team acry df
    team_acry.set_index("Team(Bat)", inplace = True)
    
    # changing team names to match
    new_team_name = []

    for team in df1.index:
        if team in team_acry.index:
            new_team_name.append(team_acry.loc[team]["Team(New)"])
            
    df1.index = new_team_name
    
    # pulling only the metrics we want
    df1 = df1[["BatAge", "R/G", "PA", "AB", "H", "2B", "3B", "HR", "BB", "SO", "BA", "OBP", "SLG", "OPS", "TB", "HBP", "LOB"]]
    
    # resetting index for team acry df
    team_acry.reset_index(inplace = True)
    
    # returning the dataframe
    return df1


def clean_pitching_data(df):
    
    # need to get rid of extra space in pitcher names
    random_number = list(range(len(df)))
    list_of_pitchers = []
    for number in random_number:
        string = df["Name"][number] 
        string = string.replace(u'\xa0', u' ')
        list_of_pitchers.append(string)
    df["Pitcher"] = list_of_pitchers
    
    # setting index to pitchers
    df = df.groupby("Pitcher").mean()
    
    # pulling only the metrics we want
    df = df[["ERA", "CG", "IP", "ERA+", "FIP", "WHIP", "H9", "HR9", "BB9", "SO9", "SO/W"]]
    
    # returning the dataframe
    return df

def get_distance_in_miles(home_team_zip, away_team_zip):        
    
    #for extensive list of zipcodes, set simple_zipcode=False
    search = SearchEngine(simple_zipcode=True)
    zip1 = search.by_zipcode(home_team_zip)
    zip2 = search.by_zipcode(away_team_zip)

    return round(mpu.haversine_distance((zip1.lat, zip1.lng), (zip2.lat, zip2.lng)), 2)

def get_home_away_distance_in_miles(home_team_code, away_team_code):
    
    teams = [
        { 'team': 'ARI', 'name': 'Arizona Diamondbacks', 'address': '401 E Jefferson St, Phoenix, AZ 85004' },
        { 'team': 'ATL', 'name': 'Atlanta Braves',  'address': '755 Battery Ave SE, Atlanta, GA 30339' },
        { 'team': 'BAL', 'name': 'Baltimore Orioles', 'address': '333 W Camden St, Baltimore, MD 21201' },
        { 'team': 'BOS', 'name': 'Boston Red Sox', 'address': '4 Jersey St, Boston, MA 02215' },
        { 'team': 'CHA', 'name': 'Chicago White Sox', 'address': '333 W 35th St, Chicago, IL 60616'},
        { 'team': 'CHN', 'name': 'Chicago Cubs', 'address': '1060 W Addison St, Chicago, IL 60613' },
        { 'team': 'CIN', 'name': 'Cincinnati Reds', 'address': '100 Joe Nuxhall Way, Cincinnati, OH 45202' }, 
        { 'team': 'CLE', 'name': 'Cleveland Indians', 'address': '2401 Ontario St, Cleveland, OH 44115' },
        { 'team': 'COL', 'name': 'Colorado Rockies', 'address': '2001 Blake St, Denver, CO 80205' },
        { 'team': 'DET', 'name': 'Detroit Tigers', 'address': '2100 Woodward Ave, Detroit, MI 48201' },
        { 'team': 'HOU', 'name': 'Houston Astros', 'address': '501 Crawford St, Houston, TX 77002' },
        { 'team': 'KCA', 'name': 'Kansas City Royals', 'address': '1 Royal Way, Kansas City, MO 64129' },
        { 'team': 'ANA', 'name': 'Los Angeles Angels', 'address': '2000 E Gene Autry Way, Anaheim, CA 92806' },
        { 'team': 'LAN', 'name': 'Los Angeles Dodgers', 'address': '1000 Vin Scully Ave, Los Angeles, CA 90012' },
        { 'team': 'MIA', 'name': 'Miami Marlins', 'address': '501 Marlins Way, Miami, FL 33125' },
        { 'team': 'MIL', 'name': 'Milwaukee Brewers', 'address': '1 Brewers Way, Milwaukee, WI 53214' },
        { 'team': 'MIN', 'name': 'Minnesota Twins', 'address': '1 Twins Way, Minneapolis, MN 55403' },
        { 'team': 'NYA', 'name': 'New York Yankees', 'address': '1 E 161 St, The Bronx, NY 10451' },
        { 'team': 'NYN', 'name': 'New York Mets', 'address': '41 Seaver Way, Queens, NY 11368' },
        { 'team': 'OAK', 'name': 'Oakland Athletics', 'address': '7000 Coliseum Way, Oakland, CA 94621' },
        { 'team': 'PHI', 'name': 'Philadelphia Phillies', 'address': '1 Citizens Bank Way, Philadelphia, PA 19148' },
        { 'team': 'PIT', 'name': 'Pittsburgh Pirates', 'address': '115 Federal St, Pittsburgh, PA 15212' },
        { 'team': 'SDN', 'name': 'San Diego Padres', 'address': '100 Park Blvd, San Diego, CA 92101' },
        { 'team': 'SFN', 'name': 'San Francisco Giants', 'address': '24 Willie Mays Plaza, San Francisco, CA 94107' },
        { 'team': 'SEA', 'name': 'Seattle Mariners', 'address': '1250 1st Ave S, Seattle, WA 98134' },
        { 'team': 'SLN', 'name': 'St. Louis Cardinals', 'address': '700 Clark Ave, St. Louis, MO 63102' },
        { 'team': 'TBA', 'name': 'Tampa Bay Rays', 'address': '1 Tropicana Dr., St. Petersburg, FL 33705' },
        { 'team': 'TEX', 'name': 'Texas Rangers', 'address': '734 Stadium Dr, Arlington, TX 76011' },
        { 'team': 'TOR', 'name': 'Toronto Blue Jays', 'address': '1 Blue Jays Way, Toronto, ON 14305' },
        { 'team': 'WAS', 'name': 'Washington Nationals', 'address': '1500 S Capitol St SE, Washington, DC 20003' }
    ]

    teams_zip_df = pd.DataFrame.from_dict(teams)

    teams_zip_df['zip'] = teams_zip_df['address'].str.split(',', expand=True)[2].str.split(' ', expand=True)[2]
    teams_zip_df.sort_values("team", inplace=True) 
    teams_zip_df.set_index('team', inplace=True)    
        
    return get_distance_in_miles(
        home_team_zip = teams_zip_df.loc[home_team_code]['zip'], 
        away_team_zip = teams_zip_df.loc[away_team_code]['zip'])

def combine_year_df(df_result_schedule, df_bat, df_pitch, team):
        
    # gathering Houston Astros batting averages
    df_team = df_bat.loc[team]
    df_team = pd.DataFrame(df_team)
    df_team = df_team.transpose()
    df_team.rename(columns = {
        "BatAge" : "Favorite-BatAge", 
        "R/G" : "Favorite-R/G", 
        "PA" : "Favorite-PA", 
        "AB" : "Favorite-AB", 
        "H" : "Favorite-H", 
        "2B" : "Favorite-2B", 
        "3B" : "Favorite-3B", 
        "HR" : "Favorite-HR",
        "BB" : "Favorite-BB", 
        "SO" : "Favorite-SO", 
        "BA" : "Favorite-BA", 
        "OBP" : "Favorite-OBP", 
        "SLG" : "Favorite-SLG", 
        "OPS" : "Favorite-OPS", 
        "TB" : "Favorite-TB", 
        "HBP" : "Favorite-HBP", 
        "LOB" : "Favorite-LOB",
                }, inplace=True)
    
    # merging databases
    merge_df = pd.merge(df_result_schedule, df_bat, left_index=True, right_index=True)
    df_team["key"] = 1
    merge_df["key"] = 1
    df = pd.merge(df_team, merge_df, on='key')
    del df['key']
    
    # pulling metrics for the pitchers    
    random_number = list(range(len(df)))
    
    opp_pitch_class = []
    opp_pitch_class_2 = []
    opp_pitch_class_3 = []
    opp_pitch_class_4 = []
    opp_pitch_class_5 = []
    opp_pitch_class_6 = []
    opp_pitch_class_7 = []
    opp_pitch_class_8 = []
    opp_pitch_class_9 = []
    opp_pitch_class_10 = []
    opp_pitch_class_11 = []
    
    for number in random_number:
        if df["Opposing Pitcher"][number] in df_pitch.index:
            name = df["Opposing Pitcher"][number]
            opp_pitch_class.append(df_pitch.loc[name]["ERA"])
            opp_pitch_class_2.append(df_pitch.loc[name]["CG"])
            opp_pitch_class_3.append(df_pitch.loc[name]["IP"])
            opp_pitch_class_4.append(df_pitch.loc[name]["ERA+"])
            opp_pitch_class_5.append(df_pitch.loc[name]["FIP"])
            opp_pitch_class_6.append(df_pitch.loc[name]["WHIP"])
            opp_pitch_class_7.append(df_pitch.loc[name]["H9"])
            opp_pitch_class_8.append(df_pitch.loc[name]["HR9"])
            opp_pitch_class_9.append(df_pitch.loc[name]["BB9"])
            opp_pitch_class_10.append(df_pitch.loc[name]["SO9"])
            opp_pitch_class_11.append(df_pitch.loc[name]["SO/W"])
        else:
            opp_pitch_class.append(0)
            opp_pitch_class_2.append("N/A")
            opp_pitch_class_3.append("N/A")
            opp_pitch_class_4.append("N/A")
            opp_pitch_class_5.append("N/A")
            opp_pitch_class_6.append("N/A")
            opp_pitch_class_7.append("N/A")
            opp_pitch_class_8.append("N/A")
            opp_pitch_class_9.append("N/A")
            opp_pitch_class_10.append("N/A")
            opp_pitch_class_11.append("N/A")

    start_pitch_class = []
    start_pitch_class_2 = []
    start_pitch_class_3 = []
    start_pitch_class_4 = []
    start_pitch_class_5 = []
    start_pitch_class_6 = []
    start_pitch_class_7 = []
    start_pitch_class_8 = []
    start_pitch_class_9 = []
    start_pitch_class_10 = []
    start_pitch_class_11 = []
       
    for number in random_number:
        if df["Starting Pitcher"][number] in df_pitch.index:
            name = df["Starting Pitcher"][number]
            start_pitch_class.append(df_pitch.loc[name]["ERA"])
            start_pitch_class_2.append(df_pitch.loc[name]["CG"])
            start_pitch_class_3.append(df_pitch.loc[name]["IP"])
            start_pitch_class_4.append(df_pitch.loc[name]["ERA+"])
            start_pitch_class_5.append(df_pitch.loc[name]["FIP"])
            start_pitch_class_6.append(df_pitch.loc[name]["WHIP"])
            start_pitch_class_7.append(df_pitch.loc[name]["H9"])
            start_pitch_class_8.append(df_pitch.loc[name]["HR9"])
            start_pitch_class_9.append(df_pitch.loc[name]["BB9"])
            start_pitch_class_10.append(df_pitch.loc[name]["SO9"])
            start_pitch_class_11.append(df_pitch.loc[name]["SO/W"])
        else:
            start_pitch_class.append(0)
            start_pitch_class_2.append("N/A")
            start_pitch_class_3.append("N/A")
            start_pitch_class_4.append("N/A")
            start_pitch_class_5.append("N/A")
            start_pitch_class_6.append("N/A")
            start_pitch_class_7.append("N/A")
            start_pitch_class_8.append("N/A")
            start_pitch_class_9.append("N/A")
            start_pitch_class_10.append("N/A")
            start_pitch_class_11.append("N/A")
    
    # adding all the pitching metrics
    return_df = df
    return_df["ERA_Starting"] = start_pitch_class
    return_df["ERA_Opposing"] = opp_pitch_class
    return_df["CG_Starting"] = start_pitch_class_2
    return_df["CG_Opposing"] = opp_pitch_class_2
    return_df["IP_Starting"] = start_pitch_class_3
    return_df["IP_Opposing"] = opp_pitch_class_3
    return_df["ERA+_Starting "] = start_pitch_class_4
    return_df["ERA+_Opposing"] = opp_pitch_class_4
    return_df["FIP_Starting"] = start_pitch_class_5
    return_df["FIP_Opposing"] = opp_pitch_class_5
    return_df["WHIP_Starting"] = start_pitch_class_6
    return_df["WHIP_Opposing"] = opp_pitch_class_6
    return_df["H9_Starting "] = start_pitch_class_7
    return_df["H9_Opposing"] = opp_pitch_class_7
    return_df["HR9_Starting"] = start_pitch_class_8
    return_df["HR9_Opposing"] = opp_pitch_class_8
    return_df["BB9_Starting"] = start_pitch_class_9
    return_df["BB9_Opposing"] = opp_pitch_class_9
    return_df["SO9_Starting "] = start_pitch_class_10
    return_df["SO9_Opposing"] = opp_pitch_class_10
    return_df["SO/W_Starting"] = start_pitch_class_11
    return_df["SO/W_Opposing"] = opp_pitch_class_10
    
    # deleting any rows where pitcher data was not found
    return_df = return_df[return_df.HR9_Starting != "N/A"]
    return_df = return_df[return_df.HR9_Opposing != "N/A"]
    # return_df = return_df[return_df.ERA_Starting != 0]
    # return_df = return_df[return_df.ERA_Opposing != 0]
    
    # dropping starting and opposing pitcher as we have their metrics now
    return_df.drop(["Starting Pitcher", "Opposing Pitcher"], axis=1, inplace = True)
    
    # returning dataframe
    return return_df