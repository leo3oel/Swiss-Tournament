from tkinter import filedialog

from SaveAndRestore import SaveAndRestore
from Teams import Team
from Games import Game

class Tournament:

    def __init__(self, fileName):
        restored = SaveAndRestore.restore(fileName)
        self.teams = self.__getTeams(restored["teams"])
        self.games = self.__getGames(restored["games"], restored["days"])

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
    
    def __getGames(self, restoredGames, restoredDays):
        games = []
        for game in restoredGames:
            if game["group"] < 0:
                pass
            else:
                group = chr(ord('A')+game["group"])
                games.append(
                    Game(
                        group,
                        game["time"],
                        restoredDays[game["day"]],
                        self.teams[game["group"]][game["teamA"]],
                        self.teams[game["group"]][game["teamB"]],
                        self.teams[game["group"]][game["referee"]],
                        game["score"],
                    )
                )
        return games




if __name__ == "__main__":
    filename = filedialog.askopenfile()
    main = Tournament(filename)