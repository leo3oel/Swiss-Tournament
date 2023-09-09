"""
Create Teams, each team consists from players
Saves Player scores
"""
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

    def incrementGoals(self, value):
        self.goals += value

    def addRedCard(self):
        self.redCards+=1

    def addYellowCard(self):
        self.yellowCards+=1

    def addGreenCard(self):
        self.greenCards+=1

    def returnPlayer(self):
        if type(self.name) is list:
            name = " ".join(self.name)
        else:
            name = self.name
        text = [
            str(self.number),
            name,
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

    def __init__(self, name, group, players, numberOfWins, numberOfLosses, numberOfTies, goalsPlus, goalsMinus, gamesRefed):
        self.name = name
        self.players = [Player(*player, self.name) for player in players]
        self.group = group
        self.numberOfWins = numberOfWins
        self.numberOfLosses = numberOfLosses
        self.numberOfTies = numberOfTies
        self.goalsPlus = goalsPlus
        self.goalsMinus = goalsMinus
        self.gamesRefed = gamesRefed

    def getPoints(self) -> int:
        points = 0
        points += self.numberOfTies*1
        points += self.numberOfWins*3
        return points
    
    def getPlusGoals(self):
        return self.goalsPlus
    
    def getMinusGoals(self):
        return self.goalsMinus
    
    def getGoalDiff(self):
        return self.getPlusGoals() - self.getMinusGoals()
    
    def getNumberOfGames(self):
        return self.numberOfLosses + self.numberOfTies + self.numberOfWins
    
    def incrementGoalCountOfPlayer(self, playerNumber, value):
        if self.checkIfPlayerExists(playerNumber):
            for player in self.players:
                if playerNumber == player.number:
                    player.incrementGoals(value)
                    break
        else:
            self.players.append(Player(playerNumber, 
                                       "Unknown",
                                       0,
                                       0,
                                       0,
                                       value,
                                       self.name))

    def checkIfPlayerExists(self, playerNumber):
        playerNumberList = [player.number for player in self.players]
        if playerNumber not in playerNumberList:
            return False
        return True

    def getPlayersList(self):
        return self.players
    
    def getExportPlayers(self):
        players = self.getPlayersList()
        return [player.export() for player in players]
    
    def export(self):
        dict = {
            "name": self.name,
            "group": self.group,
            "players": self.getExportPlayers(),
            "numberOfWins": self.numberOfWins,
            "numberOfLosses": self.numberOfLosses,
            "numberOfTies": self.numberOfTies,
            "goals+": self.getPlusGoals(),
            "goals-": self.getMinusGoals(),
            "gamesRefed": self.gamesRefed
        }
        return dict
    
    def getScorers(self):
        scorer = [player.returnPlayer() for player in self.players]
        scorer = sorted(scorer, reverse=True, key=lambda x: int(x[-1]))
        return scorer
    
class EmptyTeam(Team):

    def __init__(self):
        super().__init__("", -5, [], [], 0, 0, 0, 0, 0)

