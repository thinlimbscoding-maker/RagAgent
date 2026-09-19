class School:

    def __init__(self, pcmMarks):
        self.pcmMarks = pcmMarks

    def firstClass(self):

        if self.pcmMarks >= 60:
            return True
        else:
            return False


class College:

    def __init__(self, airRank):
        self.airRank = airRank

    def cutoff(self):
        if self.airRank < 200000:
            return True
        else:
            return False


class Job(School, College):
    def __init__(self, pcmMarks, airRank, pckg):
        School.__init__(self, pcmMarks)
        College.__init__(self, airRank)

        self.pckg = pckg

    def placment(self):
        if self.firstClass() and self.cutoff():
            return f"hired with ${self.pckg}"
        else:
            return "better luck next time "


myCarrer = Job(10, 10000, "12Lpa")
print(myCarrer.placment())
