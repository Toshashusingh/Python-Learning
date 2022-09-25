#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[61]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def cl_nhl_df(): 
    # YOUR CODE HERE
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities['Metropolitan area']=cities['Metropolitan area'].apply(lambda x: x.strip())

    cities=cities.replace(to_replace ='\[\w* \d*\]', value ='', regex = True)
    cities=cities.replace(to_replace ='\s*(?=\w*)', value ='', regex = True)
    cities["NHL"] = cities["NHL"].replace({"RangersIslandersDevils": "Rangers,Islanders,Devils","KingsDucks": "Kings,Ducks",
                                           "RedWings": "Red,Wings", 
                                           "MapleLeafs": "Maple,Leafs", 
                                           "BlueJackets": "Blue,Jackets",
                                           "GoldenKnights": "Golden,Knights" })
    cities["NHL"] = cities["NHL"].apply(lambda x: x.split(","))
    cities = cities.explode("NHL")



    NHL=pd.read_csv('assets/nhl.csv')
    NHL=NHL[NHL['year']==2018]


    NHL['team_name']=NHL['team'].apply(lambda x: x.rsplit(' ',1)[1]).apply(lambda x: x.replace('*',''))
    final=pd.merge(cities,NHL,left_on='NHL', right_on='team_name')
    final=final[['Metropolitan area','Population (2016 est.)[8]','NHL','team_name','W','L']]
    final['Population (2016 est.)[8]']=final['Population (2016 est.)[8]'].astype(float)
    final['W/L%']=final['W'].astype(int)/(final['W'].astype(int)+final['L'].astype(int))
    final.set_index('Metropolitan area')
    a=final.groupby(['Metropolitan area','Population (2016 est.)[8]'],sort=False).mean().reset_index()
     # pass in metropolitan area population from cities
    return a


