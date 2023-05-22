#!/usr/bin/env python
# coding: utf-8

# # IPL DATA ANALYSIS

# The Indian Premier League (IPL) is an Indian professional Twenty20 (T20) cricket league established in 2008. The league is based on a round-robin group and knockout format and has teams in major Indian cities.

# ### Import the required libraries
# 

# In[66]:


import pandas as pd
import numpy as nd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# #### import data

# In[67]:


#read the file
match=pd.read_csv("C:\Desktop\Data Analyst Project\ipl cricket power bi\match.csv")


# #### show data table

# In[68]:


#view data
match.head()


# #### import second library

# In[69]:


delivery =pd.read_csv("C:\Desktop\Data Analyst Project\ipl cricket power bi\delivery.csv")


# ### show data table

# In[70]:


delivery.head()


# In[71]:


# to view all the columns data types and check if there null values
match.info()


# Based on the above data the following observation can be made:
# 1.This dataset contains 18 columns and 816 rows .
# 
# 2.some columns contain null values as well further analysis can be performed by examining each column and taking necessary steps to perform the analysis.
# 
# 3.Additionaly insights can be derived by investigating each column,which may provide useful information about IPL Data Analysis

# In[72]:


match.describe()


# In[73]:


#no of rows and columns in first dataset
match.shape


# In[74]:


#columns in first dataset
match.columns


# In[75]:


delivery.info()


# In[76]:


delivery.describe()


# In[77]:


delivery.columns


# In[78]:


delivery.shape


# ### How many teams are there?

# #### List to all the participant teams in ipl

# In[79]:


Teams= match['team1'].tolist() + match['team2'].tolist()


# In[80]:


Teams = list(set(Teams))
Teams


# # Number of matches played  per venues?

# In[81]:


match['venue'].value_counts()


# In[82]:


plt.figure(figsize=(6,10))
ax=sns.countplot(y='venue',data=match)
for bars in ax.containers:
    ax.bar_label(bars)
plt.xticks(rotation='vertical')


# as we can see here highest number of matches played in Eden Garden  77,Feroz Shah Kotla  74, Wankhede Stadium 73 respectively

# ### Number of matches played by each team in ipl

# In[83]:


match['team1'].value_counts()


# In[84]:


match['team2'].value_counts()


# In[85]:


plt.figure(figsize=(5,9))
x=match['team1'].value_counts()
y=match['team2'].value_counts()
ax=(x+y).plot(kind='barh',color='blue') #barh means horizontal bar graph
for bars in ax.containers:
    ax.bar_label(bars)


# RCB and MI played highest number of matches in ipl

# ### matches won by each team

# In[86]:


x = pd.DataFrame({'Winner':match['winner']}).value_counts()
print(x)


# In[87]:


ax=sns.countplot('winner',data=match)
plt.xticks(rotation='vertical')
for bars in ax.containers:
    ax.bar_label(bars)


# In[88]:


#columns in second dataset
delivery.columns


# # Top 5 best performer in ipl( man of the match)

# In[89]:


M_match=match['man_of_match'].value_counts().head()
print(M_match)
ax=sns.barplot(x=M_match.index ,y=M_match.values, data=match)
plt.title("top 5 match")
plt.xticks(rotation=90)
plt.xlabel("player")
for bars in ax.containers:
    ax.bar_label(bars)
plt.ylabel("match count")
plt.show()


# AB de Villiers is a batsman who performed very well in 23 matches  and chriss gayle on 22 matches 

# # Players with highest number of runs

# In[90]:


#use group by in batsman ans aggregate runs
top_batsman= delivery.groupby('batsman')['batsman_runs'].agg('sum').reset_index().sort_values('batsman_runs',ascending=False).head(10)


# In[91]:


top_batsman


# In[92]:


ax=sns.barplot(y='batsman', x='batsman_runs',data=top_batsman)
for bars in ax.containers:
    ax.bar_label(bars)
plt.title('Top 10 Batsman in ipl')


# in the whole ipl season in batting  virat kohli made 5878 runs,5368 runs and DA Warner 5254  respectively  

# # Runs given by Bowlers in ipl

# In[93]:


bowlers=delivery.groupby('bowler')['total_runs'].agg('sum').reset_index().sort_values('total_runs',ascending=False).head(10)
bowlers


# In[94]:


ax=delivery.groupby('bowler').agg({'total_runs':'sum','dismissal_kind':'count'}).reset_index()
bx=ax.sort_values('total_runs', ascending=False).head(10)
ex=sns.barplot(y='bowler',x='total_runs',data=bx) 
for bars in ex.containers:
    ex.bar_label(bars)


# In[95]:


delivery.groupby('bowler')['is_wicket'].agg('sum').head(10)


# In[96]:


wkt =delivery.groupby('bowler')['is_wicket'].agg('sum').reset_index().sort_values('is_wicket',ascending=False).head(15) 
wkt
#wicket taken by bowlers


# In[97]:


wkt.set_index('bowler', inplace=True)
ax=wkt.plot(kind='bar')
for bars in ax.containers:
    ax.bar_label(bars)


