# Machine_Learning_MLB_Game_Predictions

![](Pictures/baseball_stadium.jpg)

## Key Findings

- For the games that we've been testing in the 2020 playoffs, we're currently 6-3. However we've correctly guess all Astros games. Since we trained our data on the Astros tendencies, we believe the model may be better suited to Astros games as opposed to other teams.

- 

- We realized the metrics that we had placed high importance on, the models did not.

## Hypothesis 

Using metrics we've identified below, we wanted to run them through various models to see if we can accurately predict which team would win. We created columns for each of the metrics for the home and away team, similiar to starting and opposing pitcher.

#### Pitching Metrics

- ERA, CG, IP, ERA+, FIP, WHIP, H9, HR9, BB9, SO9, SO/W

![](Pictures/pitching_df.png)

#### Batting Metrics

- BatAge, R/G, PA, AB, H, 2B, 3B, HR, BB, SO, BA, OBP, SLG, OPS, TB, HBP, LOB

![](Pictures/batting_df.png)

## Data Acquisition

We pulled data in from thebaseballcube.com and baseball-reference.com. Since we pulled in data from two different sources, each source had their own naming conventions for teams. We had to create a new dataframe with the team names along with their accroynms to be able to cross reference one another. We created [functions](Code/functions.py) to help clean up the data and reorganize into a way we can feed it into our models.

We pulled everyones pitching data along with team's average batting data for the years 2013 through 2019. For the records of win/loses we used the Astros. We pulled in their schedules from 2013 through 2019. We weren't able to pull in 2020 data as the season was still going, and it required a premium membership to pull it in. 

We also created a dictionary with all the locations of stadiums of the teams to create a new column in our dataframe which would hold distance. If the Astros were the home team, the distance would be negative, to reflect the other team having to travel. 

All the data can be found in the [Data](Data) folder.

## Models Used

We decided to test out the following six models. 

Model 1 

Model 2

Model 3

Model 4

Model 5

Model 6

## Predicted Games

[insert results]

