#all required libraries that are needed
# deepcopy
import copy
# time module
import time
#math module
import math

# taking input from file
with open('input.txt', 'r') as input_file:
    data_item = [[int(num) for num in line.split()] for line in input_file if line.strip() != ""]
    

#Extracting the Input and Goal States from the input file.
initial = data_item[0:3].copy()
final = data_item[3:6].copy()

# store total steps taken by hill climbing algorithm
step = 0

# checking whether the movement is possible or not on grid
def isValid(x,y):
    return x >= 0 and x <= 2 and y >= 0 and y <= 2

#Search with displaced tile count i.e. h(n)= no of displaced tiles 
def numDisplacedTiles(currState):
    heuristicVal = 0
    for i in range(0,3):
        for j in range(0,3):
            if currState[i][j]!=final[i][j]:
                heuristicVal=heuristicVal+1        
    return heuristicVal

#Search with mannhaten distance i.e. h(n)= manhattenDistance
def sumOfManhatten(currState,finalState):
    #position of the tiles of final puzzle
    posTiles = {1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],0:[2,2]}
    heuristicVal = 0
    for i in range(0,3):
        for j in range(0,3):
            #calculating manhatten distance
            manhatten_Distance = abs(i-posTiles[currState[i][j]][0]) + abs(j-posTiles[currState[i][j]][1])     
            heuristicVal = heuristicVal +  manhatten_Distance      
    return heuristicVal

#function that calculates the heuristic value of the puzzle 
def heuristicValue(currState,selectedMethod):
    if selectedMethod == 1:
        return numDisplacedTiles(currState)
    elif selectedMethod == 2:
        return sumOfManhatten(currState,final)
    
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

#function that solves the Puzzle using hill climbing
def hillClimbing(initial,final,step):
    #assuming the current state have best heuristic
    best = heuristicValue(initial,selectedMethod)
    
    #if goal reached
    if best == 0:
        print("👏Hurray!Puzzle Solved.")
        return step
    
    #storing all the neighbours of current state
    neighbours,moves = generateNeighbours(initial)
    nextState = copy.deepcopy(initial)
    #iterating on all the neighbours of current state
    idx = 0
    currMove = ""
    for currState in neighbours :
        #calculating the heuristic value
        h_value = heuristicValue(currState,selectedMethod)
        #updating the h_value and next state with best possible state (if possible)
        if h_value < best :
            best = h_value
            nextState = copy.deepcopy(currState)
            currMove = moves[idx]
            idx = idx + 1
    if(currMove != ""):
        print(currMove)
    previous_h_val = heuristicValue(initial,final)
    #if next state is same
    if nextState == initial:
        #check if any neighbours state have h_val equal to currState
        idx = 0
        currMove = ""
        for currState in neighbours :
            h_value = heuristicValue(currState,selectedMethod)
            #shoulder point
            if h_value == best :
                best = h_value
                nextState = copy.deepcopy(currState)
                currMove = moves[idx]
                idx = idx + 1
                break
        if(currMove != ""):
            print(currMove)
        #if still nextState is not updated return failure
        if nextState == initial:
            print("Ooops! Program Stucked.\nBetter Luck Next Time 👍")
            return step
        
        #if there is some next state(shoulder point)
        else:
            count = 100
            while(count):
                flag = False
                #storing all the neighbours of current state
                neighbours,moves= generateNeighbours(initial)
                nextState = copy.deepcopy(initial)
                
                #iterating on all the neighbours of current state
                idx = 0
                currMove = ""
                for currState in neighbours :
                    #calculating the heuristic value
                    h_value = heuristicValue(currState,selectedMethod)
                    #updating the h_value and next state with best possible state (if possible)
                    if h_value < best :
                        best = h_value
                        nextState = copy.deepcopy(currState)
                        currMove = moves[idx]
                        idx = idx + 1
                        flag = True
                if(currMove != ""):
                    print(currMove)

                previous_h_val = heuristicValue(initial,selectedMethod)
                 #check if any neighbours state have h_val equal to currState
                if nextState == initial:
                    idx = 0
                    currMove = ""
                    for currState in neighbours :
                        h_value = heuristicValue(currState,selectedMethod)
                        if h_value == best :
                            best = h_value
                            nextState = copy.deepcopy(currState)
                            currMove = moves[idx]
                            idx = idx + 1
                            break
                    if(currMove != ""):
                        print(currMove)
                #if still nextState is not updated return failure    
                if nextState == initial:
                    print("Ooops! Program Stucked.\nBetter Luck Next Time 👍")
                    break
                
                initial = copy.deepcopy(nextState)
                if flag == True:
                    break
                #incrementing steps
                step = step + 1
                #decrementing count
                count = count - 1
            #if count == 0 return failure
            if count == 0:
                print("Ooops! Program Stucked.\nBetter Luck Next Time 👍")
                return step
    #incrementing steps
    step = step + 1
    #calling the hillClimbing on next State
    return hillClimbing(nextState,final,step)
    

#main functions starts from here
if __name__=='__main__':
    print("Welcome to 8-Puzzle Solver\n")
    print("Initial State of the Puzzle.")
    print(initial)
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
    print("1.h(n):No of Displaced Tiles.")
    print("2.h(n):Sum of Mahnatten Distance.")
    selectedMethod = int(input())
    print("Solving the Puzzle.....")
    print("Steps:")
    sTime = time.time()
    stepCount = hillClimbing(initial,final,0)
    eTime = time.time()
    print("Number of States Explored:",stepCount)
    print("Total Time Taken:",round(eTime-sTime,3),"sec")
    print("Thank You For Using this service")
    #thank you so much
