from config.constants import DB_PATH, RAW_DATA_PATH
import numpy as np
import sqlite3
import pandas as pd
from pipeline.load_features import load_deliveries

deliveries = load_deliveries()
# print(deliveries.head())


def get_top_bowlers(df, years, phase=None, top_n=10, min_overs=6):
    # top_n = int(top_n)
    if years:                                        # ← only filter if years provided
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:                                         # filter by phase if provided
        df = df[df['phase'] == phase]
    df = df.groupby('bowler')['is_bowler_wicket'].sum().reset_index(name='total_wickets')
    df = df.sort_values('total_wickets', ascending=False)
    return df.head(top_n)

def get_top_economical_bowlers(df, years, phase=None, top_n=10, min_overs=10):
    # top_n = int(top_n)
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:
        df = df[df['phase'] == phase]
    df = df[df['is_legal_ball'] == 1]
    df = df.groupby('bowler').agg(
        total_runs=('total_runs', 'sum'),
        total_balls=('is_legal_ball', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]
    df['economy'] = (df['total_runs'] / df['total_balls'] * 6).round(2)
    df = df.sort_values('economy', ascending=True)
    return df.head(top_n)

def get_top_dot_ball_bowlers(df, years, phase=None, top_n=10, min_overs=10):
    # top_n = int(top_n)
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:
        df = df[df['phase'] == phase]
    df = df[df['is_legal_ball'] == 1]
    df = df.groupby('bowler').agg(
        total_dot_balls=('is_dot_ball', 'sum'),
        total_balls=('is_legal_ball', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]
    df['dot_ball_pct'] = (df['total_dot_balls'] / df['total_balls'] * 100).round(2)
    df = df.sort_values('dot_ball_pct', ascending=False)
    return df.head(top_n)

def get_best_phasewise_bowlers(df, years, phase=None, top_n=10, min_overs=6):
    # top_n = int(top_n)
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    df = df[df['is_legal_ball'] == 1]
    df = df.groupby(['phase', 'bowler']).agg(
        total_runs=('total_runs', 'sum'),
        total_balls=('is_legal_ball', 'sum'),
        total_wickets=('is_bowler_wicket', 'sum')
    ).reset_index()
    df = df[df['total_balls'] >= min_overs * 6]
    df['economy'] = (df['total_runs'] / df['total_balls'] * 6).round(2)
    powerplay = df[df['phase'] == 'powerplay'].sort_values('total_wickets', ascending=False).head(top_n)
    middle    = df[df['phase'] == 'middle'].sort_values('total_wickets', ascending=False).head(top_n)
    death     = df[df['phase'] == 'death'].sort_values('economy', ascending=True).head(top_n)
    return pd.concat([powerplay, middle, death]).reset_index(drop=True)