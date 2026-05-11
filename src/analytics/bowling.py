from config.constants import DB_PATH, RAW_DATA_PATH
import numpy as np
import sqlite3
import pandas as pd
from pipeline.load_features import deliveries 

# print(deliveries.head())



def get_top_bowlers(df, years, top_n = 10,min_overs=6):
    
    df = df[df['match_date'].dt.year.isin(years)]
    df = df.groupby('bowler')['is_bowler_wicket'].sum().reset_index(name='total_wickets')
    df = df.sort_values('total_wickets', ascending=False)               # explicit column name
    df = df.head(top_n)
    return df

a = get_top_bowlers(deliveries,[2008,2009,2010,2011,2012],5)
# print(a)


def get_top_economical_bowlers(df, years, top_n=10, min_overs=10):
    df = df[df['match_date'].dt.year.isin(years)]
    df = df[df['is_legal_ball'] == 1]                                        # only legal balls
    df = df.groupby('bowler').agg(
        total_runs=('total_runs', 'sum'),
        total_balls=('is_legal_ball', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]                              # min overs filter to avoid outliers
    df['economy'] = (df['total_runs'] / df['total_balls'] * 6).round(2)
    df = df.sort_values('economy', ascending=True)                           # lower economy is better
    return df.head(top_n)


def get_top_dot_ball_bowlers(df, years, top_n=10, min_overs=10):
    df = df[df['match_date'].dt.year.isin(years)]
    df = df[df['is_legal_ball'] == 1]
    df = df.groupby('bowler').agg(
        total_dot_balls=('is_dot_ball', 'sum'),
        total_balls=('is_legal_ball', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]                              # min overs filter
    df['dot_ball_pct'] = (df['total_dot_balls'] / df['total_balls'] * 100).round(2)
    df = df.sort_values('dot_ball_pct', ascending=False)
    return df.head(top_n)


def get_best_phasewise_bowlers(df, years, top_n=10, min_overs=6):
    df = df[df['match_date'].dt.year.isin(years)]
    df = df[df['is_legal_ball'] == 1]
    df = df.groupby(['phase', 'bowler']).agg(
        total_runs=('total_runs', 'sum'),
        total_balls=('is_legal_ball', 'sum'),
        total_wickets=('is_bowler_wicket', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]
    df['economy'] = (df['total_runs'] / df['total_balls'] * 6).round(2)

    powerplay   = df[df['phase'] == 'powerplay'].sort_values('total_wickets', ascending=False).head(top_n)
    middle      = df[df['phase'] == 'middle'].sort_values('total_wickets', ascending=False).head(top_n)
    death       = df[df['phase'] == 'death'].sort_values('economy', ascending=True).head(top_n)

    df = pd.concat([powerplay, middle, death]).reset_index(drop=True)
    return df

# A = get_top_economical_bowlers(deliveries, [2025, 2023, 2024], top_n=10, min_overs=10)
# A = get_top_dot_ball_bowlers(deliveries, [2025, 2023, 2024], top_n=10, min_overs=10)
# print(deliveries['phase'].unique())
# A = get_best_phasewise_bowlers(deliveries, [2025, 2023, 2024], top_n=5, min_overs=10)

# print(A)