import pandas as pd


def create_match_df(data,file):
   
    match_info = {

        'match_id' : file.name.split('.')[0],
        'match_date' : pd.to_datetime(data['info']['dates'][0]),
        'venue' : data['info'].get('city','NA'),
        'toss' : data['info']['toss']['winner'],
        'toss_decision' : data['info']['toss']['decision'],
        'team1' : data['info']['teams'][0],
        'team2' : data['info']['teams'][1],
        'winner' : data['info']['outcome'].get('winner', 'NA')

    }
    return match_info


def create_ball_df(data,file):
    ball_info_list = []
    for inning in data['innings']:
            innings_name = list(inning.keys())[0]
            # print(innings_name)
            batting_team = inning[innings_name]['team']
            bowling_team = [team for team in data['info']['teams'] if team!= batting_team][0]

            for ball_dict in inning[innings_name]['deliveries']:
                for ball_num,info in ball_dict.items():

                    # fielders when wicket falls
                    if info.get('wicket')  and info.get('wicket').get('fielders') :

                        fielders = info.get('wicket').get('fielders') 
                    # fielders_list= list(fielders)
                        fielders_involved = ", ".join(fielders)
                        # print(fielders_involved)
                    else :
                        fielders_involved = 'NA'

                    #same for extra_type

                    if info.get('extras'):
                        extra_type = list(info.get('extras',{}).keys()) if info.get('extras') else 'NA'
                        extra_type = ", ".join(extra_type)
                        # print(extra_type)
                    else :
                        extra_type = 'NA'


                    ball_info = {
                        'match_id' : file.name.split('.')[0],
                        'innings' : innings_name,
                        'over' : ball_num,
                        'batting_team' : batting_team,
                        'bowling_team' : bowling_team,
                        'non_striker' :info['non_striker'],
                        'bowler' : info['bowler'],
                        'batsman' : info['batsman'],
                        'wicket' : int(bool(info.get('wicket'))),
                        'wicket_kind' : info.get('wicket').get('kind') if info.get('wicket') else 'NA',
                        'fielders' : fielders_involved,
                        'player_out' : info.get('wicket').get('player_out') if info.get('wicket') else 'NA',
                        'batsman_runs': info.get('runs', {}).get('batsman', 0),
                        'extra_runs': info.get('runs', {}).get('extras', 0),
                        'total_runs': info.get('runs', {}).get('total', 0),
                        'extra_type' : extra_type


                    }
                    ball_info_list.append(ball_info)
        
    return ball_info_list
