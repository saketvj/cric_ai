import numpy as np
import sqlite3
import pandas as pd

def get_phase(over):
    over_num = int(over)+1
    if over_num <= 6:
        return 'powerplay'
    elif over_num <= 15:
        return 'middle'
    else:
        return 'death'


def add_phase(df):
    df['phase'] = df['over'].apply(get_phase)
    return df


def add_boundary_flag(df):

    df['is_boundary'] = df['batsman_runs'].apply(
        lambda x: 1 if x in [4, 6] else 0
    )

    return df


def add_dot_ball_flag(df):

    df['is_dot_ball'] = df['total_runs'].apply(
        lambda x: 1 if x == 0 else 0
    )

    return df



def add_legal_ball_flag(df):

    df['is_legal_ball'] = df['extra_type'].apply(
        lambda x: 0 if ('wides' in x or 'noballs' in x) else 1
    )

    return df


def add_batsman_ball_faced(df):

    df['batsman_ball_faced'] = df['extra_type'].apply(
        lambda x: 0 if 'wides' in x else 1
    )

    return df



def add_bowler_wicket_flag(df):

    bowler_wickets = [
        'bowled',
        'caught',
        'lbw',
        'stumped',
        'caught and bowled',
        'hit wicket'
    ]

    df['is_bowler_wicket'] = df['wicket_kind'].apply(
        lambda x: 1 if x in bowler_wickets else 0
    )

    return df


def add_cumulative_features(df):

    # cumulative runs scored in innings
    df['cumulative_runs'] = (
        df.groupby(['match_id', 'innings'])['total_runs']
        .transform('cumsum')
    )

    # cumulative wickets fallen
    df['cumulative_wickets'] = (
        df.groupby(['match_id', 'innings'])['wicket']
        .transform('cumsum')
    )

    # cumulative legal balls bowled
    df['cumulative_legal_balls'] = (
        df.groupby(['match_id', 'innings'])['is_legal_ball']
        .transform('cumsum')
    )

    return df



def add_target(df):

    # 🔹 Get first innings total for every match
    first_innings_score = (
        df[df['innings'] == '1st innings']
        .groupby('match_id')['total_runs']
        .sum()
        .reset_index()
    )

    # 🔹 Target = first innings score + 1
    first_innings_score['target'] = (
        first_innings_score['total_runs'] + 1
    )

    # 🔹 Keep only required columns
    target_df = first_innings_score[['match_id', 'target']]

    # 🔹 Merge target into ball dataframe
    df = df.merge(target_df, on='match_id', how='left')

    # 🔹 Keep target only for second innings
    df['target'] = np.where(
        df['innings'] == '2nd innings',
        df['target'],
        np.nan
    )

    return df

def add_balls_remaining(df):

    df['balls_remaining'] = (
        120 - df['cumulative_legal_balls']
    )

    return df

def add_wickets_remaining(df):

    df['wickets_remaining'] = (
        10 - df['cumulative_wickets']
    )

    return df



def add_runs_required(df):

    df['runs_required'] = np.where(
        df['innings'] == '2nd innings',
        df['target'] - df['cumulative_runs'],
        np.nan
    )

    return df


def add_current_run_rate(df):

    df['current_run_rate'] = np.where(
        df['cumulative_legal_balls'] > 0,
        (df['cumulative_runs'] * 6)
        / df['cumulative_legal_balls'],
        0
    )

    return df

def add_required_run_rate(df):

    df['required_run_rate'] = np.where(
        (df['innings'] == '2nd innings')
        & (df['balls_remaining'] > 0),

        (df['runs_required'] * 6)
        / df['balls_remaining'],

        np.nan
    )

    return df



def apply_features(df):

    df = add_phase(df)

    df = add_boundary_flag(df)

    df = add_dot_ball_flag(df)

    df = add_legal_ball_flag(df)

    df = add_batsman_ball_faced(df)

    df = add_bowler_wicket_flag(df)

    df = add_cumulative_features(df)

    df = add_target(df)

    df = add_balls_remaining(df)

    df = add_wickets_remaining(df)

    df = add_runs_required(df)

    df = add_current_run_rate(df)

    df = add_required_run_rate(df)

    return df



