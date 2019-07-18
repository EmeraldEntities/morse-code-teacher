from random import randint, shuffle
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

#-----------------#
WIDTH = 75
HEIGHT = 75
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
#-----------------#
BLACK = (255, 255, 255)

#########################
# FUNCTIONS
#########################
def loadSound(sound): #- Loads a sound file
    newSound = pygame.mixer.Sound(sound)
    newSound.set_volume(0.5)
    return newSound

def loadFromFile(file): #- Loads a .txt and saves as a list
    with open(file) as f:
        allObjectsRaw = f.readlines()
        allObjects = []
        for i in allObjectsRaw:
            allObjects.append(i.rstrip())
    return allObjects

def playTone(icon): #- Plays the morse tone
    if icon == ".":
        dot.play()
        pygame.time.wait(450)
    elif icon == "-":
        dash.play()
        pygame.time.wait(700)
    elif icon == "0": #- only used in event of a space
        pygame.time.wait(1750)

#------------------------#
#- Load in everything important
allMorse = loadFromFile("morse.txt")
allWords = loadFromFile("words.txt")
allSentences = loadFromFile("sentences.txt")
allLetters = loadFromFile("alphabet.txt")
allLetters.append(" ")

dot = loadSound("dot.wav")
dash = loadSound("dash.wav")
#---------------------------------

inPlay = True
mode = "tutorial"

#########################
# LOOP
#########################
while inPlay:
    gameWindow.fill(BLACK)

    if mode == "tutorial": #- The learning section
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Type any letter OR word and you will hear the tone for it. Put a * and then a number for it to be repeated."
        print "Type allLetters to hear all letters."
        print "Type 'Test me' to enter WORD phase"
        print "Type '*RUN AWAY*' to run away"
        choice = raw_input("\nWhat is your input? ").rstrip()
        if choice == "Test me":
            mode = "selectWord"
        elif choice == "*RUN AWAY*":
            inPlay = False
            mode = "exitting"
        elif choice == "allLetters":
            toTranslate = allLetters
        else:
            choice = choice.lower()
            breakString = -1
            breakString = choice.find("*")

            if breakString == -1:
                toTranslate = list(choice)
                timesToLoop = 1     
            else:
                timesToLoop = int(choice[breakString+1:])
                toTranslate = choice[:breakString]
                    
        if mode == "tutorial":
            morseToTranslate = []
            actualLetters = []
            originalMorse = []
            
            for i in toTranslate: #- Takes the input and converts them to morse
                morseToTranslate.append(allMorse[allLetters.index(i)].split()) 
                originalMorse.append(allMorse[allLetters.index(i)])
                actualLetters.append(i)
            
            for i in range(timesToLoop): #- In case we want it to repeat
                print "\nPlaying! Play Number " + str(i + 1) + "\n"
                for n in range(len(morseToTranslate)):
                    for m in morseToTranslate[n]:
                        playTone(m)
                    if actualLetters[n] != " ":
                        print "Letter: " + actualLetters[n]
                        print "Morse: " + originalMorse[n]
                    else:
                        print "\n"
                    pygame.time.wait(700)
                pygame.time.wait(1500)

    elif mode == "guessWord":
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "Playing test word:" 
        morseAssociated = []
        for i in letters: #- Converts the new word we assigned into a morse code
            morseAssociated.append(allMorse[allLetters.index(i)].split())
        
        for i in morseAssociated: #- Plays it
            for e in i:
                playTone(e)
                
            pygame.time.wait(700)
        confirmation = True

        # - Provides and prints choices
        randomChoice = shuffle(choices)
        print "\n\nHere are your possible choices:"
        print choices

        while confirmation: #- Makes sure that the input is valid
            result = raw_input("\nWhat's the word? Type r to replay. Type 'i don't like' to run away. ").rstrip()
            if result == newWord:
                print "\nCorrect!"
                mode = "selectWord"
                confirmation = False
            elif result == "i don't like":
                print "\nTutorial Time!"
                mode = "tutorial"
                confirmation = False
            elif result == "r":
                print "\nReplaying:"
                confirmation = False
            else:
                print "\nWrong guess! Try again!"

    elif mode == "selectWord": #- Chooses a random word
        usedWord = True
        choices = []
        while usedWord:
            newWord = allWords[randint(0, len(allWords)-1)]
            usedWord = False

        letters = list(newWord)
        notGuessed = True
        choices.append(newWord)

        while len(choices) < 9: #- Generates a list of choices
            randomWord = allWords[randint(0, len(allWords)-1)]
            if randomWord not in choices and randomWord != newWord:
                choices.append(randomWord)
        mode = "guessWord"

    pygame.display.update()
pygame.quit()
