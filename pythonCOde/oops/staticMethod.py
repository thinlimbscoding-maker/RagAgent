class My:

    ctc = "10pa"

    def __init__(self, name, age, name2):
        self.name = name
        self.age = age
        self.name2 = name2

    @staticmethod
    def mySalary(exp):
        if exp > 10:
            return 20
        else:
            return 10

    @classmethod
    def accessCtc(cls):
        return cls.ctc

    def myIntro(self):
        return f"my  name is {self.name}  and my age is {self.age} {self.name2}"


obj1 = My("kunal", 26, "name2")
print(obj1.myIntro())
print("on base my exp u bonus ", obj1.mySalary(9))
