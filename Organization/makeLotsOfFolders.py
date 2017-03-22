import os
import glob
import pathlib



#create test folder structure with text files
path = r"C:\Users\peters\Desktop\pythonTest2\monkeys\big\green\awesome"
folder = pathlib.Path(path)
if not os.path.exists(path):
    os.makedirs(path)


filename = "testfile3.txt"
filepath = os.path.join(path, filename)
file = open(filepath, 'w')
file.writelines("yoyoyo what good homie\nI got chu")
file.close()

print(f"{filepath} created successfully!")
    
letters = "abcde"
letterList = list(word)

numbers = list(range(10))
print(numbers)


for letter in letters:
    for number in numbers:
        directory = os.path.join(path, letter, str(number))
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(directory)
        
        
        
        
        
