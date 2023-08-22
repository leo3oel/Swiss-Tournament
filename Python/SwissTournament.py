from Tournament import Tournament

class SwissTournament(Tournament):

    def __init__(self):
        super().__init__()
        self.teams = self.joinTeamsToOneGroup()
        self.startTimes = self.restored["startTimes"]
        self.endTimes = self.restored["endTimes"]
        self.rounds = self.restored["rounds"]
        self.timePerGame = self.restored["timePerGame"]
        self.breakBetweenRounds = self.restored["breakBetweenRounds"]
        self.games = self.restored["games"]
        self.generateGames()

    def joinTeamsToOneGroup(self):
        oneGroup = []
        for group in self.teams:
            oneGroup += group
        return oneGroup

    def generateGames(self):
        numberOfGamesPerRound = len(self.teams)/2
        sortedTable = self.sortGroups([self.teams])[0]
        if len(self.games) > 0 and self.previousRoundFinished(numberOfGamesPerRound):
            pass
        else:
            teamsToMatch = self.getTeamsToMatch(sortedTable)

    def getTeamsToMatch(self, sortedTable):
        matches = []
        selectedTeamBs = []
        for teamAIndex in range(len(sortedTable)-1):
            if not teamAIndex in selectedTeamBs:
                for teamBIndex in range(teamAIndex+1, len(sortedTable)):
                    if not self.checkIfGameExists(sortedTable[teamAIndex], sortedTable[teamBIndex]):
                        matches.append([sortedTable[teamAIndex], sortedTable[teamBIndex]])
                        selectedTeamBs.append(teamBIndex)
                        break
        return matches

    def checkIfGameExists(self, teamA, teamB):
        for game in self.games:
            if game.teamA.name == teamA.name and game.teamB.name == teamB.name:
                return True
            if game.teamA.name == teamB.name and game.teamB.name == teamA.name:
                return True
        return False
    
    def previousRoundFinished(self, numberOfGamesPerRound):
        for game in self.games[-numberOfGamesPerRound:]:
            if type(game.score[0]) is not int:
                return False
        return True

if __name__ == "__main__":
    swissTournament = SwissTournament()
