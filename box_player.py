from constant import POSITION_MAP, PRO_TEAM_MAP
from player import Player
from datetime import datetime, timedelta

class BoxPlayer(Player):
    '''player with extra data from a matchup'''
    def __init__(self, data, pro_schedule, positional_rankings, week, cur_team_id):
        super(BoxPlayer, self).__init__(data)
        self.slot_position = 'FA'
        self.points = 0
        self.projected_points = 0
        self.pro_opponent = "None" # professional team playing against
        self.pro_pos_rank = 0 # rank of professional team against player position
        self.game_played = 100 # 0-100 for percent of game played
        self.current_team = ''

        if cur_team_id != '':
            self.current_team = cur_team_id

        if 'lineupSlotId' in data:
            self.slot_position = POSITION_MAP[data['lineupSlotId']]

        player = data['playerPoolEntry']['player'] if 'playerPoolEntry' in data else data['player']
        if player['proTeamId'] in pro_schedule:
            (opp_id, date) = pro_schedule[player['proTeamId']]
            self.game_played = 100 if datetime.now() > datetime.fromtimestamp(date/1000.0) + timedelta(hours=3) else 0
            if str(player['defaultPositionId']) in positional_rankings:
                self.pro_opponent = PRO_TEAM_MAP[opp_id]
                self.pro_pos_rank = positional_rankings[str(player['defaultPositionId'])][str(opp_id)]


        player_stats = player['stats']
        for stats in player_stats:
            if stats['statSourceId'] == 0 and stats['scoringPeriodId'] == week:
                self.points = round(stats['appliedTotal'], 2)
            elif stats['statSourceId'] == 1 and stats['scoringPeriodId'] == week:
                self.projected_points = round(stats['appliedTotal'], 2)
            
    
    def __repr__(self):
        return 'Player(%s, points:%d, projected:%d)' % (self.name, self.points, self.projected_points)
