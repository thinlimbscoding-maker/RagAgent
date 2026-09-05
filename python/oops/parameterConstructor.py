class My:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def about(self):
        print(f"my nam is ${self.name} and my age is {self.age} ")
        return


myObj1 = My("kunal", 26)
print(myObj1.about())
