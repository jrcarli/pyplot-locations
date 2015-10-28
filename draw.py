import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def getColors():
    """ Snagged from colorbrewer2.org
    7 data classes
    diverging colors
    right-most scheme
    """
    colors = ['#d53e4f',
              '#fc8d59',
              '#fee08b',
              '#ffffbf',
              '#e6f598',
              '#99d594',
              '#3288bd',
             ]
    return colors

def team2val(x):
    if x=='B':
        return 0
    else:
        return 1

def loc2val(x):
    """
    array(['Not Sched', 'Tel', 'Loc A', 'Other', 'Loc B', 'Loc C', 'Vaca'], dtype=object)
    """
    if x=='Not Sched':
        return 0
    elif x=='Tel':
        return 1
    elif x=='Loc A':
        return 2
    elif x=='Loc B':
        return 3
    elif x=='Loc C':
        return 4
    elif x=='Vaca':
        return 5
    else:
        return 6

label_size = 10

df = pd.read_csv('locations.csv')
df2 = pd.melt(df, id_vars=['Person','Team'], value_vars=['Day1','Day2','Day3','Day4','Day5','Day6','Day7'],var_name='Day',value_name='Location')

df2['Site'] = df2['Location'].apply(loc2val)
df2['TeamMap'] = df2['Team'].apply(team2val)

# Figure out how many dots may appear in one x bin
max_people_per_bin = pd.groupby(df2,['Team','Location']).count()['Site'].max()

# Figure out how many teams
num_teams = len(df2['Team'].unique())
num_locations = len(df2['Location'].unique())

teams = df2['Team'].unique()

# Complete for all days. Consider loop based on 'Day'.unique()
day1 = df2[df2['Day']=='Day1']
day3 = df2[df2['Day']=='Day3']

colors = getColors()

"""
# Generate some simple plotting data
# For loop to cover each location
for i in range(0,num_locations):
    # For loop to cover each team
    for j in range(0,num_teams):
        # x is i + 0.5
        # y is j + 0.5
        plt.scatter(x=(i+0.5),y=(j+0.5),alpha=0.2)
"""

X = day3['Site'].values + 0.5
Y = day3['TeamMap'].values + 0.5
day3_team_values = day3['Team'].values
day3_site_values = day3['Site'].values
s = []
for i in range(0,len(X)):
    size = len(day3[(day3['Team']==day3_team_values[i]) & (day3['Site']==day3_site_values[i])])
    s.append(size)
#s = [20*4**n for n in range(len(x))]
t = [20*4**x for x in s]
plt.scatter(X,Y,s=t,alpha=0.5)

# Fill in the background
# TODO: colors is conveniently sized to match data, should expand
for i in range(0,num_locations):
    xgap = [i,i+1]
    plt.fill_between(x=xgap, y1=num_teams, y2=0, color=colors[i], alpha=0.2) 

# Consider setting the color or alpha here
for i in range(0,num_teams-1): # don't bother with top line
    plt.axhline(y=i+1,alpha=0.2)

# Make sure to use the full df not day-specific
#loc_labels = df2['Location'].unique()
loc_labels=['Off',
            'Tel',
            'Loc A',
            'Loc B',
            'Loc C',
            'Vacation',
            'Other',
           ]
plt.xticks(np.arange(len(loc_labels))+0.5,loc_labels)#,rotation=45)

team_labels=df2['Team'].unique()
plt.yticks(np.arange(len(team_labels))+0.5,team_labels)

ax = plt.gca()
ax.set_autoscale_on(False)
ax.invert_yaxis()
ax.xaxis.tick_top()

plt.tick_params(labelsize=10)
plt.tick_params(axis='x',top='off')
plt.tick_params(axis='y',left='off')
plt.tick_params(axis='y',right='off')

plt.xlim(0,num_locations)
plt.ylim(0,num_teams)

plt.show()

