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
    passLength = int(input("Password length: \n"))

    if passLength == 0:
        print("Invalid input")
        generator()
    else:
        print(f'Password length set to {passLength}')

    parameters = []
    parameters = input("Select password features, separate with comma: \n \n" 
        + "Upper case letters    1 \n"
        + "Numbers               2 \n"
        + "Special characters    3 \n"
        + "All of the above      4 \n"
        + "None                  0 \n"
        + "Exit program          99 \n")

    if int(parameters) !=99 and int(parameters) >4:
        print("Invalid parameters selected!!!")
        generator()
    elif int(parameters) != 99:
        print(f'Your choice = {parameters}')

    
    parameters = parameters.split(',')
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
    elif len(parameters) > 1:
        for attribute in parameters:
            print("more than one choice")
    if password != "":
        print(f'Your password is {password}')

    generator()

generator()