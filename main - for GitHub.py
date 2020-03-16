from functions import *
from alive_progress import alive_bar
import sys
from datetime import datetime
from PyDictionary import PyDictionary

dictionary=PyDictionary()
user = "Sir"
recognizing_speech_error = False

def print_info():
    print("This chatbot was developed by Saifeldin Mohamed Farid from 11XE in 2020")
    print("=============================================================================")
    print("My name is Michael.")
    print("I am your personal digital assistant.")
    print("=============================================================================\n")
print_info()
say("How may I help you ?")
while True:
    command = ""
    while not("michael" in command):
        try:
            with alive_bar(unknown="pointer", bar="solid", spinner="pulse") as bar:
                bar(text="Michael is waiting")
                command = listen()
                os.system('cls')
                print_info()
        except sr.RequestError:
            recognizing_speech_error = True
            break
    if recognizing_speech_error:
        print("\n")
        say("I am having a problem")
        say("Either there's no wifi connection or the Client ID and key are wrong")
        say("Did you input the correct Client ID and key ? Input the number of your answer ")
        print("1. Yes")
        print("2. No")
        problem_source = input(">")
        if "1" == problem_source:
            say("Then you must be having a weak wifi connection.")
            say("Come back later when the connection is good")
            time.sleep(10)
            exit()
        elif "2" == problem_source:
            input_info()
            id_file=open("id.txt")
            key_file=open("key.txt")
            id=id_file.read()
            key=key_file.read()
            say("The problem should have been solved now.")
            say("Try saying something\n")
            print_info()
            continue
        else:
            say("ERROR ! Please input a valid number\n")
            time.sleep(2)
            exit()

    with alive_bar(unknown="brackets",bar="solid", spinner="pulse") as bar:
        bar(text="Michael is listening")
        print("Sir: "+command)
        time.sleep(2)
        operation = analyze(command)

    #Operation 1 = What subjects do I have today ?
    #Operation 2 = What subject do I have now ?
    #Operation 3 = What subject do I have next ?
    #Operation 4 = What is the time ?
    #Operation 5 = What is the date ?
    #Operation 6 = What is the date time ?
    #Operation 7 = Search something on google
    #operation 8 = define a word

    #The subjects are put in a dictionary, you have to add them yourself
    #They don't necessarily have to be school subjects, they can be things you have on your schedule
    #"Subject name": (start hour, minutes, finish hour, minutes, room number)
    #If there's no room number, just leave an empty string to avoid an IndexError
    #The time has to be in military time
    #If you want to add your schedule for friday and saturday, add dictionaries for them and make them variables in the weekdays list after the dictionaries
    sunday = {}
    monday = {}
    tuesday = {}
    wednesday = {}
    thursday = {}
    weekdays = [monday, tuesday, wednesday, thursday, "friday", "saturday", sunday]

    #Make sure to remove the conditionals in the first 3 operations' conditionals if you want to include friday and saturday in your saved schedules
    if operation[0] == 1:
        if not(0<=datetime.now().weekday()<4) and datetime.now().weekday() != 6:
            engine.say(str(user)+", today is a weekend !")
            engine.runAndWait()
            print("Sir, today is a weekend !")
            continue
        if 0<=datetime.now().weekday()<4 or datetime.now().weekday()==6:
            say("You have: ")
            for subject in weekdays[datetime.now().weekday()].keys():
                say(subject)
    elif operation[0] == 2:
        if not(0<=datetime.now().weekday()<4) and datetime.now().weekday() != 6:
            engine.say(str(user)+", today is a weekend !")
            engine.runAndWait()
            print("Sir, today is a weekend !")
            continue
        for subject in weekdays[datetime.now().weekday()].values():
            if datetime(datetime.now().year, datetime.now().month, datetime.now().day, subject[0], subject[1]) <= datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, subject[2], subject[3]):
                index = list(weekdays[datetime.now().weekday()].values()).index(subject)
                say( "You have "+ str(list(weekdays[datetime.now().weekday()].keys())[index])+ " in room " + str(subject[4]) )
                break
    elif operation[0] == 3:
        if not(0<=datetime.now().weekday()<4) and datetime.now().weekday()!=6:
            engine.say(str(user)+", today is a weekend !")
            engine.runAndWait()
            print("Sir, today is a weekend !")
            continue
        for subject in weekdays[datetime.now().weekday()].values():
            if datetime(datetime.now().year, datetime.now().month, datetime.now().day, subject[0], subject[1]) <= datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, subject[2], subject[3]):
                index = list(weekdays[datetime.now().weekday()].values()).index(subject)+1
                try:
                    say( "You have "+ str(list(weekdays[datetime.now().weekday()].keys())[index])+ " in room " + str(list(weekdays[datetime.now().weekday()].values())[index][4]) )
                    break
                except IndexError:
                    say("You don't have any subjects next sir")
    elif operation[0] == 4:
        print("Michael: The time is "+ str(datetime.now().hour) + ":" + str(datetime.now().minute) + " and " + str(datetime.now().second) + " seconds")
        engine.say("The time is "+ str(datetime.now().hour) + " " + str(datetime.now().minute) + " and " + str(datetime.now().second) + " seconds")
        engine.runAndWait()
    elif operation[0] == 5:
        say("Today is "+ datetime.strftime(datetime.now(), '%A') +" "+ str(datetime.now().day) +" "+ datetime.strftime(datetime.now(), '%B') )
    elif operation[0] == 6:
        print("Michael: The time is "+ str(datetime.now().hour) + ":" + str(datetime.now().minute) + " and " + str(datetime.now().second) + " seconds")
        engine.say("The time is "+ str(datetime.now().hour) + " " + str(datetime.now().minute) + " and " + str(datetime.now().second) + " seconds")
        engine.runAndWait()
        say("Today is "+ datetime.strftime(datetime.now(), '%A') +" "+ str(datetime.now().day) +" "+ datetime.strftime(datetime.now(), '%B') )
    elif operation[0] == 7:
        google(operation[1])
    elif operation[0] == 8:
        definitions = dictionary.meaning(operation[1])
        for part_of_speech in definitions:
            say(part_of_speech)
            print("  as in:")
            engine.say(" as in ")
            engine.runAndWait()
            for meaning in definitions[part_of_speech]:
                say(meaning)
    else:
        say("I can't do that")
        continue