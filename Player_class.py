import pandas as pd
from utils import pandas_player_match

class Player:
    def __init__(self, player_name, i):
        self.i = i
        self.player_name = player_name
        self.current_rank = ""
        self.hand = ""
        self.bday = ""
        self.height = ""
        self.nationality = ""
        self.matches = []
        self.matches_pd = None

    def update(self):
        """Update player's personal data using their index."""
        _, self.current_rank, self.hand, self.bday, self.height, self.nationality = get_player_personal_data(self.i)
    
    def update_as_self(self, matchmx_row):
        """Record match data when this player is a participant."""
        relevant_data = [
            matchmx_row[0],  # Date
            matchmx_row[1],  # Tournament Name
            matchmx_row[2],  # Surface
            matchmx_row[3],  # Tournament level
            matchmx_row[4],  # Win/Loss/Undergoing
            matchmx_row[5],  # Rank
            matchmx_row[6],  # Seed
            matchmx_row[8],  # Round
            matchmx_row[9],  # Score
            matchmx_row[11],  # Opponent Name
            matchmx_row[12],  # Opponent Rank
            matchmx_row[13],  # Opponent Seed
            matchmx_row[15],  # Opponent Hand
            matchmx_row[16],  # Opponent BDay
            matchmx_row[17],  # Opponent Height
            matchmx_row[18],  # Opponent Nationality
        ]
        self.matches.append(relevant_data)
    
    def update_as_opp(self, matchmx_row, opp):
        """Record match data when this player is the opponent."""
        status = 'L' if matchmx_row[4] == 'W' else 'W' if matchmx_row[4] == 'L' else 'U'
        relevant_data = [
            matchmx_row[0],  # Date
            matchmx_row[1],  # Tournament Name
            matchmx_row[2],  # Surface
            matchmx_row[3],  # Tournament level
            status,          # Updated status
            matchmx_row[12], # Rank
            matchmx_row[13], # Seed
            matchmx_row[8],  # Round
            matchmx_row[9],  # Score
            opp.player_name,  # Opponent Name
            matchmx_row[5],   # Opponent Rank
            matchmx_row[6],   # Opponent Seed
            opp.hand,         # Opponent Hand
            opp.bday,         # Opponent BDay
            opp.height,       # Opponent Height
            opp.nationality   # Nationality
        ]
        self.matches.append(relevant_data)

    def convert_match_data_to_pd(self):
        """Convert match data to pandas DataFrame."""
        self.matches_pd = pandas_player_match(self.matches)

    def get_win_percentage_date(self, num, date):
        """Get the win percentage of the player."""
        wins = 0
        games = 0
        
        # Convert the input date to a Timestamp object
        date = pd.to_datetime(date)

        # Count games and wins
        matches_counted = 0
        try:
            for i in range(len(self.matches)):
                # Convert match date to a Timestamp before comparing
                match_date = pd.to_datetime(self.matches[i][0])
                
                if match_date < date:  # Only consider matches before the given date
                    games += 1
                    if self.matches[i][4] == 'W':
                        wins += 1
                    elif self.matches[i][4] == 'U':
                        wins += 0.5  # Neutral outcome
                    
                    matches_counted += 1
                    if matches_counted >= num:  # Stop once we have enough matches
                        break
        except IndexError:
            pass

        # Calculate win percentage
        win_percentage = 0.0
        if games > 0:
            win_percentage = (wins / games) * 100
        
        return wins, games, win_percentage
        


    def get_surface_win_percentage(self, num):
        """Get the win percentage of the player on a given surface."""
        surface_games = {"Hard": 0, "Clay": 0, "Grass": 0}
        surface_wins = {"Hard": 0, "Clay": 0, "Grass": 0}

        # Count games and wins
        try:
            for i in range(num):
                surface = self.matches[i][2]  # Surface type
                result = self.matches[i][4]    # Match result
                
                if surface in surface_games:
                    surface_games[surface] += 1
                    if result == 'W':
                        surface_wins[surface] += 1
                    elif result == 'U':
                        surface_wins[surface] += 0.5  # Neutral outcome
        except IndexError:
            pass

        # Calculate win percentage
        surface_win_percentage = {}
        for surface in surface_games.keys():
            total_games = surface_games[surface]
            if total_games > 0:
                surface_win_percentage[surface] = (surface_wins[surface] / total_games) * 100
            else:
                surface_win_percentage[surface] = 0.0  # No games played on this surface
    
        return surface_wins, surface_games, surface_win_percentage
    
    def get_surface_win_percentage_date(self, num, date):
        """Get the win percentage of the player on a given surface for the 'num' matches before the given date."""
        surface_games = {"Hard": 0, "Clay": 0, "Grass": 0}
        surface_wins = {"Hard": 0, "Clay": 0, "Grass": 0}
        
        # Convert the input date to a Timestamp object
        date = pd.to_datetime(date)

        # Count games and wins
        matches_counted = 0
        try:
            for i in range(len(self.matches)):
                # Convert match date to a Timestamp before comparing
                match_date = pd.to_datetime(self.matches[i][0])
                
                if match_date < date:  # Only consider matches before the given date
                    surface = self.matches[i][2]  # Surface type
                    result = self.matches[i][4]   # Match result

                    if surface in surface_games:
                        surface_games[surface] += 1
                        if result == 'W':
                            surface_wins[surface] += 1
                        elif result == 'U':
                            surface_wins[surface] += 0.5  # Neutral outcome
                    
                    matches_counted += 1
                    if matches_counted >= num:  # Stop once we have enough matches
                        break
        except IndexError:
            pass

        # Calculate win percentage
        surface_win_percentage = {}
        for surface in surface_games.keys():
            total_games = surface_games[surface]
            if total_games > 0:
                surface_win_percentage[surface] = (surface_wins[surface] / total_games) * 100
            else:
                surface_win_percentage[surface] = 0.0
        
        return surface_wins, surface_games, surface_win_percentage
    

    def get_surface_win_percentage_date_surface(self, num, date, surface):
        """Get the win percentage of the player for the 'num' matches on the given surface before the given date."""
        surface_games = 0
        surface_wins = 0
        
        # Convert the input date to a Timestamp object
        date = pd.to_datetime(date)

        # Count games and wins
        matches_counted = 0
        try:
            for i in range(len(self.matches)):
                # Convert match date to a Timestamp before comparing
                match_date = pd.to_datetime(self.matches[i][0])
                
                if match_date < date:  # Only consider matches before the given date
                    match_surface = self.matches[i][2]  # Surface type
                    result = self.matches[i][4]   # Match result

                    if match_surface == surface:  # Only count matches on the given surface
                        surface_games += 1
                        if result == 'W':
                            surface_wins += 1
                        elif result == 'U':
                            surface_wins += 0.5  # Neutral outcome
                        
                        matches_counted += 1
                        if matches_counted >= num:  # Stop once we have enough matches
                            break
        except IndexError:
            pass

        # Calculate win percentage
        surface_win_percentage = 0.0
        if surface_games > 0:
            surface_win_percentage = (surface_wins / surface_games) * 100
        
        return surface_wins, surface_games, surface_win_percentage




    def get_player_meetings(self, player2):
        return self.matches_pd[self.matches_pd['Opp Name'] == player2][['Tournament Name', 
                                                                        'Surface',
                                                                        'Tournament level',
                                                                        'Status',
                                                                        'Round',
                                                                        'Score',
                                                                        'Rank',
                                                                        'Seed',
                                                                        'Opp Rank',
                                                                        'Opp Seed',
                                                                        ]]
