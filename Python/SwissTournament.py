"""
Swiss Tournament, works for 6 Teams or more (equal number)
Generates matches, referees for matches
"""
import tkinter as tk
import datetime
import os
import argparse

from Tournament import Tournament
from Games import Game
from SaveAndRestore import SaveAndRestore
from Teams import Team, EmptyTeam, Player
from PdfGenerator import PdfGenerator
import DataContainers as DataContainers

class MatchGui(tk.Toplevel):

    def __init__(self, master, tournament, currentMatches):
        tk.Toplevel.__init__(self, master)
        self.tournament = tournament
        self.currentMatches = currentMatches
        self.title("List Reorder")
        self.displayList()

    def displayList(self, frame=None):
        # TODO: Clean this up
        if frame:    
            frame.destroy()
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)
        matches = self.currentMatches
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
        reorderButton = tk.Button(frame, text="Refresh Order", command=lambda: self.updateOrder(matches, frame))
        reorderButton.grid(
            column=1, row=200, padx=5, pady=10
        )
        closeToSaveMsg = tk.Label(frame, text="Close this window to accept gameorder.", fg='#f00', font=12)
        closeToSaveMsg.grid(column=1, row=201, padx=5, pady=15)

    def updateOrder(self, list, frame):
        list = sorted(list, key=lambda x: x[-1].get())
        matches = [match[:-1] for match in list]
        self.currentMatches = matches
        self.__addReferees()
        self.displayList(frame)   

    def __addReferees(self):
        sortedReferees = sorted(self.tournament.teams, key=lambda team: team.gamesRefed)
        for index, match in enumerate(self.currentMatches):
            for ref in sortedReferees:
                currentMatch = [match[0].name, match[1].name]
                if index<len(self.currentMatches)-1:
                    nextMatch = self.currentMatches[index+1]
                    nextMatch = [nextMatch[0].name, nextMatch[1].name]
                else:
                    nextMatch = []
                if index > 0:
                    previousMatch = self.currentMatches[index-1]
                    previousMatch = [previousMatch[0].name, previousMatch[1].name]
                else:
                    previousMatch = []
                if (ref.name not in currentMatch) \
                    and (ref.name not in nextMatch) \
                    and (ref.name not in previousMatch):
                    match[2] = ref
                    sortedReferees.remove(ref)
                    break

