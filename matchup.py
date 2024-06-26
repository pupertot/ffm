class Matchup(object):
    def __init__(self, data):
        self.data = data
        self._fetch_matchup_info()

    def __repr__(self):
        return 'Matchup(%s, %s)' % (self.home_team, self.away_team, )

    def _fetch_matchup_info(self):
        '''Fetch info for matchup'''
        self.home_team = self.data['home']['teamId']
        self.home_score = self.data['home']['totalPoints']
        self.away_team = self.data['away']['teamId']
        self.away_score = self.data['away']['totalPoints']