def nhl_correlation():
    a=cl_nhl_df()
    
    population_by_region = a['Population (2016 est.)[8]'] # pass in metropolitan area population from cities
    win_loss_by_region = a['W/L%'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[62]:


nhl_correlation()


# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[63]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def cl_nba_df():
    # YOUR CODE HERE
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities['Metropolitan area']=cities['Metropolitan area'].apply(lambda x: x.strip())

    cities=cities.replace(to_replace ='\[\w* \d*\]', value ='', regex = True)
    cities=cities.replace(to_replace ='\s*(?=\w*)', value ='', regex = True)
    cities["NBA"] = cities["NBA"].replace({"KnicksNets": "Knicks,Nets",
                                           "LakersClippers": "Lakers,Clippers",
                                           "TrailBlazers": "Trail,Blazers"})
    cities["NBA"] = cities["NBA"].apply(lambda x: x.split(","))
    cities = cities.explode("NBA")
    nba_df=nba_df[nba_df['year']==2018]
    nba_df=nba_df.replace(to_replace =('(\*)*\(\d*\s*\)*'), value ='', regex = True)
    nba_df['team_name']=nba_df['team'].apply(lambda x: x.rsplit(' ',1)[1]).apply(lambda x: x.replace('*','')).apply(lambda x: x.strip())

    final= pd.merge(cities,nba_df,left_on='NBA',right_on='team_name')
    final['W-L%']=final['W'].astype(int)/(final['W'].astype(int)+final['L'].astype(int))
    final= final[["Metropolitan area", "Population (2016 est.)[8]", "NBA", 'team_name', "W", "L", "W-L%"]]
    
    final["W-L%"] = final["W-L%"].astype("float")
    final['Population (2016 est.)[8]']=final['Population (2016 est.)[8]'].astype(float)
    a=final.groupby(['Metropolitan area','Population (2016 est.)[8]'],sort=False).mean().reset_index()
    return a
    

def nba_correlation():
    a=cl_nba_df()
    
    population_by_region =a['Population (2016 est.)[8]'] # pass in metropolitan area population from cities
    win_loss_by_region =a['W-L%'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[64]:


nba_correlation()


# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[65]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
def cl_mlb_df():
    # YOUR CODE HERE
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities=cities.replace(to_replace ='\[\w* \d*\]', value ='', regex = True)
    cities=cities.replace(to_replace ='\s*(?=\w*)', value ='', regex = True)
    cities["MLB"] = cities["MLB"].replace({"BlueJays": "Blue,Jays", 
                                           "CubsWhiteSox": "Cubs,White,Sox", 
                                           "DodgersAngels": "Dodgers,Angels", 
                                           "GiantsAthletics": "Giants,Athletics", 
                                           "YankeesMets": "Yankees,Mets",
                                           "RedSox": "RedSox"})
    
    cities["MLB"] = cities["MLB"].apply(lambda x: x.split(","))
    cities = cities.explode("MLB")
    
    mlb_df=mlb_df[mlb_df['year']==2018]
    mlb_df['team']=mlb_df['team'].replace({"Boston Red Sox": "Boston RedSox"})   
    
    mlb_df['team_name']=mlb_df['team'].apply(lambda x: x.rsplit(' ',1)[1]).apply(lambda x: x.replace('*','')).apply(lambda x: x.strip())
    final= pd.merge(cities,mlb_df,left_on='MLB',right_on='team_name')
    final['W-L%']=final['W'].astype(int)/(final['W'].astype(int)+final['L'].astype(int))
    final= final[["Metropolitan area", "Population (2016 est.)[8]", "MLB", 'team_name', "W", "L", "W-L%"]]
    
    final["W-L%"] = final["W-L%"].astype("float")
    final['Population (2016 est.)[8]']=final['Population (2016 est.)[8]'].astype(float)
    b=final.groupby(['Metropolitan area','Population (2016 est.)[8]'],sort=False)['W-L%'].mean().reset_index()
    return b
    
def mlb_correlation():
    
    b=cl_mlb_df()
    population_by_region =b['Population (2016 est.)[8]'] # pass in metropolitan area population from cities
    win_loss_by_region =b['W-L%']  # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[66]:


mlb_correlation()


# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[67]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
def cl_nfl_df():
    # YOUR CODE HERE
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    cities['Metropolitan area']=cities['Metropolitan area'].apply(lambda x: x.strip())

    cities=cities.replace(to_replace ='\[\w* \d*\]', value ='', regex = True)
    cities=cities.replace(to_replace ='\s*(?=\w*)', value ='', regex = True)
    cities["NFL"] = cities["NFL"].replace({"GiantsJets": "Giants,Jets",
                                           "RamsChargers": "Rams,Chargers",
                                           "49ersRaiders": "49ers,Raiders"
                                           })
    cities["NFL"] = cities["NFL"].apply(lambda x: x.split(","))
    cities = cities.explode("NFL")
    nfl_df=nfl_df[nfl_df['year']==2018]
    nfl_df["team"] = nfl_df["team"].apply(lambda x: re.sub(r"(\*|\+)", "", x))
    nfl_df['team_name']= nfl_df['team'].apply(lambda x: x.rsplit(' ',1)[1])
    final= pd.merge(cities,nfl_df,left_on='NFL',right_on='team_name')
    final['W-L%']=final['W'].astype(int)/(final['W'].astype(int)+final['L'].astype(int))
    final= final[["Metropolitan area", "Population (2016 est.)[8]", "NFL", 'team_name', "W", "L", "W-L%"]]
    
    final["W-L%"] = final["W-L%"].astype("float")
    final['Population (2016 est.)[8]']=final['Population (2016 est.)[8]'].astype(float)
    a=final.groupby(['Metropolitan area','Population (2016 est.)[8]'],sort=False).mean().reset_index()
    return a
    
def nfl_correlation():
    a=cl_nfl_df()
    population_by_region =a['Population (2016 est.)[8]'] # pass in metropolitan area population from cities
    win_loss_by_region =a['W-L%']  # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[68]:


nfl_correlation()


# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[72]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

  


def sports_team_performance():
    # YOUR CODE HERE
    nfl_df=cl_nfl_df()
    nba_df=cl_nba_df()
    nhl_df=cl_nhl_df()
    mlb_df=cl_mlb_df()
    nfl_df = nfl_df[["Metropolitan area", "W-L%"]]
    nba_df = nba_df[["Metropolitan area", "W-L%"]]
    nhl_df = nhl_df[["Metropolitan area", "W/L%"]]  
    mlb_df = mlb_df[["Metropolitan area", "W-L%"]]
    df=pd.merge(nfl_df,nba_df,on='Metropolitan area',how='outer')
    df=pd.merge(df,nhl_df,on='Metropolitan area',how='outer')
    df=pd.merge(df,mlb_df,on='Metropolitan area',how='outer')
    df=df.set_index('Metropolitan area')
    a=[]
    for i in df.columns:
    
        b=[]
        for y in df.columns:
            b.append(stats.ttest_rel(df[i],df[y],nan_policy='omit')[1])
        
        
    a.append(b)   
    

    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame(a,columns=sports, index=sports)
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    
    
    return p_values


# In[ ]:





# In[73]:


sports_team_performance()


# In[74]:


nfl_df=cl_nfl_df()
nba_df=cl_nba_df()
nhl_df=cl_nhl_df()
mlb_df=cl_mlb_df()
nfl_df = nfl_df[["Metropolitan area", "W-L%"]]
nba_df = nba_df[["Metropolitan area", "W-L%"]]
nhl_df = nhl_df[["Metropolitan area", "W/L%"]]  
mlb_df = mlb_df[["Metropolitan area", "W-L%"]]
df=pd.merge(nfl_df,nba_df,on='Metropolitan area',how='outer')
df=pd.merge(df,nhl_df,on='Metropolitan area',how='outer')
df=pd.merge(df,mlb_df,on='Metropolitan area',how='outer')
df=df.set_index('Metropolitan area')
a=[]
for i in df.columns:
    
    b=[]
    for y in df.columns:
        
        
        b.append(stats.ttest_rel(df[i],df[y],nan_policy='omit')[1])
        
        
    a.append(b)   
a
sports = ['NFL', 'NBA', 'NHL', 'MLB']
p_values = pd.DataFrame(a,columns=sports, index=sports)
p_values


# In[ ]:





# In[ ]:




