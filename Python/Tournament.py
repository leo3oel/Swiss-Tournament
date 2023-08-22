from tkinter import filedialog

from SaveAndRestore import SaveAndRestore
from Teams import Team

class Tournament:

    def __init__(self, fileName = None):
        if not fileName:
            fileName = filedialog.askopenfile()
        self.restored = SaveAndRestore.restore(fileName)
        self.teams = self.__getTeams(self.restored["teams"])
        self.days = self.restored["days"]
        self.dates = self.restored["dates"]

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