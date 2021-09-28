# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import urllib.request
import random
from pathlib import Path

class EliteCode:
    def fetchRandomProblems(numProblems, difficulties):
        # Chooses n random problem and fetches the prompts, skeleton and solutions from github
        problems = []
        indicies = []
        #fetch list of problems
        urlEasy = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Easy/problemList.txt"
        urlMedium = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Medium/problemList.txt"
        urlHard = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Hard/problemList.txt"
        print("Fetching latest problem list")
        base_path = Path(__file__).parent
        filenameEasy, headersEasy = urllib.request.urlretrieve(urlEasy, filename= base_path / 'Easy/problemList.txt')
        filenameMedium, headersMedium = urllib.request.urlretrieve(urlMedium, filename= base_path / 'Medium/problemList.txt')
        filenameHard, headersHard = urllib.request.urlretrieve(urlHard, filename= base_path / 'Hard/problemList.txt')
        print(filenameEasy)
        print(filenameMedium)
        print(filenameHard)
        
        f = open(filename)
        print(f.read())
        
        # using https://gist.github.com/oculushut/193a7c2b6002d808a791
        #pick n random numbers within the num problems in the fetched file and make sure they are not the same
        for i in range(0, numProblems):
            newRand = random.randrange(0, len(fileFetched))
            if newRand not in indicies:
                indicies.append(newRand)
                problems.append(problemList[i])
        return problems
    
    def loadProblem(problem):
        # somehow open the problem on screen -- with timer and allowing person to edit
        print("test")
        
    def startTest(numProblems = 2, timer = 115, difficulties = [3,1]):
        problems = []
        fetchRandomProblems(numProblems, difficulties)
        for problem in problems:
            loadProblem(problem)
            
