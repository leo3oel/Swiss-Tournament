"""
Graphical Interface;
Also main Program to start a Tournament
Currently only starts SwissTournament
"""
import tkinter as tk

from SwissTournament import SwissTournament

class GamesWindow:

    def __init__(self):
        pass

class TableWindow(tk.Tk):

    def __init__(self, tournament):
        tk.Tk.__init__(self)
        self.title = "Tournament Table"
        self.__tableFrame = tk.Frame(self)
        self.__createWindow()
        self.mainloop()

    def refreshTable(self):
        self.__tableFrame.destroy()
        self.__tableFrame = tk.Frame(self)

class EntryWindow(tk.Tk):

    __gameNumber = 0

    def __init__(self, tournament):
        tk.Tk.__init__(self)
        self.title = "Game Entry"
        self.__tournament = tournament
        self.__currentGameFrame = tk.Frame(self)
        self.__createWindow()
        self.mainloop()

    def __createWindow(self):
        self.__createCurrentGameFrame()
        self.__createButtons()

    def __createCurrentGameFrame(self, scoreA=None, scoreB=None):
        gamesOfRound = self.__tournament.generateGamesOfRound(self.__tournament.currentRound)
        if scoreA == None:
            game = gamesOfRound[self.__gameNumber]
            scoreA = game.score[0]
            scoreB = game.score[1]
        self.__currentGameFrame.destroy()
        self.__currentGameFrame = tk.Frame(self)
        self.__currentGameFrame.grid(row=0, column=0, columnspan=4)
        self.__addGameToFrame(gamesOfRound[self.__gameNumber], scoreA, scoreB)

    def __createButtons(self):
        previousGameBt = tk.Button(self, text="Previous Game", command=lambda: self.__changeGame(-1))
        previousGameBt.grid(row=1,column=0, padx=5, pady=5)
        createPdf = tk.Button(self, text="Create PDF", command=self.__createPDF)
        createPdf.grid(row=1,column=1, padx=5, pady=5)
        saveGameBt = tk.Button(self, text="Save Game", command=self.__saveGame)
        saveGameBt.grid(row=1,column=2, padx=5, pady=5)
        nextGameBt = tk.Button(self, text="Next Game", command=lambda: self.__changeGame(1))
        nextGameBt.grid(row=1,column=3, padx=5, pady=5)

    def __addGameToFrame(self, game, scoreA, scoreB):
        teamAName = tk.Label(self.__currentGameFrame, text=game.teamA.name)
        teamAName.grid(row=0,column=0, padx=5, pady=20)
        teamBName = tk.Label(self.__currentGameFrame, text=game.teamB.name)
        teamBName.grid(row=0,column=1, padx=5, pady=20)
        teamAScore = tk.Label(self.__currentGameFrame, text=str(scoreA))
        teamAScore.grid(row=1,column=0, padx=5, pady=5)
        teamAScore = tk.Label(self.__currentGameFrame, text=str(scoreB))
        teamAScore.grid(row=1,column=0, padx=5, pady=5)
        
    # def __createPlayerNumberEntry(self, score):
    #     entryFields = []
    #     if type(score) is not int:
    #         return entryFields
    #     for index in range(score):

    #         entryFields.append(
    #             tk.Entry(self.__currentGameFrame, textvariable=)
    #         )
        

    def __changeGame(self, relativIndex):
        self.__gameNumber += relativIndex
        if self.__gameNumber<0:
            self.__gameNumber == 0
        if self.__gameNumber>=self.__tournament.gamesPerRound:
            self.__gameNumber = self.__tournament.gamesPerRound
        self.__createCurrentGameFrame()

    def __saveGame(self):
        # TODO: Save game
        self.__tournament.saveFile()

    def __createPDF(self):
        self.__tournament.generatePdf()

class MainGui:

    def __init__(self):
        tournament = SwissTournament()
        if len(tournament.games) == 0:
            tournament.generateGames()
        EntryWindow(tournament)

if __name__ == "__main__":
    MainGui()
