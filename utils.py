import pandas as pd

def pandas_player_match(player_matches):

    match_data = pd.DataFrame(player_matches, columns=[
        'Date', 
        'Tournament Name', 
        'Surface', 
        'Tournament level', 
        'Status',
        'Rank', 
        'Seed', 
        'Round', 
        'Score', 
        'Opp Name', 
        'Opp Rank', 
        'Opp Seed', 
        'Opp Hand', 
        'Opp BDay', 
        'Opp Height', 
        'Opp Nationality'
    ])

    match_data['Date'] = pd.to_datetime(match_data['Date'])
    match_data.set_index('Date', inplace=True)
    match_data.sort_index(inplace=True, ascending=False)


    return match_data


