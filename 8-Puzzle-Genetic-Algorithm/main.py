#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
8-Puzzle Solver Using Genetic Algorithm
Name: Krishna Kant Verma (2211cs19)
copyright@krishna6431
'''


# In[1]:


#all required imports 
import copy
import random
import time


# In[2]:


#if want to take input from file
# with open('input.txt', 'r') as input_file:

#     data_item = [[int(num) for num in line.split()] for line in input_file if line.strip() != ""]
    

# Extracting the Input and Goal States from the input file.

# initial = data_item[0:3].copy()
# final = data_item[3:6].copy()


# In[3]:


#fitness function to calculate fitness value
def fitnessValue(currState,selectedMethod):
    #no of placed tiles
    if selectedMethod == 1:
        #placed tiles
        fitness = 0
        for i in range(0,9):
            if(currState[i]==0):
                if i==8:
                    fitness+=1
                else:
                    continue
            if(currState[i]==(i-1)):
                fitness += 1
        return fitness
    #summation of multiply of tilesValue and respective Index
    elif selectedMethod == 2:
        fitness = 0
        for i in range(0,9):
            if(currState[i]==0):
                continue
            fitness += currState[i]*(i-1)
        return fitness


# In[4]:


#selecting two indexes for the selection of parents from the population
def rouletteWheelSelection(population,rouletteWheel):
    selectionRange = list(range(0,10))
    parent1 = random.choice(selectionRange)
    selectionRange.remove(parent1)
    parent2 = random.choice(selectionRange)
    selectionRange.remove(parent2)
    return parent1,parent2


# In[5]:


#crossOver Function of two Parents for creating offsprings
def crossOverFunction(parent1,parent2):
    #choosing some random number
    randomIndex = random.randint(0,8)
    offspring1=[]
    offspring2=[]
    #offspring1
    offspring1Parent1Chromosome = parent1[0:randomIndex]
    offspring1Parent2Chromosome = []
    
    #Cross for First offspring
    for i in range(0,9):
        if parent2[i] not in offspring1Parent1Chromosome:
            offspring1Parent2Chromosome.append(parent2[i])
            
    offspring1.append(offspring1Parent1Chromosome)
    offspring1.append(offspring1Parent2Chromosome)
    
    #offspring2
    offspring2Parent1Chromosome = parent1[randomIndex:]
    offspring2Parent2Chromosome = []
    
    #cross for 2nd Offspring
    for i in range(0,9):
        if parent1[i] not in offspring2Parent1Chromosome:
            offspring2Parent2Chromosome.append(parent1[i])
            
    offspring2.append(offspring2Parent1Chromosome)
    offspring2.append(offspring2Parent2Chromosome)
    
    offspring1 = [item for sublist in offspring1 for item in sublist]
    offspring2 = [item for sublist in offspring2 for item in sublist]
    return offspring1,offspring2


# In[6]:


#function of mutation for offspring probabilisticallly
def mutationFunction(offspring1,offspring2):
    mutationRange = [1,2,3,4,5,6,7,8,0]
    mutate1 = random.choice(mutationRange)
    mutationRange.remove(mutate1)
    mutate2 = random.choice(mutationRange)
    mutationRange.remove(mutate2)
    offspring1[mutate1],offspring1[mutate2] = offspring1[mutate2],offspring1[mutate1]
    offspring2[mutate1],offspring2[mutate2] = offspring2[mutate2],offspring2[mutate1]
    return offspring1,offspring2


# In[7]:


# population function for generating initial population
def generateInitialPopulation(initial):
    population = []
    population.append(initial)
    for i in range (0,8):
        population.append(initial)
        population[i][i],population[i][i+1] = population[i][i+1],population[i][i]
    population.append(initial)
    population[8][8],population[8][0] = population[8][0],population[8][8]
    return population


# In[8]:


#main algorithm 
def geneticAlgorithmSearch(initial,final,selectedMethod):
    startTime = time.time()
    print("Initial State:",initial)
    found = False
    bestChromosome = initial
    steps = 0
    fitnessList = []
    population = []
    count = 0
    tle = 60
    gen = 0
    #if initial not equal to final proceed further
    if initial != final:
        gen = 0;
        found = False
        #genrating population
        population = generateInitialPopulation(initial)
        #generating fitnessvalue
        for i in range(0,10):
            fitnessList.append(fitnessValue(population[i],selectedMethod))
        
        #iterate untill TLE or Solution Found
        while found != True and (time.time()-startTime) < tle:
            
            #Finding best chromosome till now
            currBest = []
            currentBestFitness = -1
            flag = False
            for i in range(0,10):
                if(population[i]==final):
                    currBest = final
                    flag = True
                    break
                elif currentBestFitness < fitnessList[i]:
                    currBest = population[i]
                    currentBestFitness = fitnessList[i]
            bestChromosome = currBest
            found = flag
            steps = i
            
            #generating roulette wheel array
            rouletteWheel = []
            for i in range(0,10):
                j=0
                while j <= fitnessList[i]:
                    rouletteWheel.append(i)
                    j = j + 1
                    
            #new generation population
            newgenPopulation = []
            repeat = 0
            
            #selecting parent each time and crossover is happening 
            while repeat < 5:
                parent1,parent2 = rouletteWheelSelection(population,rouletteWheel)
                randomProb = random.random()
                #if randomProb is following the criteria then offsping will generate
                if(randomProb > 0.71):
                    offspring1,offspring2 = crossOverFunction(population[rouletteWheel[parent1]],population[rouletteWheel[parent2]])
                    randomProb = random.random()
                    #mutate only when randomProb follow probablistic criteria
                    if randomProb < 0.225:
                        offspring1,offspring2 = mutationFunction(offspring1,offspring2)
                    newgenPopulation.append(offspring1)
                    newgenPopulation.append(offspring2)
                    repeat = repeat + 1
            #upgrading generation
            gen = gen + 1
            population = []
            population = newgenPopulation
            
            #creating new fitness for new generation
            fitnessList = []
            for i in range(0,10):
                fitnessList.append(fitnessValue(population[i],selectedMethod))
    #total time taken 
    totalTime = time.time() - startTime
    #if goal found
    if found:
        print("Hurray!The Puzzle has been Solved Successfully")
    else:
        print("Ooops! Puzzle didn't Solved")
    
    print("Start State :")
    print(initial)

    print("Goal State :")
    print(final)

    print("BestChromosome:")
    print(bestChromosome)
    
    print("Total number of states explored : ",end="")    
    if(initial==final):
        print("0")
    else:
        print((gen+1)*10)

    print("Time taken for execution : ",end="")
    print(round(totalTime,4),"sec")


# In[11]:


if __name__ == '__main__':
    print("8-Puzzle Solver Using Genetic Algorithm\n")
#     initial = [3,2,1,4,5,6,8,7,0]
#     initial = [4,1,3,0,2,5,7,8,6]
    # initial = [3,2,1,4,5,6,8,7,0]
#     initial = [1,2,3,4,5,6,7,8,0]
#     initial = [5,0,8,4,2,1,7,3,6]
    initial = [5,1,7,4,8,6,3,2,0]


    final   = [1,2,3,4,5,6,7,8,0]
    print("Initial:",initial)
    print("Final:",final)
    print("1.Fitness Function 1(Place Tiles):")
    print("2.Fitness Function 2(Sum of Product of Tile*Index):")
    print("\nSelect one of the above fitness function to Solve the Puzzle")
    selectedMethod = int(input())
    print("Solving Using Genetic Algorithm.")
    geneticAlgorithmSearch(initial,final,selectedMethod)
#thank you so much
