import os
def createFile():
 with open("notes.txt", "w") as file:
    file.write("hellow first line\n")
    file.write("i am 2nd line2")

    if os.path.exists("notes.txt"):
      return "added"
    else:
      return "not added"
    
# if not(os.path.exists('notes.txt')):
print("result of create file",createFile())


def appendFile():
  with open("notes.txt",'a') as file:
    file.write("\n i am 32rd line")
    if os.path.exists('notes.txt'):
      return 'data append'
    else:
      return 'data not append'

print("Result of append file",appendFile())    