# from the above graph SL Malinga has taken 188 wicket, DJ bravo 175 and Amit Mishra 169 while if we talk aboutt given runs PP chawla has given 4330 runs and took 164 wickets. while SL malinga has given 3486 runs

# # now If we  talk about A single player

# #### runs given by SL Malinga  against teams in ipl

# In[98]:


bowl=delivery['bowler']=='SL Malinga'
delivery[bowl].groupby('batting_team')['total_runs'].agg('sum')


# In[99]:


bowl=delivery['bowler']=='SL Malinga'
ax=delivery[bowl].groupby('batting_team')['total_runs'].agg('sum').plot(kind='bar',color='green')
for bars in ax.containers:
    ax.bar_label(bars)


# from the above graph ,as we can see hare SL Malinga has given highest run against chennai super kings ,Deccan Chargers and delhi capitals

# In[106]:


bowl=delivery['bowler']=='SL Malinga'
delivery[bowl].groupby('batting_team')['is_wicket'].agg('sum')


# In[165]:


delivery[bowl].groupby('bowling_team')['is_wicket'].agg('sum').plot(kind='pie') 


# SL malinga has taken highest wickets 30 against channai super kings on ipl

# # Runs given by harbhajan singh in different over  against teams 

# In[128]:


bowl=delivery['bowler']=='Harbhajan Singh'


# In[129]:


delivery1=delivery[bowl]
delivery1=delivery1[['batting_team','over','batsman_runs']]

x = delivery1.pivot_table(values='batsman_runs',index='batting_team',columns='over',aggfunc='count')
sns.heatmap(x,cmap='summer')


# if we observe the heat map closely ,we can easilyb identify it shows over_wise of all the teams in which royal challengers banglore 
# and rajasthan royals have good opener and finisher as well 
# that's the reason this are the best ipl team
# and same goes with kkr as well ,after ther first 4 overs they performed really well
# if your opponents are Rajasthan royal ,royal challengers and kolkata knight rider you have to come with full bowling preparation
# kkr has good batsman but they lack in last over as per heat map.

# if we talk about mumbai indians ,sunrise hydrabad,king eleven punjab they have good middle order batsman

# # total of dismissal kind 

# In[130]:


# top dismissal kind
ax=sns.countplot('dismissal_kind',data=delivery)
plt.xticks(rotation=90)
for bars in ax.containers:
    ax.bar_label(bars)


# # Top Bowlers

# In[135]:


bowl1=delivery['dismissal_kind']=='caught'
bowl2=delivery['dismissal_kind']=='bowled'
bowl3=delivery['dismissal_kind']=='ibw'
bowl4=delivery['dismissal_kind']=='caught and bowled'
bowl5=delivery['dismissal_kind']=='stumped'
new_ses=delivery[bowl1| bowl2|bowl3|bowl4|bowl5]
new_ses.groupby('bowler')['player_dismissed'].agg('count').sort_values(ascending=False).head(15)


# In[136]:


#top 15 bowlers
bowl1=delivery['dismissal_kind']=='caught'
bowl2=delivery['dismissal_kind']=='bowled'
bowl3=delivery['dismissal_kind']=='ibw'
bowl4=delivery['dismissal_kind']=='caught and bowled'
bowl5=delivery['dismissal_kind']=='stumped'
new_ses=delivery[bowl1| bowl2|bowl3|bowl4|bowl5]
ax=new_ses.groupby('bowler')['player_dismissed'].agg('count').sort_values(ascending=False).head(15).plot(kind='bar')
for bars in ax.containers:
    ax.bar_label(bars)


# ### Run scored by Raina against A mishra?

# In[141]:


bowl=delivery['bowler']=='A Mishra'
bat2=delivery['batsman']=='SK Raina'
delivery[bowl].groupby('batsman')['batsman_runs'].agg('count').sort_values(ascending=False)['SK Raina']


# ### Number of sixes by players

# In[138]:


boundary6 =delivery.groupby('batsman')['batsman_runs'].agg(lambda x:(x==6).sum()).reset_index().sort_values(by='batsman_runs', ascending=False).head(10)
boundary6


# In[140]:


#graphical representation

ax=sns.barplot( x= boundary6['batsman'], y = boundary6['batsman_runs'], data=boundary6)
plt.title("No. of sixes by batsman")
plt.xlabel('batsman')
plt.xticks(rotation=90)
for bars in ax.containers:
    ax.bar_label(bars)
plt.show


# most of the sixes by chrish gayle 

# ### Number of fours by batsman.

# In[172]:


boundary4=delivery.groupby('batsman')['batsman_runs'].agg(lambda y:(y==4).sum()).reset_index().sort_values( by='batsman_runs', ascending=False).head(10)
boundary4


# In[173]:


px=sns.barplot(x=boundary4['batsman'] ,y=boundary4['batsman_runs'] ,data=boundary4)
plt.xlabel("batsman")
plt.ylabel("no.of fours")
plt.xticks(rotation=90)
for bars in px.containers:
    px.bar_label(bars)
plt.show


# most number of fours by Shikhar dhawan who made 591  four boundaries,and after him on second position david warner who made 510 four boundaries.
