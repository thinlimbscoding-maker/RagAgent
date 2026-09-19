class Dog:
    food = "meat"

    def __init__(self, age):
        self.dogage = age

    def ageFInd(self):
        return self.dogage

    def changeFoodType(cls, newfood):
        cls.food = newfood
        return cls.food

    @classmethod
    def change_species(cls, newFod):
        cls.food = newFod  # Changes the variable for the WHOLE class


dogObj1 = Dog("12")
dogObj2 = Dog("22")

Dog.change_species("burder")


print(Dog.food)
print(dogObj1.food)
print(dogObj2.food)
print(dogObj1.changeFoodType(8))
print(dogObj1.food)
print(Dog.food)  # 🟢 Output is STILL: burder
