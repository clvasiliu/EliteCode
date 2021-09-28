#TODOS:
# Add testing features... maybe custom testing too?
# Add more problems to the list
# Figure our counter issues
# Add implementation for fetching difficulty(randomly) or setting on launch

import urllib.request
import random
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from pathlib import Path

class CircularLinkedList:
    def __init__(self, items):
        self.items = items
        self.currPtr = 0

    def setPtr(self, num):
        self.currPtr = num

    def getIndex(self):
        return self.currPtr
        
    def curr(self):
        return self.items[self.currPtr]
        
    def next(self):
        self.currPtr += 1
        if self.currPtr >= len(self.items):
            self.currPtr = 0
        return self.items[self.currPtr]

class EliteCode:
    def fetchRandomProblems(numProblems, difficulties):
        # Chooses n random problem and fetches the prompts, skeleton and solutions from github
        problems = []
        indicies = []
        #fetch list of problems
        urlEasy = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Easy/problemList.json"
        urlMedium = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Medium/problemList.json"
        urlHard = "https://raw.githubusercontent.com/clvasiliu/EliteCode/main/Hard/problemList.json"
        print("Fetching latest problem list")
        base_path = Path(__file__).parent

        #fetch the updated problem lists
        filenameEasy, headersEasy = urllib.request.urlretrieve(urlEasy, filename= base_path / 'Easy/problemList.json')
        filenameMedium, headersMedium = urllib.request.urlretrieve(urlMedium, filename= base_path / 'Medium/problemList.json')
        filenameHard, headersHard = urllib.request.urlretrieve(urlHard, filename= base_path / 'Hard/problemList.json')
        
        f = open(filenameEasy)
        jsonData = json.load(f)
        
        #pick n random numbers within the num problems in the fetched file and make sure they are not the same
        print("Selecting random problems of specified difficulty") # doesnt do difficulty yet but you get the point
        while len(problems) < numProblems:
            newRand = random.randrange(0, len(jsonData))
            if newRand not in indicies:
                indicies.append(newRand)
                print("Selected problem:")
                print(jsonData[str(newRand)]["name"])
                problems.append(jsonData[str(newRand)])
        f.close()
        return problems

    def downloadProblems(problems):
        base_path = Path(__file__).parent
        fps = []
        for problem in problems:
            print("Now Downloading:")
            print(problem['name'])
            problemUrl = problem["url"]
            filename, headers = urllib.request.urlretrieve(problemUrl, filename= base_path / ('Problems/' + problem['name'] + '.py'))
            fps.append(filename)
        return CircularLinkedList(fps)

    #next 2 functions from:
    #https://thecleverprogrammer.com/2020/09/25/text-editor-gui-with-python/
    def openNextProblem(problems, txt_edit, window, testResults, label):
        """Open a file for editing."""
        if label['text'] != "xxx":
            testResults['text'] = ""
            if txt_edit.get(1.0, tk.END) != "\n":
                EliteCode.saveProblemFile(problems.curr(), txt_edit, window, label)
                txt_edit.delete(1.0, tk.END)
            filepath = problems.next()
            if not filepath:
                return
            txt_edit.delete(1.0, tk.END)
            with open(filepath, "r") as input_file:
                text = input_file.read()
                txt_edit.insert(tk.END, text)
            window.title(f"EliteCode - Exam in Progress")

    def saveProblemFile(problemFp, txt_edit, window, label):
        """Save the current file as a new file."""
        if label['text'] != "xxx":
            filepath = problemFp
            if not filepath:
                return
            with open(filepath, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
            window.title(f"EliteCode - Save Complete")
        
    def loadProblem(problems, timeLimit, problemsMD):
        # somehow open the problem on screen -- with timer and allowing person to edit
        window = tk.Tk()
        window.title("EliteCode")
        window.rowconfigure(0, minsize=800, weight=1)
        window.columnconfigure(1, minsize=800, weight=1)

        txt_edit = tk.Text(window)
        fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

        label = tk.Label(fr_buttons, text="xxx", fg="Red")
        label.grid(row=0, column=0, sticky='ew', padx=5)
        
        testResultsLabel = tk.Label(fr_buttons, text="Test Results:")
        testResultsLabel.grid(row=5, column=0, sticky='ew', padx=5)
        
        testResults = tk.Label(fr_buttons)
        testResults.grid(row=6, column=0, sticky='ew', padx=5)

        btn_start = tk.Button(fr_buttons, text="Start Practicing", command=lambda: EliteCode.startCountdown(timeLimit, label, problems, txt_edit, window, problemsMD, testResults))
        btn_next = tk.Button(fr_buttons, text="Next Problem", command=lambda: EliteCode.openNextProblem(problems, txt_edit, window, testResults, label))
        btn_save = tk.Button(fr_buttons, text="Save", command=lambda: EliteCode.saveProblemFile(problems.curr(), txt_edit, window, label))
        btn_test = tk.Button(fr_buttons, text="Run Tests", command=lambda: EliteCode.testProblem(problemsMD[problems.getIndex()], problems.curr(), testResults, txt_edit, window, label))
        
        btn_start.grid(row=1, column=0, sticky="ew", padx=5, pady=15)
        btn_next.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_test.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")

        window.mainloop()

    def startCountdown(timeLimit, label, problems, txt_edit, window, problemsMD, testResults):
        if label['text'] == "xxx":
            print("Starting Exam")
            EliteCode.countdown(timeLimit, label, window, problems, txt_edit, problemsMD, testResults)
            EliteCode.openNextProblem(problems, txt_edit, window, testResults, label)

    # taken from:
    # https://stackoverflow.com/questions/34029223/basic-tkinter-countdown-timer
    def countdown(count, label, window, problems, txt_edit, problemsMD, testResults):
        # change text in label
        label['text'] = count

        if count > 0:
            # call countdown again after 60000ms (1min)
            window.after(60000, EliteCode.countdown, count-1, label, window, problems, txt_edit, problemsMD)
        else:
            EliteCode.saveProblemFile(problems.curr(), txt_edit, window)
            txt_edit.delete(1.0, tk.END)
            EliteCode.testCode(problems, problemsMD, testResults)

    def testProblem(problemMD, problem, testResults, txt_edit, window, label):
        if label['text'] != "xxx":
            EliteCode.saveProblemFile(problem, txt_edit, window, label)
            print("Running tests for:")
            print(problemMD['name'])
            __currProblem = __import__(("Problems." + problemMD["name"]), globals(), locals(), [problemMD["name"]], 0)
            __function = getattr(__currProblem, problemMD["name"])
            result = __function(1,2)
            testResults['text'] = result #         Testing.runTests(__function, problemMD) -- ideally import another class using same method as above and run tests from it,
                                                  #                                                    outputting all the results as a string that can be used here
            print(__function(1, 2))

    def testCode(problems, problemsMD, testResults):
        #do stuff
        #print(Problems.(problems.curr)(1, 2))
        print("Running all tests on code")
        for problemMD in problemsMD:
            print(problemMD)
            EliteCode.testProblem(problemMD, testResults)
    
    def startTest(numProblems = 2, timeLimit = 115, difficulties = [1, 1]):
        problems = EliteCode.fetchRandomProblems(numProblems, difficulties)
        problemFps = EliteCode.downloadProblems(problems)
        EliteCode.loadProblem(problemFps, timeLimit, problems)

EliteCode.startTest(timeLimit = 1)
