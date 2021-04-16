import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
import requests
import pickle
import math
import re

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

base_url = 'https://www.teamrankings.com/mlb/stat/run-differential?date='

# Create list of dates to be used
season_start = pd.datetime(2016, 4, 3)
season_end = pd.datetime(2016, 10, 3)

date_index = pd.date_range(season_start, season_end)

# Remove the time from each date
dates = []
for date in date_index:
    dt = str(date).split(' ')
    dates.append(dt[0])

def get_dates(year, start_month, start_date, end_month, end_date):

    # Create list of dates to be used
    start = pd.datetime(year, start_month, start_date)
    end = pd.datetime(year, end_month, end_date)

    index = pd.date_range(start, end)

    # Remove the time from each date
    dates = []
    for date in date_index:
        dt = str(date).split(' ')
        dates.append(dt[0])

    return dates

season2016_dates = get_dates(2016, 4, 3, 10, 3)

# Grab HTML from webpage
html = requests.get(base_url+dates[3]).content

#Parse HTML
new_soup = BeautifulSoup(html, 'lxml')

# Grab the tables
tables = new_soup.find_all('table')

print('Document contains {0} HTML Table(s).'.format(len(tables)))

# Get the column names for the
columns = []
for row in tables[0].thead.tr.find_all('th'):
    val = row.contents[0].strip()
    columns.append(val)
print(columns)

tb = tables[0].tbody.find_all('tr')

li = {}
for row in tb:
    tdx = [val for val in row.find_all('td')]
    rd = tdx[2].contents[0].strip()
    team = tdx[1].a.contents[0].strip()
    li[team] = [dates[3], rd]

def get_run_diff(dates):

    lis = []
    for i in range(len(dates)):
        # Grab HTML from webpage
        html = requests.get(base_url+dates[i]).content

        #Parse HTML
        new_soup = BeautifulSoup(html, 'lxml')

        # Grab the tables
        tables = new_soup.find_all('table')

        tb = tables[0].tbody.find_all('tr')

        li = {}
        for row in tb:
            tdx = [val for val in row.find_all('td')]
            rd = tdx[2].contents[0].strip()
            team = tdx[1].a.contents[0].strip()
            li[team] = [dates[i], rd]

        lis.append(li)

    return lis

ZOLG = get_run_diff(season2016_dates)
# Get unique team names
team_names = []
for d in ZOLG:
    for name in d.keys():
        if name not in team_names:
            team_names.append(name)

def get_team_RD(team, dd):
    '''
    Parameters
    -----------
    team: A str. The name of the team you wish to analyze
    dd: A list of dictionaries

    Returns
    ---------
    df: A pandas.DataFrame
    '''
    dates = []
    rds = []
    for d in dd:
        if team in d:
            val = d[team]
            dates.append(val[0])
            if val[1] == '--':
                rds.append(0.0)
            else:
                rds.append(val[1])

    # Build dataframe
    df = pd.DataFrame()

    df['Date'] = dates
    # Change to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Change to float values
    df['Run Differential'] = rds
    df['Run Differential'] = df['Run Differential'].astype('float')

    # Set dates as indices
    df.set_index('Date', inplace=True)

    return df

rd_df = pd.concat([td])
ARI = get_team_RD('Chi Cubs', ZOLG)

def plot_RD(df):

    fig,ax = plt.subplots()

    ax.plot(df)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))
    ax.set_xlabel('Month')
    ax.set_ylabel('Run Differential')

    return ax

ax = plot_RD(ARI)

plt.show()
