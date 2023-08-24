"""
Swiss Tournament, works for 6 Teams or more (equal number)
Generates matches, referees for matches
"""
import tkinter as tk
import datetime

from Tournament import Tournament
from Games import Game
from SaveAndRestore import SaveAndRestore
from Teams import Team, EmptyTeam
from PdfGenerator import PdfGenerator

class SwissTournament(Tournament):

    def __init__(self, fileName = None):
        super().__init__(fileName)
        self.teams = self.joinTeamsToOneGroup()
        self.startTimes = self.restored["startTimes"]
        self.endTimes = self.restored["endTimes"]
        self.rounds = self.restored["rounds"]
        self.timePerGame = self.restored["timePerGame"]
        self.breakBetweenRounds = self.restored["breakBetweenRounds"]
        self.emptyTeam = EmptyTeam()
        self.currentRound = self.restored["currentRound"]
        self.gamesPerRound = int(len(self.teams)/2)

    def joinTeamsToOneGroup(self):
        oneGroup = []
        for group in self.teams:
            oneGroup += group
        return oneGroup

    def generateGames(self):
        numberOfGamesPerRound = self.gamesPerRound
        sortedTable = self.sortGroups([self.teams])[0]
        for roundNumber in range(0, self.rounds):
            firstGameOfRound = roundNumber*numberOfGamesPerRound
            if self.previousRoundFinished(roundNumber, numberOfGamesPerRound) or roundNumber == 0:
                self.__currentMatches = self.getTeamsToMatch(sortedTable)
                self.__addReferees()
                self.getMatchOrder()
                self.__addGamesToList(firstGameOfRound, numberOfGamesPerRound)
            else:
                self.__currentMatches = self.getTeamsToMatch(sortedTable, emptyMode=True)
                self.__addGamesToList(firstGameOfRound, numberOfGamesPerRound)
        self.__addFinals(numberOfGamesPerRound)
        self.__addGamesToList((self.rounds+1)*numberOfGamesPerRound, numberOfGamesPerRound)
    
    def __addFinals(self, numberOfGamesPerRound):
        self.__currentMatches = []
        if self.previousRoundFinished(self.rounds, numberOfGamesPerRound):
            # TODO: Generate finals if tournament finished
            pass
        else:
            for index in range(numberOfGamesPerRound):
                match = []
                for i in range(2):
                    place = (numberOfGamesPerRound-index)*2-1+i
                    string = str(place) + ". Platz"
                    match.append(
                        Team(
                            string,
                            -2,
                            [],
                            0,
                            0,
                            0,
                            0,
                            0,
                            0
                        )
                    )
                self.__currentMatches.append(match)
        self.__getRefereesForFinals()

    def __getRefereesForFinals(self):
        for index, match in enumerate(self.__currentMatches):
            if index < 2:
                match.append(self.__currentMatches[-2+index][1])
            else:
                match.append(self.__currentMatches[index-2][0])

    def __addGamesToList(self, firstGameOfRound, gamesPerRound, finals=False):
        currentDateTime = datetime.datetime.strptime(self.startTimes[0], '%H:%M')
        currentDay = 0
        group = 0
        if finals:
            group = -1
        round = []
        for index, game in enumerate(self.__currentMatches):
            if len(self.games)>0 and index == 0:
                currentDateTime = datetime.datetime.strptime(self.games[-1].time, '%H:%M')
                currentDateTime += datetime.timedelta(minutes=(self.breakBetweenRounds+self.timePerGame))
                currentDay = self.games[-1].day
            if len(self.endTimes) > currentDay:
                if currentDateTime > datetime.datetime.strptime(self.endTimes[currentDay], '%H:%M'):
                    currentDay += 1
                    currentDateTime = datetime.datetime.strptime(self.startTimes[currentDay], '%H:%M')
            currentTime = currentDateTime.strftime('%H:%M')
            round.append(
                Game(
                    group,
                    currentTime,
                    currentDay,
                    game[0],
                    game[1],
                    game[2],
                    [-1, -1],
                    [[], []]
                    )
            )
            game[2].gamesRefed += 1
            currentDateTime += datetime.timedelta(minutes=(self.timePerGame))
        if len(self.games) <= firstGameOfRound:
            self.games += round
        else:
            i = 0
            for gameIndex in range(firstGameOfRound,firstGameOfRound+gamesPerRound):
                self.games[gameIndex] = round[i]
                i += 1

    def getTeamsToMatch(self, sortedTable, emptyMode=False):
        matches = []
        selectedTeamBs = []
        if emptyMode:
            for index in range(int(len(sortedTable)/2)):
                matches.append([self.emptyTeam, self.emptyTeam, self.emptyTeam])
            return matches
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
            try:
                if game.teamA.name == teamA.name and game.teamB.name == teamB.name:
                    return True
                if game.teamA.name == teamB.name and game.teamB.name == teamA.name:
                    return True
            except:
                return False
        return False
    
    def previousRoundFinished(self, roundNumber, numberOfGamesPerRound):
        lastGamePreviousRound = roundNumber*numberOfGamesPerRound-1
        if lastGamePreviousRound > 0:
            if self.games[lastGamePreviousRound].score[0] != -1:
                return True
        return False
    
    def getMatchOrder(self):
        root = tk.Tk()
        root.title("List Reorder")
        self.displayList(root)
        root.mainloop() 

    def displayList(self, root, frame=None):
        # TODO: Clean this up
        if frame:    
            frame.destroy()
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)
        matches = self.__currentMatches
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

    def updateOrder(self, list, frame, root):
        list = sorted(list, key=lambda x: x[-1].get())
        matches = [match[:-1] for match in list]
        self.__currentMatches = matches
        self.__addReferees()
        self.displayList(root, frame)   

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

    def generateGamesOfRound(self, roundNumber):
        gamesPerRound = self.gamesPerRound
        games = []
        for gameIndex in range(gamesPerRound*roundNumber, gamesPerRound*(roundNumber+1)):
            games.append(self.games[gameIndex])
        return games

    def saveFile(self):
        teams = []
        games = []
        for team in self.teams:
            teams.append(team.export())
        for game in self.games:
            games.append(game.export())
        dict = {
            "teams": teams,
            "games": games,
            "startTimes": self.startTimes,
            "endTimes": self.endTimes,
            "rounds": self.rounds,
            "timePerGame": self.timePerGame,
            "breakBetweenRounds": self.breakBetweenRounds,
            "days": self.days,
            "dates": self.dates,
            "currentRound": self.currentRound
        }
        SaveAndRestore.save(self.fileName, dict)
        
    def generatePdf(self):
        gamesPerRound = self.gamesPerRound
        generator = PdfGenerator(self, True, gamesPerRound)
        generator.generateTexFile()

if __name__ == "__main__":
    import os
    swissTournament = SwissTournament()
    swissTournament.generateGames()
    swissTournament.saveFile()
    swissTournament.generatePdf()

