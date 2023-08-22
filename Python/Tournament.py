from tkinter import filedialog

from SaveAndRestore import SaveAndRestore
from Teams import Team
from Games import Game

class Tournament:

    def __init__(self, fileName = None):
        if not fileName:
            fileName = filedialog.askopenfile()
        self.restored = SaveAndRestore.restore(fileName)
        self.fileName = fileName
        self.teams = self.__getTeams(self.restored["teams"])
        self.days = self.restored["days"]
        self.dates = self.restored["dates"]
        self.games = self.__getGames(self.restored["games"], self.restored["days"])

    def __getGames(self, restoredGames, restoredDays, getIntermediateWithTeams = False, getFinalsWithTeams = False):
        games = []
        for game in restoredGames:
            if game["group"] < 0:
                if game["group"] == -1:
                    self.__getIntermediate(game, games, restoredDays, getIntermediateWithTeams)
                elif game["group"] == -2:
                    self.__getFinals(game, games, restoredDays, getFinalsWithTeams)
            else:
                group = game["group"]
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        self.__getTeamFromTeamName(game["teamA"]),
                        self.__getTeamFromTeamName(game["teamB"]),
                        self.__getTeamFromTeamName(game["referee"]),
                        game["score"]
                    )
                )
        return games
    
    def __getTeamFromTeamName(self, teamName):
        for group in self.teams:
            for team in group:
                if team.name == teamName:
                    return team
                
    def __getIntermediate(self, game, games, restoredDays, withTeams):
            group = "Z"
            if self.__alreadyGamesPlayed() and withTeams:
                sortedGroups = self.sortGroups(self.teams)
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        sortedGroups[game["teamA"][0]][game["teamA"][1]],
                        sortedGroups[game["teamB"][0]][game["teamB"][1]],
                        sortedGroups[game["referee"][0]][game["referee"][1]],
                        game["score"],
                    )
                )
            else:
                groupTeamA = chr(ord('A')+game["teamA"][0])
                groupTeamB = chr(ord('A')+game["teamB"][0])
                groupTeamRef = chr(ord('A')+game["referee"][0])
                stringTeamA = f"{game['teamA'][1]+1}. Gruppe {groupTeamA}"
                stringTeamB = f"{game['teamB'][1]+1}. Gruppe {groupTeamB}"
                stringTeamRef = f"{game['referee'][1]+1}. Gruppe {groupTeamRef}"
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        stringTeamA,
                        stringTeamB,
                        stringTeamRef,
                        game["score"],
                    )
                )

    def __getFinals(self, game, games, restoredDays, withTeams):
        group = f"Pl. {game['teamA']+1}"    
        if withTeams:
            combinedGroup = []
            for group in self.teams:
                combinedGroup += group
            sortedGroup = self.sortGroups([combinedGroup])[0]
            games.append(
                Game(
                    group,
                    game["time"],
                    game["day"],
                    sortedGroup[game["teamA"]],
                    sortedGroup[game["teamB"]],
                    sortedGroup[game["referee"]],
                    game["score"],
                )
            )
        else:
            teamAStr = f"Platz {game['teamA']+1}"
            teamBStr = f"Platz {game['teamB']+1}"
            refereeStr = f"Platz {game['referee']+1}"
            games.append(
                Game(
                    group,
                    game["time"],
                    game["day"],
                    teamAStr,
                    teamBStr,
                    refereeStr,
                    game["score"],
                )
            )

    def __alreadyGamesPlayed(self):
        for group in self.teams:
            for team in group:
                if team.getPoints()>0:
                    return True
        return False

    def __getTeams(self, restoredTeams):
        teams = []
        for team in restoredTeams:
            while len(teams) <= team["group"]:
                teams.append([])
            teams[team["group"]].append(Team(
                team["name"],
                team["group"],
                team["players"],
                team["games"],
                team["gamesRefed"]
            ))
        return teams

    def sortGroups(self, groupLists):
        sortedGroups = []
        for group in groupLists:
            sortedGroups.append(
                sorted(group, key = lambda x : (x.getPoints(), x.getGoalDiff(), x.getPlusGoals()), reverse=True)
            )
        return sortedGroups

    def printTable(self):
        combinedGroups = []
        for group in self.teams:
            combinedGroups += group
        combinedGroups = self.teams + [combinedGroups]
        sortedGroups = self.sortGroups(combinedGroups)
        integer = 1
        for group in sortedGroups:
            print("Gruppe " + str(integer))
            integer+=1
            for team in group:
                print(team.name + " " + str(team.getPoints()) + " " + str(team.getGoalDiff()) + " " + str(team.getPlusGoals()) + " " + str(team.getMinusGoals()))
            print()

    def getPlayersWithTeams(self):
        players = []
        for group in self.teams:
            for team in group:
                playerList = [team.name]
                for player in team.getPlayersList():
                    playerList.append(player)
                players.append(playerList)
        return players
    
    def printPlayersWithTeams(self, playerList):
        for team in playerList:
            print("===== " + team[0] + " =====")
            for playerindex in range(1, len(team)):
                print(" ".join(team[playerindex].returnPlayer()))

if __name__ == "__main__":
    main = Tournament()
    main.printTable()
    main.printPlayersWithTeams(main.getPlayersWithTeams())