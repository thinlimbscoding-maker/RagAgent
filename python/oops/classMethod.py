# class method where we want to keep same property tiugh out all class
class My:
    mySkill = "coder"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def show_skill(cls):

        print(f"my class is {cls.mySkill}")

    def my_intro(self):
        print(f"my name is {self.name} and age is {self.age} ")


myObj = My("kunal", 26)
print("showing direct skill", myObj.mySkill)
print("showing class method", myObj.show_skill())

print("showing my_intro", myObj.my_intro())
