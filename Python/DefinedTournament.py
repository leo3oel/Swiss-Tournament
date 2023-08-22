"""
Tournament Games will be read from List
Use this for Group Tournaments, etc
WIP
"""
from Tournament import Tournament
from Games import Game

class DefinedTournament(Tournament):

    def __init__(self):
        super().__init__()
        self.games = self.__getGames(self.restored["games"], self.restored["days"])

    def __getGames(self, restoredGames, restoredDays, getIntermediateWithTeams = False, getFinalsWithTeams = False):
        games = []
        for game in restoredGames:
            if game["group"] < 0:
                if game["group"] == -1:
                    self.__getIntermediate(game, games, restoredDays, getIntermediateWithTeams)
                elif game["group"] == -2:
                    self.__getFinals(game, games, restoredDays, getFinalsWithTeams)
            else:
                group = chr(ord('A')+game["group"])
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        self.teams[game["group"]][game["teamA"]],
                        self.teams[game["group"]][game["teamB"]],
                        self.teams[game["group"]][game["referee"]],
                        game["score"],
                    )
                )
        return games

    def __getIntermediate(self, game, games, restoredDays, withTeams):
            group = "Z"
            if self.__alreadyGamesPlayed() and withTeams:
                sortedGroups = self.sortGroups(self.teams)
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        sortedGroups[game["teamA"][0]][game["teamA"][1]],
                        sortedGroups[game["teamB"][0]][game["teamB"][1]],
                        sortedGroups[game["referee"][0]][game["referee"][1]],
                        game["score"],
                    )
                )
            else:
                groupTeamA = chr(ord('A')+game["teamA"][0])
                groupTeamB = chr(ord('A')+game["teamB"][0])
                groupTeamRef = chr(ord('A')+game["referee"][0])
                stringTeamA = f"{game['teamA'][1]+1}. Gruppe {groupTeamA}"
                stringTeamB = f"{game['teamB'][1]+1}. Gruppe {groupTeamB}"
                stringTeamRef = f"{game['referee'][1]+1}. Gruppe {groupTeamRef}"
                games.append(
                    Game(
                        group,
                        game["time"],
                        game["day"],
                        stringTeamA,
                        stringTeamB,
                        stringTeamRef,
                        game["score"],
                    )
                )

    def __getFinals(self, game, games, restoredDays, withTeams):
        group = f"Pl. {game['teamA']+1}"    
        if withTeams:
            combinedGroup = []
            for group in self.teams:
                combinedGroup += group
            sortedGroup = self.sortGroups([combinedGroup])[0]
            games.append(
                Game(
                    group,
                    game["time"],
                    game["day"],
                    sortedGroup[game["teamA"]],
                    sortedGroup[game["teamB"]],
                    sortedGroup[game["referee"]],
                    game["score"],
                )
            )
        else:
            teamAStr = f"Platz {game['teamA']+1}"
            teamBStr = f"Platz {game['teamB']+1}"
            refereeStr = f"Platz {game['referee']+1}"
            games.append(
                Game(
                    group,
                    game["time"],
                    game["day"],
                    teamAStr,
                    teamBStr,
                    refereeStr,
                    game["score"],
                )
            )

    def __alreadyGamesPlayed(self):
        for group in self.teams:
            for team in group:
                if team.getPoints()>0:
                    return True
        return False
