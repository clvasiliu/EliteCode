# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import urllib.request
import random
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from pathlib import Path

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
        print(filenameEasy)
        print(filenameMedium)
        print(filenameHard)
        
        f = open(filenameEasy)
        jsonData = json.load(f)
        print(len(jsonData))
        
        #pick n random numbers within the num problems in the fetched file and make sure they are not the same
        for i in range(0, numProblems):
            newRand = random.randrange(0, len(jsonData))
            if newRand not in indicies:
                indicies.append(newRand)
                problems.append(jsonData[str(newRand)])
        print(problems)
        return problems

    #next 2 functions from:
    #https://thecleverprogrammer.com/2020/09/25/text-editor-gui-with-python/
    def openNextProblem():
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
        window.title(f"Thecleverprogrammer - {filepath}")

    def saveProblemFile():
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
            output_file.write(text)
        window.title(f"Thecleverprogrammer - {filepath}")
    
    def loadProblem(problem, timeLimit):
        # somehow open the problem on screen -- with timer and allowing person to edit
        window = tk.Tk()
        window.title("Thecleverprogrammer")
        window.rowconfigure(0, minsize=800, weight=1)
        window.columnconfigure(1, minsize=800, weight=1)

        txt_edit = tk.Text(window)
        fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
        btn_open = tk.Button(fr_buttons, text="Next Problem", command=EliteCode.openNextProblem)
        btn_save = tk.Button(fr_buttons, text="Save", command=EliteCode.saveProblemFile)

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")

        label = tk.Label(window)
        label.place(x=35, y=75)
        EliteCode.countdown(timeLimit, label, window)
        
        window.mainloop()

    # taken from:
    # https://stackoverflow.com/questions/34029223/basic-tkinter-countdown-timer
    def countdown(count, label, window):
        # change text in label        
        label['text'] = count

        if count > 0:
            # call countdown again after 60000ms (1min)
            window.after(60000, EliteCode.countdown, count-1, label, window)
    
    def startTest(numProblems = 2, timeLimit = 115):
        problems = []
        fetchRandomProblems(numProblems, difficulties)
        for problem in problems:
            loadProblem(problem, timeLimit)

problems = EliteCode.fetchRandomProblems(2, [1])
EliteCode.loadProblem(problems[0], 100)
