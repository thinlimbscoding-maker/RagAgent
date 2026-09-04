class Dog:
    food = "meat"

    def __init__(self, age):
        self.dogage = age

    def ageFInd(self):
        return self.dogage

    def changeFoodType(cls, newfood):
        cls.food = "maza"

    @classmethod
    def change_species(cls, newFod):
        cls.food = newFod  # Changes the variable for the WHOLE class


dogObj1 = Dog("12")
dogObj2 = Dog("22")
print(
    "trying to change class propety with without class method",
    dogObj1.changeFoodType("veg2"),
)

print(dogObj1.ageFInd(), "what is food type", dogObj1.food)
print(dogObj2.ageFInd(), "what is food type", dogObj1.food)

dogObj1.change_species("veg")
print(dogObj2.ageFInd(), "what is food type", dogObj1.food)
print(dogObj2.ageFInd(), "what is food type", dogObj2.food)
