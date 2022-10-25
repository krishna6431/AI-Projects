# copyright@krishna6431
#all required libraries that are needed
# deepcopy
import copy
# time module
import time
#math module
import math
import random

# taking input from file
with open('input.txt', 'r') as input_file:
    data_item = [[int(num) for num in line.split()] for line in input_file if line.strip() != ""]

# Extracting the Input and Goal States from the input file.
initial = data_item[0:3].copy()
# final = data_item[3:6].copy()

# initial = [[3,2,1],[4,5,6],[8,7,0]]
final = [[1,2,3],[4,5,6],[7,8,0]]
# store total steps taken by hill climbing algorithm

# checking whether the movement is possible or not on grid
def isValid(x,y):
    return x >= 0 and x <= 2 and y >= 0 and y <= 2

#Search with displaced tile count i.e. objective fn = no of displaced tiles 
def energyNumDisplacedTiles(currState):
    energyVal = 0
    for i in range(0,3):
        for j in range(0,3):
            if currState[i][j]!=final[i][j]:
                energyVal=energyVal+1        
    return energyVal

#Search with mannhaten distance i.e. objectiive fn= manhattenDistance
def energySumOfManhatten(currState,finalState):
    #position of the tiles of final puzzle
    posTiles = {1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],0:[2,2]}
    energyVal = 0
    for i in range(0,3):
        for j in range(0,3):
            #calculating manhatten distance
            manhatten_Distance = abs(i-posTiles[currState[i][j]][0]) + abs(j-posTiles[currState[i][j]][1])     
            energyVal = energyVal +  manhatten_Distance      
    return energyVal

#function that calculates the heuristic value of the puzzle 
def energyValue(currState,selectedMethod):
    if selectedMethod == 1:
        return energyNumDisplacedTiles(currState)
    elif selectedMethod == 2:
        return energySumOfManhatten(currState,final)
    
#Function that finds the position of 0 in the puzzle
def findBlankPosition(currPuzzleState):
    for i in range(0,3):
        for j in range(0,3):
            if(currPuzzleState[i][j]==0):
                return i,j

# function to generate the neighbours states of the current state
def generateNeighbours(currPuzzleState):
    neighbours = []
    moves =[]
    #up down right left
    moveDirection = [[0,1],[0,-1],[1,0],[-1,0]]
    x,y = findBlankPosition(currPuzzleState)
    #iterating on all four directions if possible
    for i in range(0,4):
        newX = x + moveDirection[i][0]
        newY = y + moveDirection[i][1]
        if not isValid(newX,newY):
            continue
        if i == 0:
            moves.append("Right")
        elif i == 1:
            moves.append("Left")
        elif i == 2:
            moves.append("Down")
        elif i == 3:
            moves.append("Up")
        tempState = copy.deepcopy(currPuzzleState)
        tempState[newX][newY],tempState[x][y] = tempState[x][y],tempState[newX][newY]
        neighbours.append(tempState)
    return neighbours,moves

#function that solves the Puzzle using Simmulated Annealing
def simmulatedAnneling(initial,final,maxMoves,prob,selectedMethod):
    print("Starting from:")
    print(initial)
    currState = initial
    lastState = initial
    print("Initial State=",currState)
    temperature = maxMoves
    #energy value of initial puzzle
    oldEnergy = energyValue(currState,selectedMethod)
    resultMoves=[]
    step=0
    #untill problem solved or temperature == 0 repeat
    while not currState==final and temperature > 0:
        #finding neighbours and corresponding moves
        neighbours,moves = generateNeighbours(currState)
        #state of acceptnace 
        accepted = False
        #untill not accepting the next state repeat
        while not accepted:
            #iterating over all possible neighbour
            for i in range(0,len(neighbours)):
                neighbour=neighbours[i]
                if neighbour!=lastState:
                    #calculating energy of neighbour state
                    newEnergy = energyValue(neighbour,selectedMethod)
                    deltaEnergy = newEnergy - oldEnergy
                    #if it less than zero then select that state
                    if deltaEnergy <= 0:
                        lastState=currState
                        step = step + 1
                        currState = neighbour
                        resultMoves.append(moves[i])
                        print("nextState=",currState)
                        accepted = True
                        break
                    #otherwise select probablistily random state
                    else:
                        boltz = math.exp(-float(prob*deltaEnergy)/temperature)
                        print("boltz: "+str(boltz))
                        r = random.random()
                        #if boltzman probability is greagter equal to random probability generated
                        if r <= boltz:
                            lastState=currState
                            currState = neighbour
                            resultMoves.append(moves[i])
                            step = step + 1
                            accepted = True
                            print("nextState=",currState)
                            break
                    #if still not accepted
                    if not accepted:
                        currState = initial      
        oldEnergy = newEnergy
        temperature = temperature-1
    #solved Successfully
    if temperature != 0:
        print("Hurray! Problem Solved Successfully")
        print("Steps to Solve:",resultMoves)
    #failure case
    else:
        print("Oops! Unable to Solve This Puzzle.")
    return step

#main functions starts from here
if __name__=='__main__':
    print("Welcome to 8-Puzzle Solver (Simulated Annealing Version)\n")
    print("Initial State of the Puzzle.")
    print(initial)
    step=0
    final=[]
    l=[]
    for i in range (1,10):
        if i!=9:
            l.append(i)
        else:
            l.append(0)
        if i%3==0:
            final.append(l)
            l=[]
            
    print("\nFinal state of Puzzle:")
    print(final)
    print("\nSelect the Method from below options.")
    print("1.Objective Function :No of Displaced Tiles.")
    print("2.Objective Function:Sum of Mahnatten Distance.")
    selectedMethod = int(input())
    print("Solving the Puzzle.....")
    sTime = time.time()
    step = simmulatedAnneling(initial,final,10,0.25,selectedMethod)
    eTime = time.time()
    print("Number of States Explored:",step)
    print("Total Time Taken:",round(eTime-sTime,3),"sec")
    print("Thank You For Using this service")
    #thank you so much
