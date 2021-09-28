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

    def curr(self):
        return self.items[self.currPtr]
        
    def next(self):
        currItem = self.items[self.currPtr]
        self.currPtr += 1
        if self.currPtr >= len(self.items):
            self.currPtr = 0
        return currItem

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
        for i in range(0, numProblems):
            newRand = random.randrange(0, len(jsonData))
            if newRand not in indicies:
                indicies.append(newRand)
                problems.append(jsonData[str(newRand)])
        print(problems)
        f.close()
        return problems

    def downloadProblems(problems):
        base_path = Path(__file__).parent
        fps = []
        for problem in problems:
            print("Now Downloading:\n")
            print(problem['name'])
            problemUrl = problem["url"]
            filename, headers = urllib.request.urlretrieve(problemUrl, filename= base_path / ('Problems/' + problem['name'] + '.py'))
            print(filename)
            fps.append(filename)
        return CircularLinkedList(fps)

    #next 2 functions from:
    #https://thecleverprogrammer.com/2020/09/25/text-editor-gui-with-python/
    def openNextProblem(problemFp, txt_edit, window):
        """Open a file for editing."""
        filepath = problemFp
        if not filepath:
            return
        txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
        window.title(f"EliteCode - Exam in Progress")

    def saveProblemFile(problemFp, txt_edit, window):
        """Save the current file as a new file."""
        filepath = problemFp
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
            output_file.write(text)
        window.title(f"EliteCode - Save Complete")
        
    def loadProblem(problems, timeLimit):
        # somehow open the problem on screen -- with timer and allowing person to edit
        window = tk.Tk()
        window.title("EliteCode")
        window.rowconfigure(0, minsize=800, weight=1)
        window.columnconfigure(1, minsize=800, weight=1)

        txt_edit = tk.Text(window)
        fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

        label = tk.Label(fr_buttons, text="xxx", fg="Red")
        label.grid(row=0, column=0, sticky='ew', padx=5)
        
        btn_start = tk.Button(fr_buttons, text="Start Practicing", command=lambda: EliteCode.startCountdown(timeLimit, label, problems.next(), txt_edit, window))
        btn_open = tk.Button(fr_buttons, text="Next Problem", command=lambda: EliteCode.openNextProblem(problems.next(), txt_edit, window))
#        EliteCode.countdown(timeLimit, label, window)
        btn_save = tk.Button(fr_buttons, text="Save", command=lambda: EliteCode.saveProblemFile(problems.curr(), txt_edit, window))
        
        btn_start.grid(row=1, column=0, sticky="ew", padx=5, pady=15)
        btn_open.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")

        window.mainloop()

    def startCountdown(timeLimit, label, problem, txt_edit, window):
        EliteCode.openNextProblem(problem, txt_edit, window)
        EliteCode.countdown(timeLimit, label, window)

    # taken from:
    # https://stackoverflow.com/questions/34029223/basic-tkinter-countdown-timer
    def countdown(count, label, window):
        # change text in label        
        label['text'] = count
        print(count)

        if count > 0:
            # call countdown again after 60000ms (1min)
            window.after(60000, EliteCode.countdown, count-1, label, window)
        else:
            ptr = problems.curr()
            while problems.next() != ptr:
                EliteCode.saveProblemFile(problems.curr(), txt_edit, window)
            EliteCode.testCode()

    def testCode():
        #do stuff
        print("testing code")
    
    def startTest(numProblems = 2, timeLimit = 115, difficulties = [1, 1]):
        problems = EliteCode.fetchRandomProblems(numProblems, difficulties)
        problemFps = EliteCode.downloadProblems(problems)
        EliteCode.loadProblem(problemFps, timeLimit)

EliteCode.startTest()
