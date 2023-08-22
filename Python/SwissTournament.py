import tkinter as tk
import datetime

from Tournament import Tournament
from Games import Game

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
            self.__currentMatches = self.getTeamsToMatch(sortedTable)
            self.__addReferees()
            self.getMatchOrder(self.__currentMatches)
            self.__currentMatches
            self.__addGamesToList()

    def __addGamesToList(self):
        currentDateTime = datetime.datetime.strptime(self.startTimes[0], '%H:%M')
        currentDay = 0
        if len(self.games)>0:
            currentDateTime = datetime.datetime.strptime(self.games[-1].time, '%H:%M')
            currentDateTime += datetime.timedelta(minutes=(self.breakBetweenRounds+self.timePerGame))
            currentDay = self.days.index(self.games[-1].date)
        for game in self.__currentMatches:
            if len(self.endTimes) > currentDay:
                if currentDateTime > datetime.datetime.strptime(self.endTimes[currentDay], '%H:%M'):
                    currentDay += 1
                    currentDateTime = datetime.datetime.strptime(self.startTimes[currentDay], '%H:%M')
            currentTime = currentDateTime.strftime('%H:%M')
            self.games.append(
                Game(
                    "0",
                    currentTime,
                    currentDay,
                    game[0],
                    game[1],
                    game[2],
                    ["", ""]
                    )
            )
            currentDateTime += datetime.timedelta(minutes=(self.timePerGame))

    def getTeamsToMatch(self, sortedTable):
        matches = []
        selectedTeamBs = []
        for teamAIndex in range(len(sortedTable)-1):
            if not teamAIndex in selectedTeamBs:
                for teamBIndex in range(teamAIndex+1, len(sortedTable)):
                    if not self.checkIfGameExists(sortedTable[teamAIndex], sortedTable[teamBIndex]):
                        matches.append([sortedTable[teamAIndex], sortedTable[teamBIndex], ""])
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
    
    def getMatchOrder(self, teamsToMatch):
        root = tk.Tk()
        root.title("List Reorder")
        self.displayList(root, teamsToMatch)
        root.mainloop() 

    def displayList(self, root, matches, frame=None):
        # TODO: Clean this up
        if frame:    
            frame.destroy()
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)
        for index, teams in enumerate(matches):
            if len(teams)<4:
                teams.append("")
            entry = tk.Entry(frame)
            entry.insert(0, str(1+index))
            teams[-1] = entry
        tk.Label(frame, text="Team A").grid(
            column=0, row=0, padx=5, pady=10
        ),
        tk.Label(frame, text="Team B").grid(
            column=1, row=0, padx=5, pady=10
        ),
        tk.Label(frame, text="Referee").grid(
            column=2, row=0, padx=5, pady=10
        ),
        tk.Label(frame, text="Position").grid(
            column=3, row=0, padx=5, pady=10
        )
        for index, teams in enumerate(matches):
            tk.Label(frame, text=teams[0].name).grid(
                column=0, row=1+index, padx=5, pady=5
            ),
            tk.Label(frame, text=teams[1].name).grid(
                column=1, row=1+index, padx=5, pady=5
            ),
            tk.Label(frame, text=teams[2].name).grid(
                column=2, row=1+index, padx=5, pady=5
            ),
            teams[3].grid(
                column=3, row=1+index, padx=5, pady=5
            )
        reorderButton = tk.Button(frame, text="Refresh Order", command=lambda: self.updateOrder(matches, frame, root))
        reorderButton.grid(
            column=1, row=200, padx=5, pady=10
        )
        return matches

    def updateOrder(self, list, frame, root):
        list = sorted(list, key=lambda x: x[-1].get())
        self.__currentMatches = [match[:-1] for match in list]
        self.__addReferees()
        self.displayList(root, list, frame)

    def __addReferees(self):
        sortedReferees = sorted(self.teams, key=lambda team: team.gamesRefed)
        for index, match in enumerate(self.__currentMatches):
            for ref in sortedReferees:
                currentMatch = [match[0].name, match[1].name]
                if index<len(self.__currentMatches)-1:
                    nextMatch = self.__currentMatches[index+1]
                    nextMatch = [nextMatch[0].name, nextMatch[1].name]
                else:
                    nextMatch = []
                if index > 0:
                    previousMatch = self.__currentMatches[index-1]
                    previousMatch = [previousMatch[0].name, previousMatch[1].name]
                else:
                    previousMatch = []
                if (ref.name not in currentMatch) \
                    and (ref.name not in nextMatch) \
                    and (ref.name not in previousMatch):
                    match[2] = ref
                    sortedReferees.remove(ref)
                    break



if __name__ == "__main__":
    swissTournament = SwissTournament()