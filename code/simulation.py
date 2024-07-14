from random import random


match_scores_occurence = {}
set_scores_occurence = {}

class SimStats:
    """SimStats handles accumulation of statistics across multiple completed games."""

    def __init__(self, nameA, nameB):
        """Create a new accumulator for a series of games."""
        self.winsA = 0
        self.winsB = 0
        self.number_of_sets = 0
        self.nameA = nameA
        self.nameB = nameB

    def update(self, aMatch):
        """Determine the outcome of aGame and updates statistics."""
        a, b = aMatch.getMatches()
        if a > b:
            self.winsA += a
        else:
            self.winsB += b
        self.number_of_sets = self.number_of_sets +  int(aMatch.getSetsNumber())

    def printReport(self):
        """Prints a report of aGame."""
        n = self.winsA + self.winsB
        print("Summary of ", n, " games: \n")
        print("        wins (%total)")
        print("------------------------")
        self.printLine(self.nameA, self.winsA, n)
        self.printLine(self.nameB, self.winsB, n)

    def printLine(self, label, wins, n):
        """Prints one line for the report."""
        template = "Player {0}:{1:5}   ({2:5.1%})"
        print(template.format(label, wins, float(wins) / n))


class TennisGame:
    """A TennisGame represents a game in progress. A game has two players and keeps track of which one is currently serving."""

    def __init__(self, firstserveA, winsfirstA, winssecondA, aceA, dfA, firstserveB, winsfirstB, winssecondB, aceB,
                 dfB, nameA, nameB, sets_in_a_match):
        """Create a new game having players with all given probabilities."""
        self.playerA = Player(firstserveA, winsfirstA, winssecondA, aceA, dfA, nameA)
        self.playerB = Player(firstserveB, winsfirstB, winssecondB, aceB, dfB, nameB)
        self.server = self.playerA
        self.notserver = self.playerB
        self.sets_in_a_match = sets_in_a_match
        self.number_of_sets = 0

    def playGame(self):
        """Play a game to completion."""
        while not self.gameisOver():
            if self.server.winsServe():
                self.server.incPoint()
            else:
                self.notserver.incPoint()
        a, b = self.getPoints()
        if a > 4 or b > 4:
            if a > b:
                a = "Win"
                b = 40
            else:
                a = 40
                b = "Win"
        else:
            if a == 1:
                a = 15
            elif a == 2:
                a = 30
            elif a == 3:
                a = 40
            elif a == 4:
                a = "Win"
            if b == 1:
                b = 15
            elif b == 2:
                b = 30
            elif b == 3:
                b = 40
            elif b == 4:
                b = "Win"
        print(f"Game {a}:{b} |", f" Serve: {self.server}")
        self.gameUpdate()
        self.serveChange()

    def playSet(self):
        """Play a set to completion."""
        while not self.setisOver():
            self.playGame()
        if self.istieBreak() == True:
            self.tieBreak()
            a, b = self.getPoints()
            c, d = self.getGames()
            print(f"Set {c}:{d}|", f" Tiebreak: {a}:{b}")
            self.playerA.points = 0
            self.playerB.points = 0
            self.setUpdate()
        else:
            c, d = self.getGames()
            print(f"Set {c}:{d}")
            self.setUpdate()
        if f"{c}:{d}" not in set_scores_occurence:
            set_scores_occurence[f"{c}:{d}"] = 1
        else:
            set_scores_occurence[f"{c}:{d}"] += 1
        self.number_of_sets += 1


    def playMatch(self):
        """Play a match to completion."""
        while not self.matchisOver():
            self.playSet()
        a, b = self.getSets()
        print(f"Match {a}:{b}")
        print("")
        print("")
        self.matchUpdate()
        if f"{a}:{b}" not in match_scores_occurence:
            match_scores_occurence[f"{a}:{b}"] = 1
        else:
            match_scores_occurence[f"{a}:{b}"] += 1

    def serveChange(self):
        """Changes the person serving serve."""
        if self.server == self.playerA:
            self.server = self.playerB
            self.notserver = self.playerA
        else:
            self.server = self.playerA
            self.notserver = self.playerB

    def istieBreak(self):
        """Returns True if a tiebreak is required, False otherwise."""
        a, b = self.getGames()
        if a == b == 6:
            return True
        else:
            return False

    def tieBreak(self):
        """Plays a tiebreak between two players."""
        x = self.server
        if self.server.winsServe():
            self.server.incPoint()
        else:
            self.notserver.incPoint()
        k = 0
        while not self.tiebreakOver():
            k += 1
            if k % 2 == 1:
                self.serveChange()
            if self.server.winsServe():
                self.server.incPoint()
            else:
                self.notserver.incPoint()
        if x == self.server:
            self.serveChange()
        self.tieBreakUpdate()

    def getPoints(self):
        """Returns the current points of player A and player B."""
        return self.playerA.getPoint(), self.playerB.getPoint()

    def getGames(self):
        """Returns the current games of player A and player B."""
        return self.playerA.getGame(), self.playerB.getGame()

    def getSets(self):
        """Returns the current sets of player A and player B."""
        return self.playerA.getSet(), self.playerB.getSet()

    def getMatches(self):
        """Returns the current matches of player A and player B."""
        return self.playerA.getMatch(), self.playerB.getMatch()

    def getSetsNumber(self):
        return self.number_of_sets

    def tiebreakOver(self):
        """Returns True if tiebreak is finished, False otherwise."""
        a, b = self.getPoints()
        if a > b and b + 1 < a and a >= 7:
            return True
        if a < b and a + 1 < b and b >= 7:
            return True
        else:
            return False

    def gameisOver(self):
        """Returns True if game is finished, False otherwise."""
        a, b = self.getPoints()
        if a > b and b + 1 < a and a >= 4:
            return True
        elif a < b and a + 1 < b and b >= 4:
            return True
        else:
            return False

    def setisOver(self):
        """Returns True if set is finished, False otherwise."""
        a, b = self.getGames()
        if a > b and b + 1 < a and a >= 6:
            return True
        elif a < b and a + 1 < b and b >= 6:
            return True
        elif a == b == 6:
            return True
        else:
            return False

    def matchisOver(self):
        """Returns True if match is finished, False otherwise."""
        a, b = self.getSets()
        sets_in_a_match = self.sets_in_a_match
        return a == sets_in_a_match or b == sets_in_a_match

    def tieBreakUpdate(self):
        """Updates the score after tiebreak."""
        a, b = self.getPoints()
        if a > b:
            self.playerA.incGame()
        if b > a:
            self.playerB.incGame()

    def gameUpdate(self):
        """Updates the score after a game."""
        a, b = self.getPoints()
        if a > b:
            self.playerA.incGame()
            self.playerA.points = 0
            self.playerB.points = 0
        if b > a:
            self.playerB.incGame()
            self.playerA.points = 0
            self.playerB.points = 0

    def setUpdate(self):
        """Updates the score after a set."""
        a, b = self.getGames()
        if a > b:
            self.playerA.incSet()
            self.playerA.games = 0
            self.playerB.games = 0
        if b > a:
            self.playerB.incSet()
            self.playerA.games = 0
            self.playerB.games = 0

    def matchUpdate(self):
        """Updates the score after a match."""
        a, b = self.getSets()
        if a > b:
            self.playerA.incMatch()
            self.playerA.sets = 0
            self.playerB.sets = 0
        if b > a:
            self.playerB.incMatch()
            self.playerA.sets = 0
            self.playerB.sets = 0


