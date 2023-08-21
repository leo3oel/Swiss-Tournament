import openpyxl

class Report:

    def __init__(self, game, dates, templatePath):
        self.__date = dates[game.day]
        self.__teamA = game.teamA
        self.__teamB = game.teamB
        self.__referee = game.referre.name
        self.__time = game.time
        self.__templatePath = templatePath

    def generateReport(self):
        template = openpyxl.load_workbook(self.__templatePath)
        sheet = template.active 
        sheet.cell(row=7, column=3).value = self.__time
        sheet.cell(row=10, column=1).value = self.__date
        sheet.cell(row=12, column=4).value = self.__referee
        sheet.cell(row=22, column=2).value = self.__teamA.name
        sheet.cell(row=22, column=6).value = self.__teamB.name
        self.enterPlayers(sheet, self.__teamA.players, )


    def enterPlayers(self, sheet, players, startCell):
        currentCell = startCell
        for player in players:
            sheet.cell(row=currentCell[0], column=currentCell[1]).value = player[0]
            sheet.cell(row=currentCell[0], column=currentCell[1]+1).value = player[1]
            sheet.cell(row=currentCell[0], column=currentCell[1]+2).value = player[2]
            currentCell[0] += 1