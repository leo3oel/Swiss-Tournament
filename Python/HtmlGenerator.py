import jinja2, os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webbrowser
import threading
import subprocess

class GenerateAndDisplayHtml:

    def __init__(self, tournament, swiss, gamesPerRound=1):
        self.templatePath = os.path.join(os.getcwd(), "Website", "template.html")
        self.templatePathMobile = os.path.join(os.getcwd(), "Website", "templateMobile.html")
        self.outputPath = os.path.join(os.getcwd(), "Website", "plan.html")
        self.outputPathMobile = os.path.join(os.getcwd(), "Website", "planMobile.html")
        self.tournament = tournament
        self.swiss = swiss
        self.gamesPerRound = gamesPerRound
        with open(self.templatePath) as file:
            self.template = jinja2.Template(file.read())
        with open(self.templatePathMobile) as file:
            self.templateMobile = jinja2.Template(file.read())

    def generateHtmlFile(self):
        table = self.__getFormatedTable()
        gamesPerDay = self.__formatGamesForPrinting(self.tournament.games)
        scorers = self.__getScorerTable()
        output = self.template.render(table=table, days=self.tournament.days, games=gamesPerDay, gamesPerRound=self.tournament.gamesPerRound, scorers=scorers)
        with open(self.outputPath, 'w', encoding="utf8") as file:
            file.write(output)

    def generateHtmlFileMobile(self):
        table = self.__getFormatedTable()
        gamesPerDay = self.__formatGamesForPrinting(self.tournament.games)
        output = self.templateMobile.render(table=table, days=self.tournament.days, games=gamesPerDay, gamesPerRound=self.tournament.gamesPerRound)
        with open(self.outputPathMobile, 'w', encoding="utf8") as file:
            file.write(output)
        result = self.get_current_git_branch()
        result
        if self.get_current_git_branch() == "tournament-2025":
            try: 
                returnValue = subprocess.check_output(["git", "diff", "--exit-code", "Website/planMobile.html"], stderr=subprocess.STDOUT)
                returnValue
            except:
                subprocess.call(["git", "commit", "-m", 
                                "auto commit: plan updated", "Website/planMobile.html"])
                subprocess.call(["git", "push", "origin", "tournament-2025"])

    def get_current_git_branch(self):
        try:
            result = subprocess.run(["git", "branch", "--show-current"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print("Error:", result.stderr)
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def __getFormatedTable(self):
        sortedTable = self.tournament.sortGroups([self.tournament.teams])[0]
        teams = []
        for team in sortedTable:
            teamdict = {
                "name": team.name,
                "numberOfGames": team.getNumberOfGames(),
                "points": team.getPoints(),
                "plusGoals": team.getPlusGoals(),
                "minusGoals": team.getMinusGoals(),
                "goalDiff": team.getGoalDiff()
            }
            teams.append(teamdict)
        return teams
    
    def __formatGamesForPrinting(self, games):
        days = []
        for number, game in enumerate(games):
            gameNumber = number + 1
            while game.day >= len(days):
                days.append([])
            gameDict = {
                "number": gameNumber,
                "time": game.time,
                "teamA": self.__getTeamName(game.teamA),
                "teamB": self.__getTeamName(game.teamB),
                "scoreA": self.__getScore(game.score[0]),
                "scoreB": self.__getScore(game.score[1]),
                "referee": self.__getTeamName(game.referee)
            }
            days[game.day].append(gameDict)
        return days
    
    def __getTeamName(self, team):
        if type(team) is str:
            return team
        return team.name

    def __getScore(self, score):
        if score>=0:
            return score
        return ""
    
    def __getScorerTable(self):
        table = self.tournament.getScorerTable()[:10]
        scorers = []
        for scorer in table:
            scorerDict = {
                "name": scorer[1],
                "team": scorer[2],
                "number": scorer[0],
                "goals": scorer[3]
            }
            scorers.append(scorerDict)
        return scorers

    def startServer(self):
        self.closeServer()
        self.httpd = HTTPServer(("", 8000), SimpleHTTPRequestHandler)   
        thread = threading.Thread(target=self.httpd.serve_forever);
        thread.start();

    def closeServer(self):
        if hasattr(self, "httpd"):
            self.httpd.shutdown()

    def openPage(self):
        webbrowser.open("http://localhost:8000/Website/plan.html")

if __name__ == '__main__':
    generator = GenerateAndDisplayHtml(None, None)
    generator.startServer()
    generator.openPage()
    input = input()
