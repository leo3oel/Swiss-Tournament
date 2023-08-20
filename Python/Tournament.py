from tkinter import filedialog

from SaveAndRestore import SaveAndRestore
from Teams import Team
from Games import Game

class Tournament:

    def __init__(self, fileName = None):
        if not fileName:
            fileName = filedialog.askopenfile()
        restored = SaveAndRestore.restore(fileName)
        self.teams = self.__getTeams(restored["teams"])
        self.games = self.__getGames(restored["games"], restored["days"])
        self.days = restored["days"]

    def __getTeams(self, restoredTeams):
        teams = []
        for team in restoredTeams:
            while len(teams) <= team["group"]:
                teams.append([])
            teams[team["group"]].append(Team(
                team["name"],
                team["group"],
                team["players"],
                team["games"]
            ))
        return teams
    
    def __getGames(self, restoredGames, restoredDays, getIntermediateWithTeams = False, getFinalsWithTeams = False):
        games = []
        for game in restoredGames:
            if game["group"] < 0:
                if game["group"] == -1:
                    self.__getIntermediate(game, games, restoredDays, getIntermediateWithTeams)
                elif game["group"] == -2:
                    self.__getFinals(game, games, restoredDays, getFinalsWithTeams)
            else:
                group = chr(ord('A')+game["group"])
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        self.teams[game["group"]][game["teamA"]],
                        self.teams[game["group"]][game["teamB"]],
                        self.teams[game["group"]][game["referee"]],
                        game["score"],
                    )
                )
        return games
    
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

if __name__ == "__main__":
    main = Tournament()
    main.printTable()