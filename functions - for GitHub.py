import speech_recognition as sr
import pyttsx3
import os
import time
import pyttsx3
import re
import webbrowser

#Analyzing the background noise and setting up some settings
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    #r.adjust_for_ambient_noise(source, duration = 1)
    r.energy_threshold = 2500
r.pause_threshold = 0.5
r.dynamic_energy_threshold = True #This makes the recognizer class automatically adjust the energy threshold level over time, as to eventually reach a suitable value. May encounter errors in the beginning.

#The functions I have defined here are:
#say()-insert text as an argument to hear voice output and have it printed out
#get_info()-Introduces the user to the chatbot and gets his houndify log in details
#listen()-have the chatbot listen to what you are saying
#analyze()-takes the user's command as an argument and analyzes it
#google()-for searching things up on google, takes the query as an argument

#THE say() FUNCTION:
#Setting up the voice
engine = pyttsx3.init()
engine.setProperty('rate', 175)
def say(text):
    print("Michael: " + text)
    engine.say(text)
    engine.runAndWait()

#THE THE get_info() FUNCTION:
#The function input_info() will introduce the user to the chatbot and get his login details from houndify
#So that the user can use the chatbot
def input_info():
    say("Hello, my name is Michael. I am your personal digital assistant.")
    say("In order for me to hear what you say, you must sign up to houndify and provide in your log in details.")
    say("Houndify is a speech to text service.")
    say("Your login details will not be shared with anyone.")
    say("Go to this website and sign up")
    print("https://www.houndify.com/")
    time.sleep(1)
    say("Now input your Client ID from the Houndify speech to text service")
    id=input(">")
    with open("id.txt", "w") as id_file:
        id_file.write(id)
    say("Now input your Client Key from the Houndify speech to text service")
    key=input(">")
    with open("key.txt", "w") as key_file:
        key_file.write(key)
    say("Thanks for logging in")

#THE listen() FUNCTION:
#First, we have to retrieve the key and log in
try:
    id_file=open("id.txt")
    key_file=open("key.txt")
    id=id_file.read()
    key=key_file.read()
except IOError:
    input_info()
def listen():
    with mic as source:
        audio = r.listen(source, phrase_time_limit=5) #If the chatbot cuts you off too early, just increase the number of seconds on the phrase_time_limit or delete the parameter.
        global id
        global key
        command =r.recognize_houndify(audio, id, key)
        return command #This is what the chatbot has heard from the user

#THE FUNCTION analyze() FOR PARSING USER INPUT:
def analyze(command):
    if re.search(("(subjects|schedule|sessions).*today"), command) is not None:
        return [1]
    elif re.search("(subject|schedule|session).*now", command) is not None:
        return [2]
    elif re.search("(subjects?|schedule|session).*next", command) is not None:
        return [3]
    elif (re.search("time", command) is not None) and ("date" not in command) and ("today" not in command):
        return [4]
    elif (re.search("(date|today)", command) is not None) and ("time" not in command):
        return [5]
    elif (re.search("(date|today)", command) is not None) and (re.search("time", command) is not None):
        return [6]
    elif re.search("(search|browse|look|the internet|google) (for|up)", command) is not None:
        match = re.search("(search|browse|look|the internet|google) (for|up)", command)
        query = command.partition(match.group(0))[-1]
        return [7, query]
    elif re.search("define", command) is not None:
        match = re.search("define", command)
        word = command.partition(match.group(0))[-1]
        return [8, word]
    else:
        return [0] # A value of 0 at the first index should mean that no function is available ( He can't do that )

#THIS FUNCTION google() IS FOR SEARCHING UP STUFF ON THE WEB
def google(query):
    url="https://www.google.com/?#q="
    webbrowser.open(url+query,2)
    say("Searching Google for "+query)