class SwissTournament(Tournament):

    def __init__(self, fileName = None):
        super().__init__(fileName)
        self.teams = self.joinTeamsToOneGroup()
        self.startTimes = self.restored["startTimes"]
        self.endTimes = self.restored["endTimes"]
        self.rounds = self.restored["rounds"]
        self.timePerGroupGame = self.restored["timePerGroupGame"]
        self.timePerFinalGame = self.restored["timePerFinalGame"]
        self.breakBetweenRounds = self.restored["breakBetweenRounds"]
        self.emptyTeam = EmptyTeam()
        self.currentRound = self.restored["currentRound"]
        self.gamesPerRound = int(len(self.teams)/2)
        if self.currentRound <= self.rounds and len(self.games)>0:
            self.generateGames(finalsOnly=True)

    def joinTeamsToOneGroup(self):
        oneGroup = []
        for group in self.teams:
            oneGroup += group
        return oneGroup

    def generateGames(self, mainWindow = None, finalsOnly=False):
        numberOfGamesPerRound = self.gamesPerRound
        sortedTable = self.sortGroups([self.teams])[0]
        if not finalsOnly:
            for roundNumber in range(self.currentRound, self.rounds):
                firstGameOfRound = roundNumber*numberOfGamesPerRound
                if self.previousRoundFinished(roundNumber, numberOfGamesPerRound) or roundNumber == 0:
                    self.__currentMatches = self.getTeamsToMatch(sortedTable)
                    self.__addReferees()
                    self.getMatchOrder(mainWindow)
                    self.__addGamesToList(firstGameOfRound, numberOfGamesPerRound)
                else:
                    self.__currentMatches = self.getTeamsToMatch(sortedTable, emptyMode=True)
                    self.__addGamesToList(firstGameOfRound, numberOfGamesPerRound)
        self.__addFinals(numberOfGamesPerRound, sortedTable)
        self.__addGamesToList((self.rounds)*numberOfGamesPerRound, numberOfGamesPerRound)
        self.saveFile()
    
    def __addFinals(self, numberOfGamesPerRound, sortedTable):
        self.__currentMatches = []
        if self.previousRoundFinished(self.rounds, numberOfGamesPerRound):
            for index in range(numberOfGamesPerRound):
                match = []
                for i in range(2):
                    place = (numberOfGamesPerRound-index)*2-1+i
                    match.append(sortedTable[place-1])
                self.__currentMatches.append(match)
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
            if finals or ". Platz" in game[1].name:
                gameTime = self.timePerFinalGame
            else:
                gameTime = self.timePerGroupGame
            if len(self.games)>0 and index == 0:
                currentDateTime = datetime.datetime.strptime(self.games[firstGameOfRound-1].time, '%H:%M')
                currentDateTime += datetime.timedelta(minutes=(self.breakBetweenRounds+gameTime))
                currentDay = self.games[firstGameOfRound-1].day
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
            currentDateTime += datetime.timedelta(minutes=(gameTime))
        if len(self.games) <= firstGameOfRound:
            self.games += round
        else:
            i = 0
            for gameIndex in range(firstGameOfRound,firstGameOfRound+gamesPerRound):
                self.games[gameIndex] = round[i]
                i += 1

    def getTeamsToMatch(self, sortedTable, emptyMode=False):
        matches = []
        selectedTeams = []
        if emptyMode:
            for index in range(int(len(sortedTable)/2)):
                matches.append([self.emptyTeam, self.emptyTeam, self.emptyTeam])
            return matches
        for teamAIndex in range(len(sortedTable)-1):
            if not teamAIndex in selectedTeams:
                for teamBIndex in range(teamAIndex+1, len(sortedTable)):
                    if not self.checkIfGameExists(sortedTable[teamAIndex], sortedTable[teamBIndex]) \
                        and teamBIndex not in selectedTeams:
                        matches.append([sortedTable[teamAIndex], sortedTable[teamBIndex], ""])
                        selectedTeams.append(teamBIndex)
                        selectedTeams.append(teamAIndex)
                        break
        if len(matches) < self.gamesPerRound:
            for teamAIndex in range(len(sortedTable)-1):
                if teamAIndex not in selectedTeams:
                    for teamBIndex in range(teamAIndex+1, len(sortedTable)):
                        if teamBIndex not in selectedTeams:
                            matches.append([sortedTable[teamAIndex], sortedTable[teamBIndex], ""])
                            selectedTeams.append(teamBIndex)
                            selectedTeams.append(teamAIndex)
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
    
    def getMatchOrder(self, mainwindow):
        getMatches = MatchGui(mainwindow, self, self.__currentMatches)
        if mainwindow:
            tk.Toplevel.wait_window(mainwindow, getMatches)
        self.__currentMatches = getMatches.currentMatches
        
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
    
    def getScorerTable(self):
        scorers = []
        for team in self.teams:
            scorers += team.getScorers()
        scorers = sorted(scorers, key=lambda x: x[-1], reverse=True)
        return scorers

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
            "timePerGroupGame": self.timePerGroupGame,
            "timePerFinalGame": self.timePerFinalGame,
            "breakBetweenRounds": self.breakBetweenRounds,
            "days": self.days,
            "dates": self.dates,
            "currentRound": self.currentRound
        }
        if "_Round-" in self.fileName.name:
            filename = self.fileName.name[:self.fileName.name.index("_Round-")]
            filename += "_Round-" + str(self.currentRound) + ".json"
        else:
            filename = self.fileName.name[:-5] + "_Round-" + str(self.currentRound) + ".json"
        SaveAndRestore.save(filename, dict)
        
    def generatePdf(self):
        gamesPerRound = self.gamesPerRound
        generator = PdfGenerator(self, True, gamesPerRound)
        generator.generateTexFile()

    def getTeamWithPlayers(self):
        teamsWithPlayers = {}
        for team in self.teams:
            players = team.getPlayerNumberAndNameList()
            teamsWithPlayers[team.name] = players 
        return teamsWithPlayers
    
    def setPlayerNames(self, team, players):
        for teamObj in self.teams:
            if teamObj.name == team:
                for player in players:
                    player_found = False
                    for teamPlayer in teamObj.players:
                        try:
                            if teamPlayer.number == int(player['number']):
                                teamPlayer.name = player['name']
                                player_found = True
                                break
                        except ValueError:
                            pass
                    if not player_found and player['number'] != '' and player['name'] != '':
                        teamObj.players.append(
                            Player(
                                player['number'],
                                player['name'],
                                0,
                                0,
                                0,
                                0,
                                teamObj.name
                            )
                        )
                    

if __name__ == "__main__":
    inputFile = None
    parser = argparse.ArgumentParser(
                    prog='SwissTournament',
                    description='Generate Table dynamically for a swiss tournament' +\
                        " with referees",
                    epilog='Text at the bottom of help')
    
    parser.add_argument("--input_file", dest="inputFile", 
                        help="Specify an input file that will be loaded at startup.")
    args = parser.parse_args()
    
    if args.inputFile:
        inputFile = DataContainers.Filename(args.inputFile)

    swissTournament = SwissTournament(fileName=inputFile)
    swissTournament.generateGames()
    swissTournament.saveFile()
    swissTournament.generatePdf()
