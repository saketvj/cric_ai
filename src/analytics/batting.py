from config.constants import DB_PATH, RAW_DATA_PATH
import numpy as np
import sqlite3
import pandas as pd
from pipeline.load_features import load_deliveries

deliveries = load_deliveries()


# print(deliveries.columns)
# most runs 

# best strike rate 
# best boundary percentage 
# best average


def get_top_batsmen(
    df,
    years,
    phase=None,
    top_n=10,
    min_balls=100
):

    if years:
        df = df[
            df['match_date'].dt.year.isin(years)
        ]
  

    if phase:
        df = df[df['phase'] == phase]

    df = (
        df.groupby('batsman')
        .agg(
            total_runs=('batsman_runs', 'sum'),
            balls_faced=('batsman_ball_faced', 'sum')
        )
        .reset_index()
    )

    df = df[
        df['balls_faced'] >= min_balls
    ]

    return (
        df.sort_values(
            'total_runs',
            ascending=False
        )
        .head(top_n)
    )

def get_best_strike_rate_batsmen(df, years, phase=None, top_n=10, min_balls=100):
    
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:
        df = df[df['phase'] == phase]
    df = (
        df.groupby('batsman')
        .agg(
            total_runs=('batsman_runs', 'sum'),
            balls_faced=('batsman_ball_faced', 'sum')
        )
        .reset_index()
    )
    df = df[df['balls_faced'] >= min_balls]
    df['strike_rate'] = (df['total_runs'] / df['balls_faced'] * 100).round(2)
    return df.sort_values('strike_rate', ascending=False).head(top_n)


def get_best_boundary_batsmen(df, years, phase=None, top_n=10, min_balls=100):
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:
        df = df[df['phase'] == phase]
    df = (
        df.groupby('batsman')
        .agg(
            total_boundaries=('is_boundary', 'sum'),
            balls_faced=('batsman_ball_faced', 'sum')
        )
        .reset_index()
    )
    df = df[df['balls_faced'] >= min_balls]
    df['boundary_pct'] = (df['total_boundaries'] / df['balls_faced'] * 100).round(2)
    return df.sort_values('boundary_pct', ascending=False).head(top_n)


def get_best_average_batsmen(df, years, phase=None, top_n=10, min_balls=100):
    
    if years:
        df = df[df['match_date'].dt.year.isin(years)]
    if phase:
        df = df[df['phase'] == phase]
    df = (
        df.groupby('batsman')
        .agg(
            total_runs=('batsman_runs', 'sum'),
            balls_faced=('batsman_ball_faced', 'sum'),
            dismissals=('wicket', 'sum')                  # counts times batsman got out
        )
        .reset_index()
    )
    df = df[df['balls_faced'] >= min_balls]
    df['average'] = (df['total_runs'] / df['dismissals'].replace(0, 1)).round(2)  # avoid division by zero
    return df.sort_values('average', ascending=False).head(top_n)


