class Player:

    def __init__(self, number, name, redCards, greenCards, yellowCards, goals, teamName):
        self.name = name
        self.teamName = teamName
        self.number = number
        self.redCards = redCards
        self.yellowCards = yellowCards
        self.greenCards = greenCards
        self.goals = goals

    def setToZero(self):
        self.redCards = 0
        self.yellowCards = 0
        self.greenCards = 0
        self.goals = 0

    def addGoal(self):
        self.goals+=1

    def addRedCard(self):
        self.redCards+=1

    def addYellowCard(self):
        self.yellowCards+=1

    def addGreenCard(self):
        self.greenCards+=1

    def returnPlayer(self):
        text = [
            str(self.number),
            " ".join(self.name),
            self.teamName,
            str(self.goals)
        ]
        return(text)
    
    def export(self):
        list = [self.number, 
                self.name, 
                self.redCards, 
                self.greenCards, 
                self.yellowCards, 
                self.goals]
        return list


class Team:

    def __init__(self, name, group, players, games, gamesRefed):
        self.name = name
        self.players = [Player(*player, self.name) for player in players]
        self.group = group
        self.games = games
        self.gamesRefed = gamesRefed

    def addGame(self, goalsPlus, goalsMinus, playerNumberGoals, playerNumberRedCard, playerNumberYellowCard, playerNumberGreenCard):
        self.games.append([goalsPlus, goalsMinus, playerNumberGoals, playerNumberRedCard, playerNumberYellowCard, playerNumberGreenCard])

    def changeGame(self, gameNumber, goalsPlus, goalsMinus, playerNumberGoals, playerNumberRedCard, playerNumberYellowCard, playerNumberGreenCard):
        self.games[gameNumber] = [goalsPlus, goalsMinus, playerNumberGoals, playerNumberRedCard, playerNumberYellowCard, playerNumberGreenCard]

    def getPoints(self):
        points = 0
        for game in self.games:
            if game[0] > game[1]:
                points += 3
            elif game[0] == game[1]:
                points += 1
        return points
    
    def getPlusGoals(self):
        plusGoals = 0
        for game in self.games:
            plusGoals += game[0]
        return plusGoals
    
    def getMinusGoals(self):
        minusGoals = 0
        for game in self.games:
            minusGoals += game[1]
        return minusGoals
    
    def getGoalDiff(self):
        return self.getPlusGoals() - self.getMinusGoals()
            
    def refreshPlayerList(self):
        for player in self.players:
            player.setToZero()
        for game in self.games:
            for playerNumber in game[2]:
                self.checkIfPlayerExists(playerNumber)
                selectedPlayer = next(player for player in self.players if player.number==playerNumber)
                selectedPlayer.addGoal()
            for playerNumber in game[3]:
                self.checkIfPlayerExists(playerNumber)
                selectedPlayer = next(player for player in self.players if player.number==playerNumber)
                selectedPlayer.addRedCard()
            for playerNumber in game[4]:
                self.checkIfPlayerExists(playerNumber)
                selectedPlayer = next(player for player in self.players if player.number==playerNumber)
                selectedPlayer.addYellowCard()
            for playerNumber in game[4]:
                self.checkIfPlayerExists(playerNumber)
                selectedPlayer = next(player for player in self.players if player.number==playerNumber)
                selectedPlayer.addGreenCard()
                
    def checkIfPlayerExists(self, playerNumber):
        playerNumberList = [player.number for player in self.players]
        if playerNumber not in playerNumberList:
            self.players.append(Player(playerNumber, "Unknown", 0, 0, 0, 0))

    def getPlayersList(self):
        self.refreshPlayerList()
        return self.players
    
    def getExportPlayers(self):
        players = self.getPlayersList()
        return [player.export() for player in players]
    
    def export(self):
        dict = {
            "name": self.name,
            "group": self.group,
            "players": self.getExportPlayers(),
            "points": self.getPoints(),
            "goals+": self.getPlusGoals(),
            "goals-": self.getMinusGoals(),
            "games" : self.games,
            "gamesRefed": self.gamesRefed
        }
        return dict
    
class EmptyTeam(Team):

    def __init__(self):
        super().__init__("", -5, [], [], 0)

if __name__ == "__main__":
    list = [Player(1,"Name", 0,0,0,0), Player(2,"Name", 0,0,0,0)]
    playerNumberList = [player.number for player in list]
    print(playerNumberList)
