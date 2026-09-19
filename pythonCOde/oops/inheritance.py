class Nameclass:
    prop1 = "kunal"
    private = "test2"

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def fullname(self):
        return self.name + self.lastname


class ScroreClass(Nameclass):

    def __init__(self, name, lastname, marks, outof):
        super().__init__(name, lastname)
        self.marks = marks
        self.outof = outof

    def tolpercentage(self):
        return self.marks * 100 / self.outof


resultObj = ScroreClass("kunal", "patley", 300, 500)
print("name is", resultObj.name)
print("result is ", resultObj.tolpercentage(), "%")
print("fullname", resultObj.fullname())
