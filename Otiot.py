import sys
import csv
import itertools
import random

#Game is Otiot Sequencer

alphabet = 'CTGA'    #define the alphabet
storedHints=[]
answerKey=[]
table = []
row=1   #saves the row in the table to write to

def inputAnswer(answerLength):
    #creates an answer for the puzzle and saves it in global variable
    global answer
    #answer=str(input('enter answer '))
    #answerLength=int(input('enter answer length '))
    answer=''
    while len(answer)<answerLength:
        answer+=random.choice(alphabet)
    print(answer)

def createAnswerKey():
    #creates an answerkey of all possible combinations of item alphabet
    #Has a loop that calls inputHint() when answerKey is not = 1
    global answerKey
    global answer
    global alphabet
    global storedHints

    storedHints = []

    count = len(answer)
    for item in itertools.product(alphabet, repeat=count):
        answerKey.append("".join(item))

#    for x in alphabet:
#        for y in alphabet:
#            for z in alphabet:
#                answerKey.append(str(x)+str(y)+str(z))
    while len(answerKey) != 1:
        #print("There are " + str(len(answerKey)) + " remaining possible answers: ")
        #print(str(answerKey))
        inputHint()
        #THIS IS THE MAIN BANANA. The game runs through this command.
    print('Only the correct solution, ' + str(answerKey) + ' remains. Here are the hints: ' + str(storedHints))


def inputHint():
    #asks for user input on the hint
    hint=''
    while len(hint) != len(answer) or hint==answer:
        #only accepts hints that are not the answer and have the same # digits as the answer
        if hint == answer:
            print('The hint cannot be the answer.')
        else:
            print('The hint must have ' + str(len(answer)) + ' letters')
        #hint = str(input('enter hint '))
        hint = ''
        while len(hint) < len(answer):          #this while loop creates the hint automatically and randomly
            hint += random.choice(alphabet)
    hintCorrectness=howCorrectisHint(hint)
    removeIncorrectFromAnswerKey(hintCorrectness,hint)



def howCorrectisHint(hint):
    #returns what % the hint matches the answer
    correctness = 0.0
    x=0
    while x < len(answer):
        if answer[x]==hint[x]:
            correctness = correctness + 1/len(answer)
        x+=1
    #print('this hint is ' + str(correctness*100) + '% correct')
    return correctness

def removeIncorrectFromAnswerKey(correctness,hint):
    #takes the answerKey and removes any potential answers that do not line up with hint
    global answerKey
    global storedHints
    newcorrectness=0.0
    itemstoremove=[]
    for possibleSolution in answerKey:      #loops through possiblesolutions array and saves any items to remove because correctness
                                            #does not match to itemstoremove array
        y=0
        while y < len(answer):
            if hint[y]==possibleSolution[y]:
                newcorrectness = newcorrectness + 1/len(answer)
            y+=1
        if newcorrectness != correctness:
            itemstoremove.append(possibleSolution)
        newcorrectness=0.0
    if len(itemstoremove)==0:
        print('This hint did not remove any possible solutions.')
        print('These are the remaining solutions' + str(answerKey))
    elif len(itemstoremove)==len(answerKey):
            print('This hint has removed all possible solutions. Enter a new hint')
            print('These are the remaining solutions' + str(answerKey))
    else:
        for notSolution in itemstoremove:
            answerKey.remove(notSolution)
        storedHints.append(hint)                            #saves stored hints in array

def createGameBoardTable():

    global answer
    global storedHints
    global table
    global row

    table.append(['Answer'])

    x=0
    while x < len(answer):
        table.append([answer[x]])
        x+=1



    tableHintCorrectness=table[len(table)-len(answer)-1]
    for x in storedHints:
        tableHintCorrectness.append(howCorrectisHint(x))

    for x in storedHints:
        print("This is the stored hint")
        print(x)
        print("table before adding stored hint")
        print(table)
        print("this is row value" + str(row))
        y=0
        while y<len(x):
            table[row+y].append(x[y])
            y+=1
            print("table after adding stored hint")
            print(table)
    row=row+y

    y=0
    blankrow=[]
    while y<=len(storedHints):
        blankrow.append(' ')
        y+=1
    table.append(blankrow)
    print(table)
    row+=2

#    blankrow=['']
#    for x in table:
#        print('added x')
#        blankrow.append('')
#        print(blankrow)
#    print(blankrow)
#    table.append(blankrow)




def writeGameBoard(table):
    with open('gameboards.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerow(r) for r in table]
    print('Gameboard has been created')





def multiGame():
    #generates multiple puzzles
    puzzlecount=int(input("How many puzzles should be generated? "))
    answerLength=int(input('enter answer length '))

    while puzzlecount>0:

        inputAnswer(answerLength)
        createAnswerKey()
        createGameBoardTable()
        storedHints = []
        answerKey = []
        puzzlecount-=1

    writeGameBoard(table)
    sys.exit()

multiGame()