class Player:
    """A player that keeps track of service win probability and score."""

    def __init__(self, firstserve, winsfirst, winssecond, ace, df, name):
        """Create a player with this probability to win a serve."""
        self.firstserve = firstserve
        self.winsfirst = winsfirst
        self.winssecond = winssecond
        self.ace = ace
        self.df = df
        self.name = name
        self.points = 0
        self.games = 0
        self.sets = 0
        self.matches = 0

    def winsServe(self):
        """Returns a boolean that is true with determined probability."""
        x = random()
        if x <= self.firstserve:
            if random() <= self.ace:
                return True
            else:
                if random() <= self.winsfirst:
                    return True
                else:
                    return False
        else:
            if random() > self.df:
                return False
            else:
                if random() <= self.winssecond:
                    return True
                else:
                    return False

    def incPoint(self):
        """Add a point to this player's points."""
        self.points += 1

    def incGame(self):
        """Add a point to this player's games."""
        self.games += 1

    def incSet(self):
        """Add a point to this player's sets."""
        self.sets += 1

    def incMatch(self):
        self.matches += 1

    def getPoint(self):
        """Returns this player's current points."""
        return self.points

    def getGame(self):
        """Returns this player's current games."""
        return self.games

    def getSet(self):
        """Returns this player's current sets."""
        return self.sets

    def getMatch(self):
        """Returns this player's current matches."""
        return self.matches

    def __str__(self):
        return self.name
