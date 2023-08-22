class Game:

    def __init__(self, group, time, day, teamA, teamB, referee, score):
        self.group = group
        self.time = time
        self.day = day
        self.teamA = teamA
        self.teamB = teamB
        self.referee = referee
        self.score = score

    def setScore(self, teamA, teamB):
        self.score = [teamA, teamB]

    def export(self):
        dict = {
            "group": int(self.group),
            "time": self.time,
            "day": self.day,
            "teamA": self.teamA.name,
            "teamB": self.teamB.name,
            "referee": self.referee.name,
            "score": self.score
        }
        return dict
