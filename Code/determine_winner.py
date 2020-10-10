from path import Path
import pandas as pd

team_acry = pd.read_csv(Path("../Data/misc_data/team_acry.csv"))

team_rooster = pd.read_csv(Path("../Data/misc_data/updated_team_rooster.csv"))
team_rooster.set_index("Player Name", inplace = True)


def determine_who_wins(starting_pitcher, opposing_pitcher, home_or_away):
    
    
    # gathering pitching data from two inputs in the function
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
    
    if opposing_pitcher in df_pitch.index:
        opp_pitch_class.append(df_pitch.loc[opposing_pitcher]["ERA"])
        opp_pitch_class_2.append(df_pitch.loc[opposing_pitcher]["CG"])
        opp_pitch_class_3.append(df_pitch.loc[opposing_pitcher]["IP"])
        opp_pitch_class_4.append(df_pitch.loc[opposing_pitcher]["ERA+"])
        opp_pitch_class_5.append(df_pitch.loc[opposing_pitcher]["FIP"])
        opp_pitch_class_6.append(df_pitch.loc[opposing_pitcher]["WHIP"])
        opp_pitch_class_7.append(df_pitch.loc[opposing_pitcher]["H9"])
        opp_pitch_class_8.append(df_pitch.loc[opposing_pitcher]["HR9"])
        opp_pitch_class_9.append(df_pitch.loc[opposing_pitcher]["BB9"])
        opp_pitch_class_10.append(df_pitch.loc[opposing_pitcher]["SO9"])
        opp_pitch_class_11.append(df_pitch.loc[opposing_pitcher]["SO/W"])
    else:
        print("Opposing Pitcher Not Found")

    
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
       
    if starting_pitcher in df_pitch.index:
        start_pitch_class.append(df_pitch.loc[starting_pitcher]["ERA"])
        start_pitch_class_2.append(df_pitch.loc[starting_pitcher]["CG"])
        start_pitch_class_3.append(df_pitch.loc[starting_pitcher]["IP"])
        start_pitch_class_4.append(df_pitch.loc[starting_pitcher]["ERA+"])
        start_pitch_class_5.append(df_pitch.loc[starting_pitcher]["FIP"])
        start_pitch_class_6.append(df_pitch.loc[starting_pitcher]["WHIP"])
        start_pitch_class_7.append(df_pitch.loc[starting_pitcher]["H9"])
        start_pitch_class_8.append(df_pitch.loc[starting_pitcher]["HR9"])
        start_pitch_class_9.append(df_pitch.loc[starting_pitcher]["BB9"])
        start_pitch_class_10.append(df_pitch.loc[starting_pitcher]["SO9"])
        start_pitch_class_11.append(df_pitch.loc[starting_pitcher]["SO/W"])
    else:
        print("Starting Pitcher Not Found")    
        
        
    # gathering batting metrics from pitchers' team
    if opposing_pitcher in team_rooster.index:
        opp_team_name = team_rooster.loc[opposing_pitcher]["Team Name"]
    
    if opp_team_name in df_bat.index:
        opp_team_metrics = df_bat.loc[opp_team_name]
        
    opp_team = pd.DataFrame(opp_team_metrics)
    opp_team = opp_team.transpose()
    opp_team = opp_team[["BatAge", "R/G", "PA", "AB", "H", "2B", "3B", "HR", "BB", "SO", "BA", "OBP", "SLG", "OPS", "TB", "HBP", "LOB"]]
    opp_team["key"] = 1

    if starting_pitcher in team_rooster.index:
        team_name = team_rooster.loc[opposing_pitcher]["Team Name"]
    
    if team_name in df_bat.index:
        team = df_bat.loc[team_name]
        
    team = pd.DataFrame(team)
    team = team.transpose()
    team = team[["BatAge", "R/G", "PA", "AB", "H", "2B", "3B", "HR", "BB", "SO", "BA", "OBP", "SLG", "OPS", "TB", "HBP", "LOB"]]
    team.rename(columns = {
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
    team["key"] = 1    
    
    
    # gathering distance between teams
    distance = get_home_away_distance_in_miles(team_name, opp_team_name)
    
    if home_or_away == "Away":
        team["Distance"] = distance
    else:
        team["Distance"] = (distance * -1)
    
        
    # creating a dataframe to combine all the pitching metrics    
    pitching_metrics = pd.DataFrame(
    {     
        "ERA-Starting" : start_pitch_class,
        "ERA-Opposing" : opp_pitch_class,
        "CG-Starting" : start_pitch_class_2,
        "CG-Opposing" : opp_pitch_class_2,
        "IP-Starting" : start_pitch_class_3,
        "IP-Opposing" : opp_pitch_class_3,
        "ERA+-Starting" : start_pitch_class_4,
        "ERA+-Opposing" : opp_pitch_class_4,
        "FIP-Starting" : start_pitch_class_5,
        "FIP-Opposing" : opp_pitch_class_5,
        "WHIP-Starting" : start_pitch_class_6,
        "WHIP-Opposing" : opp_pitch_class_6,
        "H9-Starting" : start_pitch_class_7,
        "H9-Opposing" : opp_pitch_class_7,
        "HR9-Starting" : start_pitch_class_8,
        "HR9-Opposing" : opp_pitch_class_8,
        "BB9-Starting" : start_pitch_class_9,
        "BB9-Opposing" : opp_pitch_class_9,
        "SO9-Starting" : start_pitch_class_10,
        "SO9-Opposing" : opp_pitch_class_10,
        "SO/W-Starting" : start_pitch_class_11,
        "SO/W-Opposing" : opp_pitch_class_10,
        "key" : 1
    })
    
    
    # creating test data to run through model
    batting_metrics = pd.merge(team, opp_team, on='key')
    test_data = pd.merge(batting_metrics, pitching_metrics, on="key")
    test_data.drop(["key"], axis=1, inplace = True)
    
    # testing to see what the results look like before running a model
    # it works, I can comment this out
    # result = test_data
    
    # running our model
    result = model.predict(test_data)
    
    #printing out our prediction
    return result