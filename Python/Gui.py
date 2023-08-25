"""
Graphical Interface;
Also main Program to start a Tournament
Currently only starts SwissTournament
"""
import tkinter as tk
from tkinter import messagebox as msgbx

from SwissTournament import SwissTournament
from HtmlGenerator import GenerateAndDisplayHtml

class EntryWindow(tk.Tk):

    def __init__(self, tournament):
        tk.Tk.__init__(self)
        self.title("Game Entry")
        self.__gameNumber = 0
        self.__tournament = tournament
        if len(tournament.games) == 0:
            tournament.generateGames(self)
        self.__currentGameFrame = tk.Frame(self)
        self.__htmlGenerator = GenerateAndDisplayHtml(self.__tournament, True, self.__tournament.gamesPerRound)
        self.__htmlGenerator.generateHtmlFile()
        self.__htmlGenerator.startServer()
        self.protocol("WM_DELETE_WINDOW", self.onclosing)
        self.__htmlGenerator.openPage()
        self.__createWindow()
        self.mainloop()

    def __createWindow(self, scoreA=None, scoreB=None):
        gamesOfRound = self.__tournament.generateGamesOfRound(self.__tournament.currentRound)
        if scoreA == None:
            game = gamesOfRound[self.__gameNumber]
            scoreA = game.score[0]
            scoreB = game.score[1]
        sortedTeams = self.__tournament.sortGroups([self.__tournament.teams])[0]
        self.__currentGameFrame.destroy()
        self.__currentGameFrame = tk.Frame(self)
        self.__currentGameFrame.grid(row=0, column=0, columnspan=4)
        self.__addGameToFrame(gamesOfRound[self.__gameNumber], scoreA, scoreB)

    def __addGameToFrame(self, game, scoreA, scoreB):
        row = 0
        noteLabel = tk.Label(self.__currentGameFrame, text="NOTE: SET SCORE FIRST, THEN ENTER PLAYER NUMBERS")
        noteLabel.grid(row=row, column=0, padx=20, pady=0, columnspan=2)
        row += 1
        warningLabel = tk.Label(self.__currentGameFrame, text="NOTE: To set game score to number press 'add Goal' for each team")
        warningLabel.grid(row=row, column=0, padx=20, pady=0, columnspan=2)
        row += 1
        if scoreA != -1 and scoreB != -1:
            warningLabel.grid_remove()
        teamAName = tk.Label(self.__currentGameFrame, text=game.teamA.name)
        teamAName.grid(row=row,column=0, padx=5, pady=20)
        teamBName = tk.Label(self.__currentGameFrame, text=game.teamB.name)
        teamBName.grid(row=row,column=1, padx=5, pady=20)
        row += 1
        teamAScore = tk.Label(self.__currentGameFrame, text=self.__displayScore(scoreA))
        teamAScore.grid(row=row,column=0, padx=5, pady=5)
        teamBScore = tk.Label(self.__currentGameFrame, text=self.__displayScore(scoreB))
        teamBScore.grid(row=row,column=1, padx=5, pady=5)
        teamAEntrys = self.__createPlayerNumberEntry(scoreA, game.scorer[0], 0)
        teamBEntrys = self.__createPlayerNumberEntry(scoreB, game.scorer[1], 1)
        addGoalTeamABtn = tk.Button(self.__currentGameFrame, text="Add Goal Team A", command=lambda:self.__addGoal(0,[scoreA, scoreB]))
        addGoalTeamABtn.grid(row=200,column=0, padx=5, pady=5)
        addGoalTeamBBtn = tk.Button(self.__currentGameFrame, text="Add Goal Team B", command=lambda:self.__addGoal(1,[scoreA, scoreB]))
        addGoalTeamBBtn.grid(row=200,column=1, padx=5, pady=5)
        addGoalTeamABtn = tk.Button(self.__currentGameFrame, text="Delete Goal Team A", command=lambda:self.__deleteGoal(0,[scoreA, scoreB]))
        deleteGoalTeamABtn = tk.Button(self.__currentGameFrame, text="Delete Goal Team A", command=lambda:self.__deleteGoal(0,[scoreA, scoreB]))
        deleteGoalTeamABtn.grid(row=201,column=0, padx=5, pady=5)
        deleteGoalTeamBBtn = tk.Button(self.__currentGameFrame, text="Delete Goal Team B", command=lambda:self.__deleteGoal(1,[scoreA, scoreB]))
        deleteGoalTeamBBtn.grid(row=201,column=1, padx=5, pady=5)
        if scoreA == -1 or scoreB == -1:
            deleteGoalTeamABtn.grid_remove()
            deleteGoalTeamBBtn.grid_remove()
        previousGameBt = tk.Button(self, text="Previous Game", command=lambda: self.__changeGame(-1, game, scoreA, scoreB, teamAEntrys, teamBEntrys))
        previousGameBt.grid(row=1,column=0, padx=5, pady=5)
        createPdf = tk.Button(self, text="Create PDF", command=self.__createPDF)
        createPdf.grid(row=1,column=1, padx=5, pady=5)
        saveGameBt = tk.Button(self, text="Save Game", command=lambda: self.__saveGame(game, scoreA, scoreB, teamAEntrys, teamBEntrys))
        saveGameBt.grid(row=1,column=2, padx=5, pady=5)
        nextGameBt = tk.Button(self, text="Next Game", command=lambda: self.__changeGame(1, game, scoreA, scoreB, teamAEntrys, teamBEntrys))
        nextGameBt.grid(row=1,column=3, padx=5, pady=5)
        
    def __createPlayerNumberEntry(self, score, scorer, column):
        entryFields = []
        if score == -1:
            return entryFields
        for index in range(score):
            entry = tk.Entry(self.__currentGameFrame)
            entry.grid(row=10+index, column=column, padx=5, pady=5)
            entry.insert(0, str(self.__getScorer(scorer, index)))
            entryFields.append(entry)
        return entryFields
        
    def __displayScore(self, score):
        if score < 0:
            return "not played"
        return str(score)
    
    def __getScorer(self, scorer, index):
        try:
            scorerNumber = scorer[index]
            return scorerNumber
        except:
            return ""
        
    def __addGoal(self, team, scores):
        scores[team] += 1
        self.__createWindow(*scores)

    def __deleteGoal(self, team, scores):
        scores[team] -= 1
        self.__createWindow(*scores)

    def __changeGame(self, relativIndex, game, scoreA, scoreB, teamAEntrys, teamBEntrys):
        returnValue = self.__saveGame(game, scoreA, scoreB, teamAEntrys, teamBEntrys)
        if returnValue < 0:
            if msgbx.askyesno("Switch without Saving", "Switch without Saving"):
                pass
            else:
                return -1
        self.__gameNumber += relativIndex
        if self.__gameNumber<0:
            self.__gameNumber = 0
        if self.__gameNumber>=self.__tournament.gamesPerRound:
            if msgbx.askyesno("Generate next Round", "Are you sure you want to generate next round?\n" + 
                              "Input for this Round cannot be edited afterwards."
                              ):
                self.__gameNumber = 0
                self.__tournament.currentRound += 1
                self.__tournament.generateGames(self)
                self.__tournament.saveFile()
                self.__htmlGenerator.generateHtmlFile()
            else:
                self.__gameNumber -= 1
        self.__createWindow()

    def __saveGame(self, game, scoreA, scoreB, scorerA, scorerB):
        if not self.__checkIfParametersAreComplete(game, scoreA, scoreB, scorerA, scorerB):
            msgbx.showerror("Arguments missing", "Some values are empty")
            return -1
        if game.score[0] >= 0:
            self.__resetGame(game)
        game = self.__setNewValuesForGame(game, scoreA, scoreB, scorerA, scorerB)
        self.__saveToList(game)
        self.__tournament.saveFile()
        self.__htmlGenerator.generateHtmlFile()
        return 1

    def __setNewValuesForGame(self, game, scoreA, scoreB, scorerA, scorerB):
        game.score = [scoreA, scoreB]
        game.teamA.goalsPlus += scoreA
        game.teamA.goalsMinus += scoreB
        game.teamB.goalsPlus += scoreB
        game.teamB.goalsMinus += scoreA
        scorerANumbers = [int(scorer.get()) for scorer in scorerA]
        scorerBNumbers = [int(scorer.get()) for scorer in scorerB]
        game.scorer = [scorerANumbers, scorerBNumbers]
        for scorer in scorerA:
            self.__incrementScorer(game.teamA, int(scorer.get()))
        for scorer in scorerB:
            self.__incrementScorer(game.teamB, int(scorer.get()))
        self.__changeGameNumbersOfTeam(game, +1)
        game.referee.gamesRefed += 1
        return game

    def __saveToList(self, game):
        for index, gameInList in enumerate(self.__tournament.games):
            if gameInList.time == game.time and gameInList.day == game.day:
                gameInList = game

    def __checkIfParametersAreComplete(self, game, scoreA, scoreB, scorerA, scorerB):
        if not game:
            return False
        if scoreA < 0 or scoreB < 0:
            return False
        for scorer in scorerA:
            try:
                int(scorer.get())
            except:
                return False
        for scorer in scorerB:
            try:
                int(scorer.get())
            except:
                return False
        return True

    def __resetGame(self, game):
        self.__changeGameNumbersOfTeam(game, -1)
        game.teamA.goalsPlus -= (game.score[0])
        game.teamA.goalsMinus -= (game.score[1])
        game.teamB.goalsPlus -= (game.score[1])
        game.teamB.goalsMinus -= (game.score[0])
        for scorer in game.scorer[0]:
            self.__decrementScorer(game.teamA, scorer)
        for scorer in game.scorer[1]:
            self.__decrementScorer(game.teamB, scorer)
        refTeam = game.referee
        refTeam.gamesRefed -= 1

    def __changeGameNumbersOfTeam(self, game, value):
        if game.score[0] == game.score[1]:
            self.__changeGameNumberForType(game.teamA, "tie", value)
            self.__changeGameNumberForType(game.teamB, "tie", value)
        elif game.score[0] > game.score[1]:
            self.__changeGameNumberForType(game.teamA, "won", value)
            self.__changeGameNumberForType(game.teamB, "loss", value)
        elif game.score[0] < game.score[1]:
            self.__changeGameNumberForType(game.teamA, "loss", value)
            self.__changeGameNumberForType(game.teamB, "won", value)

    def __changeGameNumberForType(self, team, type, value):
        if type == "loss":
            team.numberOfLosses += value
        if type == "tie":
            team.numberOfTies += value
        if type == "won":
            team.numberOfWins += value

    def __incrementScorer(self, team, scorer):
        team.incrementGoalCountOfPlayer(scorer, 1)

    def __decrementScorer(self, team, scorer):
        team.incrementGoalCountOfPlayer(scorer, -1)

    def __createPDF(self):
        self.__tournament.generatePdf()

    def onclosing(self):
        self.__htmlGenerator.closeServer()

class MainGui:

    def __init__(self):
        tournament = SwissTournament()
        EntryWindow(tournament)

if __name__ == "__main__":
    MainGui()
