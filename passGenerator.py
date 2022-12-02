import random
import secrets
import string
import uuid
import sys

lettersLow = string.ascii_lowercase
lettersBoth = string.ascii_letters
specialChars = string.punctuation
numbers = string.digits
passLength = 0
password = ""
def generator() :
    
    print("Pleace choose your password attributes:")
    passLength = input("Password length: \n").strip()
    if int(passLength) <= 0:
        print("Invalid input")
        generator()
    else:
        print(f'Password length set to {passLength}')

    parameters = []
    parameters = input("Select password features, separate with space: \n \n" 
        + "Upper case letters    1 \n"
        + "Numbers               2 \n"
        + "Special characters    3 \n"
        + "All of the above      4 \n"
        + "None                  0 \n"
        + "Exit program          99 \n")

    parameters = parameters.split(' ')
    parameters = list(map(int, parameters))
    for attribute in parameters:
        if attribute < 0:
            print("Invalid input")
            generator()
        if attribute !=99 and attribute >4 and attribute <0:
            print("Invalid parameters selected!!!")
            generator()
        elif attribute != 99:
            print(f'Your choice = {attribute}')
    
    if len(parameters) == 1:
        for attribute in parameters:
            if int(attribute) == 0:
                password = ''.join(random.choice(lettersLow) for i in range(passLength))
            elif int(attribute) == 1:
                password = ''.join(secrets.choice(lettersBoth) for i in range(passLength))
            elif int(attribute) == 2:
                password = ''.join(secrets.choice(numbers + lettersLow) for i in range(passLength))
            elif int(attribute) == 3:
                password = ''.join(secrets.choice(specialChars+lettersLow) for i in range(passLength))
            elif int(attribute) == 4:
                password = ''.join(secrets.choice(numbers + lettersBoth + specialChars) for i in range(passLength))
            elif int(attribute) == 99:
                sys.exit()
    else:
        if 1 not in parameters and 2 not in parameters and 3 not in parameters:
            print("Out of bounds")
            generator()
        attributes = []
        for attribute in parameters:
            attributes.append(attribute)
        if 1 in attributes and 2 in attributes:
            password = ''.join(secrets.choice(numbers + lettersBoth) for i in range(passLength))
        elif 1 in attributes and 3 in attributes:
            password = ''.join(secrets.choice(lettersBoth + specialChars) for i in range(passLength))
        elif 2 in attributes and 3 in attributes:
            password = ''.join(secrets.choice(lettersLow + numbers + specialChars) for i in range(passLength))
    if password != "":
        print(f'Your password is {password}')

    generator()

generator()