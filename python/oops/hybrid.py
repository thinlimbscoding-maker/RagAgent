class School:
    def __init__(self, pcmMarks, **restArg):
        self.pcmMarks = pcmMarks

    def firstClass(self):
        if self.pcmMarks > 60:
            return True
        else:
            return False


class College(School):
    def __init__(self, airRank, **restArg):
        super().__init__(**restArg)
        self.airRank = airRank

    def cutOff(self):
        if self.firstClass() and self.airRank < 200000:

            return True
        else:

            return False


class Certificate(School):
    def __init__(self, pythonTest, **restArg):
        super().__init__(**restArg)
        self.pythonTest = pythonTest

    def courseEligibilty(self):
        if self.firstClass() and self.pythonTest > 50:
            return True
        else:
            return False


class Placment(College, Certificate):
    def __init__(self, pcmMarks, airRank, pythonTest, noBacklog):
        super().__init__(pcmMarks=pcmMarks, airRank=airRank, pythonTest=pythonTest)

        self.noBacklog = noBacklog

    def result(self):
        if self.cutOff() and self.courseEligibilty() and self.noBacklog:
            return "YOU ARE PERFECT"
        else:
            return "You are not perect"


finalHybrid = Placment(70, 10000, 60, False)

print(finalHybrid.result())
