import jinja2, os, subprocess

from DefinedTournament import DefinedTournament

class PdfGenerator:

    def __init__(self, tournament, swiss):
        self.templatePath = os.path.join(os.getcwd(), "PdfPlan", "template.tex")
        self.outputPath = os.path.join(os.getcwd(), "PdfPlan", "spielplan.tex")
        self.tournament = tournament
        self.swiss = swiss
        with open(self.templatePath) as file:
            self.template = jinja2.Template(file.read())

    def generateTexFile(self):
        teamNames = self.__formatGroupsForPrinting(self.tournament.teams)
        games = self.__formatGamesForPrinting(self.tournament.games)
        output = self.template.render(teamNames=teamNames, groups=self.tournament.teams, days=self.tournament.days, games=games, swiss=self.swiss)
        with open(self.outputPath, 'w') as file:
            file.write(output)
        cwd = os.getcwd()
        os.chdir(os.path.dirname(self.outputPath))
        subprocess.run(["lualatex", self.outputPath])
        subprocess.run(["lualatex", self.outputPath])
        os.chdir(cwd)
        

    def __formatGroupsForPrinting(self, teams):
        teamNames = []
        firstLine = []
        if self.swiss:
            firstLine.append("Teams")
            teams = [teams]
        else:
            for iterator in range(len(teams)):
                firstLine.append("Gruppe " + chr(ord('A')+iterator))
        firstLine[-1] = firstLine[-1] + r'\\\hline\hline'
        teamNames.append(" & ".join(firstLine))
        for iterator in range(len(teams[0])):
            line = []
            for group in teams:
                line.append(group[iterator].name)
            teamNames.append(" & ".join(line))
            if iterator < len(teams[0])-1:
                teamNames[-1] += "\\\\\\hline"
        return teamNames
    
    def __formatGamesForPrinting(self, games):
        days = []
        for number, game in enumerate(games):
            gameNumber = number + 1
            while game.day>=len(days):
                days.append([])
            formatedString = str(gameNumber) + " & "
            formatedString += game.time + " & "
            if not self.swiss:
                formatedString += game.group + " & "
            if type(game.teamA) is str:
                formatedString += game.teamA + " & "
            else:
                formatedString += game.teamA.name + " & "
            if type(game.score[0]) is int:
                formatedString += str(game.score[0]) + " & "
                formatedString += ":" + " & "
                formatedString += str(game.score[1]) + " & "
            else:
                formatedString += " & : & &"
            if type(game.teamB) is str:
                formatedString += game.teamB + " & "
            else:
                formatedString += game.teamB.name + " & "
            if type(game.referee) is str:
                formatedString += game.referee
            else:
                formatedString += game.referee.name
            formatedString += r'\\'
            days[game.day].append(formatedString)
        for day in days:
            day[-1] = day[-1][:-2]
        return days



if __name__ == '__main__':
    generator = PdfGenerator()
    generator.generateTexFile()