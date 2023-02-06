
from customtkinter import *
from functools import partial
from guiFunctions import options, optionsAct, issArr, actList, filterOptions, hrsAdd, is_decimal, postMessage
from programEntries import createJob
from datetime import datetime


mainFrame = None
combo = None
comboAct = None
hrsText = None
commEntry = None
monCheck = None
tueCheck = None
wedCheck = None
tueCheck = None
friCheck = None
progFrame = None
timeText = None
timeEntry = None

def createProgramFrame(master):
    global optionsAct, options, mainFrame, combo, comboAct, hrsText, monCheck, tueCheck, wedCheck, tueCheck, friCheck, commEntry, progFrame, timeText, timeEntry

    mainFrame = CTkFrame(master=master, bg_color="#0a0a0a", corner_radius=0)

    progFrame = CTkFrame(mainFrame)
    progFrame.pack(fill="x", pady=15, padx=15)

    # -- Issue --

    # label
    issueLab = CTkLabel(progFrame, text="Issue: ")
    issueLab.configure(font=("", 26, "bold"))
    issueLab.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # combo box
    

    combo = CTkComboBox(progFrame, values=options)
    combo.configure(width=500, font=("", 18))
    combo.grid(row=0, column=1, padx=10, pady=10, sticky='w', columnspan=10)
    combo.set('')
    combo.bind("<Key>", partial(filterOptions, combobox=combo, opts=options))


    # -- Activity --

    # label

    actLab = CTkLabel(progFrame, text="Activity: ")
    actLab.configure( font=("", 26, "bold"))
    actLab.grid(row=1, column=0, padx=10, pady=10, sticky='w', columnspan=2)

    # combo box

    comboAct = CTkComboBox(progFrame, values=optionsAct)
    comboAct.configure(width=250, font=("", 18))
    comboAct.grid(row=1, column=1, padx=10, pady=10, sticky='w', columnspan=8)
    comboAct.bind("<Key>", partial(filterOptions, combobox=comboAct, opts=optionsAct))
    comboAct.set('')


    # -- Hours --

    # label

    hrsLab = CTkLabel(progFrame, text="Hours: ")
    hrsLab.configure(font=("", 26, "bold")) 
    hrsLab.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # entry

    hrsText = StringVar()

    hrsEntry = CTkEntry(progFrame, textvariable=hrsText)
    hrsEntry.configure(width=185, font=("", 18)) 
    hrsText.set("0.0")
    hrsEntry.grid(row=2, column=2, padx=10, pady=10, sticky='w', columnspan=2)

    # buttons
    


    subBut = CTkButton(progFrame, text="-", command= lambda: hrsAdd(hrsEntry, hrsText, False))
    subBut.configure(width=30, font=("", 16, "bold"))
    subBut.grid(row=2, column=1, pady=10, sticky='w')

    addBtn = CTkButton(progFrame, text="+", command= lambda: hrsAdd(hrsEntry, hrsText, True))
    addBtn.configure(width=30, font=("", 16, "bold"))
    addBtn.grid(row=2, column=4, pady=10, sticky='w')

# -- Comment --

    # label

    commLab = CTkLabel(progFrame, text="Comment: ")
    commLab.configure(font=("", 26, "bold"), justify="left")
    commLab.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    # entry
    commEntry = CTkEntry(progFrame)
    commEntry.configure(width=800, font=("", 18))
    commEntry.grid(row=3, column=1, padx=10, pady=10, sticky='w', columnspan=15)    


# -- Time --

    # label
    date = datetime.now()
    timeLab = CTkLabel(progFrame, text="Time: ")
    timeLab.configure(font=("", 26, "bold"))
    timeLab.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # entry

    timeText = StringVar()

    timeEntry = CTkEntry(progFrame, textvariable=timeText)
    timeEntry.configure(width=125, font=("", 18))
    hour = date.hour
    minute = date.minute
    if minute > 55:
        hour += 1
        minute = 0
    elif minute < 3: minute = 0
    elif minute < 8: minute = 5
    elif minute < 10: minute = 10
    elif int(str(minute)[-1]) < 3: minute = int(str(minute)[0] + '0')
    elif int(str(minute)[-1]) < 8: minute = int(str(minute)[0] + '5')
    elif int(str(minute)[-1]) >= 8: minute = int(f"{int(str(minute)[0]) + 1}0")
    if minute < 10: minute = f"0{minute}"

    timeText.set(f"{hour}:{minute}")
    timeEntry.grid(row=4, column=2, padx=10, pady=10, sticky='w', columnspan=2)

    # buttons

    subTimeBut = CTkButton(progFrame, text="-", command= lambda: addHr(False))
    subTimeBut.configure(width=30, font=("", 16, "bold"))
    subTimeBut.grid(row=4, column=1, pady=10, sticky='w')

    addTimeBtn = CTkButton(progFrame, text="+", command= lambda: addHr(True))
    addTimeBtn.configure(width=30, font=("", 16, "bold"))
    addTimeBtn.grid(row=4, column=4, pady=10, sticky='w')
