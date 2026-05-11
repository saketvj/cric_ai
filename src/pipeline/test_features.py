import pandas as pd
import numpy as np
from pipeline.feature import (
    get_phase, add_phase, add_boundary_flag, add_dot_ball_flag,
    add_legal_ball_flag, add_batsman_ball_faced, add_bowler_wicket_flag,
    add_cumulative_features, add_target, add_balls_remaining,
    add_wickets_remaining, add_runs_required, add_current_run_rate,
    add_required_run_rate, apply_features
)

def test_get_phase():
    """Test phase calculation"""
    assert get_phase(0.1) == 'powerplay'
    assert get_phase(5.6) == 'powerplay'
    assert get_phase(6.1) == 'middle'
    assert get_phase(14.5) == 'middle'
    assert get_phase(15.1) == 'death'
    assert get_phase(19.6) == 'death'
    print("✅ test_get_phase passed")

def test_add_boundary_flag():
    """Test boundary flag"""
    df = pd.DataFrame({'batsman_runs': [0, 1, 2, 4, 6, 3]})
    result = add_boundary_flag(df)
    expected = [0, 0, 0, 1, 1, 0]
    assert result['is_boundary'].tolist() == expected
    print("✅ test_add_boundary_flag passed")

def test_add_dot_ball_flag():
    """Test dot ball flag"""
    df = pd.DataFrame({'total_runs': [0, 1, 2, 4, 6, 3]})
    result = add_dot_ball_flag(df)
    expected = [1, 0, 0, 0, 0, 0]
    assert result['is_dot_ball'].tolist() == expected
    print("✅ test_add_dot_ball_flag passed")

def test_add_legal_ball_flag():
    """Test legal ball flag"""
    df = pd.DataFrame({'extra_type': ['NA', 'wides', 'noballs', 'NA', 'legbyes']})
    result = add_legal_ball_flag(df)
    expected = [1, 0, 0, 1, 1]
    assert result['is_legal_ball'].tolist() == expected
    print("✅ test_add_legal_ball_flag passed")

def test_add_batsman_ball_faced():
    """Test batsman ball faced"""
    df = pd.DataFrame({'extra_type': ['NA', 'wides', 'noballs', 'NA', 'legbyes']})
    result = add_batsman_ball_faced(df)
    expected = [1, 0, 1, 1, 1]  # wides don't count as ball faced
    assert result['batsman_ball_faced'].tolist() == expected
    print("✅ test_add_batsman_ball_faced passed")

def test_add_bowler_wicket_flag():
    """Test bowler wicket flag"""
    df = pd.DataFrame({'wicket_kind': ['bowled', 'caught', 'lbw', 'run out', 'retired hurt', 'NA']})
    result = add_bowler_wicket_flag(df)
    expected = [1, 1, 1, 0, 0, 0]
    assert result['is_bowler_wicket'].tolist() == expected
    print("✅ test_add_bowler_wicket_flag passed")

def test_cumulative_features():
    """Test cumulative features"""
    df = pd.DataFrame({
        'match_id': ['M1', 'M1', 'M1', 'M1'],
        'innings': ['1st', '1st', '1st', '1st'],
        'total_runs': [1, 2, 0, 4],
        'wicket': [0, 0, 1, 0],
        'is_legal_ball': [1, 1, 1, 1]
    })
    result = add_cumulative_features(df)
    expected_runs = [1, 3, 3, 7]
    expected_wickets = [0, 0, 1, 1]
    expected_balls = [1, 2, 3, 4]
    assert result['cumulative_runs'].tolist() == expected_runs
    assert result['cumulative_wickets'].tolist() == expected_wickets
    assert result['cumulative_legal_balls'].tolist() == expected_balls
    print("✅ test_cumulative_features passed")

def test_target_calculation():
    """Test target calculation"""
    df = pd.DataFrame({
        'match_id': ['M1', 'M1', 'M1', 'M1', 'M1', 'M1'],
        'innings': ['1st innings', '1st innings', '1st innings', '2nd innings', '2nd innings', '2nd innings'],
        'total_runs': [2, 3, 1, 1, 0, 2]
    })
    result = add_target(df)
    # First innings total = 6, target = 7
    actual = result['target'].tolist()
    assert pd.isna(actual[0]) and pd.isna(actual[1]) and pd.isna(actual[2])
    assert actual[3] == 7.0 and actual[4] == 7.0 and actual[5] == 7.0
    print("✅ test_target_calculation passed")

def test_runs_required():
    """Test runs required"""
    df = pd.DataFrame({
        'innings': ['1st innings', '2nd innings', '2nd innings'],
        'target': [np.nan, 100.0, 100.0],
        'cumulative_runs': [10, 20, 30]
    })
    result = add_runs_required(df)
    actual = result['runs_required'].tolist()
    assert pd.isna(actual[0])
    assert actual[1] == 80.0 and actual[2] == 70.0
    print("✅ test_runs_required passed")

def test_run_rates():
    """Test run rate calculations"""
    df = pd.DataFrame({
        'cumulative_runs': [10, 20, 30],
        'cumulative_legal_balls': [6, 12, 18],
        'innings': ['2nd innings', '2nd innings', '2nd innings'],
        'runs_required': [90, 80, 70],
        'balls_remaining': [114, 108, 102]
    })
    result = add_current_run_rate(df)
    result = add_required_run_rate(result)

    # CRR: 10/6 * 6 = 10, 20/12 * 6 = 10, 30/18 * 6 = 10
    expected_crr = [10.0, 10.0, 10.0]
    # RRR: 90/114 * 6, 80/108 * 6, 70/102 * 6
    expected_rrr = [90/114*6, 80/108*6, 70/102*6]

    assert np.allclose(result['current_run_rate'], expected_crr)
    assert np.allclose(result['required_run_rate'], expected_rrr)
    print("✅ test_run_rates passed")

if __name__ == "__main__":
    print("Running feature tests...")
    test_get_phase()
    test_add_boundary_flag()
    test_add_dot_ball_flag()
    test_add_legal_ball_flag()
    test_add_batsman_ball_faced()
    test_add_bowler_wicket_flag()
    test_cumulative_features()
    test_target_calculation()
    test_runs_required()
    test_run_rates()
    print("\n🎉 All tests passed!")