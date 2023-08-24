"""
A Game of the Tournament
"""

class Game:

    def __init__(self, group, time, day, teamA, teamB, referee, score, scorer):
        self.group = group
        self.time = time
        self.day = day
        self.teamA = teamA
        self.teamB = teamB
        self.referee = referee
        self.score = score
        self.scorer = scorer

    def setScore(self, teamA, teamB, scorerA, scorerB):
        self.score = [teamA, teamB]
        self.scorer = [scorerA, scorerB]

    def export(self):
        dict = {
            "group": int(self.group),
            "time": self.time,
            "day": self.day,
            "teamA": self.teamA.name,
            "teamB": self.teamB.name,
            "referee": self.referee.name,
            "score": self.score,
            "scorer": self.scorer
        }
        return dict
