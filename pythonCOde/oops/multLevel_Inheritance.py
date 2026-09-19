class School:
    def __init__(self, class10, class12):
        self.class10 = class10
        self.class12 = class12

    def totalSchool(self):

        return self.class10 + self.class12


class College(School):

    def __init__(self, class10, class12, airRank):
        super().__init__(class10, class12)
        self.airRank = airRank

    def steam(self):
        if self.airRank > 1000:
            return "dentist"
        else:
            return "Mbbs"


class Job(College):

    def __init__(self, class10, class12, airRank, houseLoan):

        super().__init__(class10, class12, airRank)
        self.houseLoan = houseLoan

    def package(self):
        if self.steam() == "Mbbs":
            return 20
        else:
            return 10

    def LoanStatus(self):
        print("sss", self.houseLoan)
        if self.houseLoan > 5000000:
            if self.package() > 15:
                return "congrat"
            else:
                return "sorry"
        else:
            return "pass"

    def loanUpdate(self):
        return self.LoanStatus()


marriage = Job(300, 400, 600, 7000000)

print(marriage.loanUpdate())


# simple rule all prametrr u need to pass from child to top Parent class