# -- Days --

    

    #label
    daysLabel = CTkLabel(progFrame, text='Days:')
    daysLabel.configure(font=("", 26, "bold"))
    daysLabel.grid(row=5, column=0, padx=10, pady=10, sticky='w')

    # checkboxes
    monCheck = CTkCheckBox(progFrame, text='Monday')
    monCheck.configure(font=("", 18))
    monCheck.grid(row=6, column=0, pady=10, padx=15, sticky='w')

    tueCheck = CTkCheckBox(progFrame, text='Tuesday')
    tueCheck.configure(font=("", 18))
    tueCheck.grid(row=7, column=0, pady=10, padx=15, sticky='w')

    wedCheck = CTkCheckBox(progFrame, text='Wednesday')
    wedCheck.configure(font=("", 18))
    wedCheck.grid(row=8, column=0, pady=10, padx=15, sticky='w')

    thuCheck = CTkCheckBox(progFrame, text='Thursday')
    thuCheck.configure(font=("", 18))
    thuCheck.grid(row=9, column=0, pady=10, padx=15, sticky='w')

    friCheck = CTkCheckBox(progFrame, text='Friday')
    friCheck.configure(font=("", 18))
    friCheck.grid(row=10, column=0, pady=10, padx=15, sticky='w')

    # -- program button --

    progBtn = CTkButton(progFrame, text="Program", command=programEntry)
    progBtn.configure(font=("", 20, "bold"))
    progBtn.grid(row=11, column=0, padx=10, pady=10, sticky='w')
    return mainFrame

def programEntry():
    global optionsAct, options, mainFrame,progFrame, combo, comboAct, hrsText, monCheck, tueCheck, wedCheck, tueCheck, friCheck, issArr, actList, commEntry, timeEntry, timeText

    if ( is_decimal(hrsText.get()) ) and ( combo.get() in options ) and ( comboAct.get() in optionsAct ) and ( float(hrsText.get()) > 0) and timeOk(timeEntry):

        issOpId = options.index(combo.get())
        actOpId = optionsAct.index(comboAct.get())

        issue = issArr[issOpId]['subject']
        issue_id = issArr[issOpId]['id']

        activity = actList[actOpId]['name']
        activity_id = actList[actOpId]['id']
        
        hours = hrsText.get()
        comment = commEntry.get()

        days = []
        if monCheck.get():
            days.append('MON')
        if tueCheck.get():
            days.append('TUE')
        if wedCheck.get():
            days.append('WED')
        if tueCheck.get():
            days.append('THU')
        if friCheck.get():
            days.append('FRI')
        
        timeArr = timeText.get().split(':')
        for num in timeArr:
            if num[0] == '0':
                num = num[1:]
        hr = int(timeArr[0])
        min = int(timeArr[1])



        entry = {'issue_id': issue_id, 'activity_id':activity_id, 'hours':hours, 'comments':comment, 'issue':issue, 'activity':activity}
        exist = createJob(entry, days,hr,min)
        postMessage(exist, mainFrame, progFrame, entry, True)

        
def timeOk(timeEntry):
    text = timeEntry.get()
    timeArr = text.split(':')

    for num in timeArr:
        if num[0] == '0':
            num = num[1:]
        if not num.isdigit() or int(num) < 0:
            return False
    
    if (len(timeArr) != 2) or (int(timeArr[0]) > 23) or (int(timeArr[1]) > 59):
        return False
    else: 
        return True

def addHr(add):
    global timeText, timeEntry
    if timeOk(timeEntry):
        timeArr = timeText.get().split(':')
        for num in timeArr:
            if num[0] == '0':
                num = num[1:]
        hr = int(timeArr[0])
        min = int(timeArr[1])
        if add:
            min += 15
            if min > 59:
                min -= 60
                hr += 1
        else:
            min -= 15
            if min < 0:
                min += 60
                hr -=1
        
        if min<10:
            timeText.set(f"{hr}:0{min}")
        else:
            timeText.set(f"{hr}:{min}")
        