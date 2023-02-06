from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkEntry, CTkComboBox
import time
from functools import partial
from guiFunctions import options, optionsAct, issArr, actList, filterOptions, hrsAdd, is_decimal, postMessage
import threading as thr
from datetime import datetime
from tkinter import StringVar
from api import timeEntryPost


startBtn = None
resetBtn = None
postBtn = None

actCrLab = None
cronometer = None
comboCrAct = None
commCrEntry = None
comboIssCr = None
#----------------- Cronometer ---------------

def createCronometer(master):
    global options, optionsAct, startBtn, resetBtn, postBtn, actCrLab, actCrLab, cronometer, comboCrAct, commCrEntry, comboIssCr

    cronometer = CTkFrame(master=master, bg_color="#0a0a0a", corner_radius=0)

    # -- Frame --
    cronoF = CTkFrame(cronometer)
    cronoF.pack(fill="x", pady=15, padx=15)

    # -- Issue --

    # label
    issCrLab = CTkLabel(cronoF, text="Issue: ")
    issCrLab.configure( font=("", 26, 'bold') )
    issCrLab.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # options

    comboIssCr = CTkComboBox(cronoF, values=options)

    comboIssCr.configure(width=500, font=("", 18))
    comboIssCr.grid(row=0, column=1, padx=10, pady=10, sticky='w', columnspan=10)
    comboIssCr.set('')
    comboIssCr.bind("<Key>", partial(filterOptions, combobox=comboIssCr, opts=options))


    # -- Activity --

    # label

    actCrLab = CTkLabel(cronoF, text="Activity: ")
    actCrLab.configure( font=("", 26, 'bold'), justify="left" )
    actCrLab.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    # combobox

    comboCrAct = CTkComboBox(cronoF, values=optionsAct)
    comboCrAct.configure(width=250, font=("", 18))
    comboCrAct.grid(row=1, column=1, padx=10, pady=10, sticky='w', columnspan=8)
    comboCrAct.set('')
    comboCrAct.bind("<Key>", partial(filterOptions, combobox=comboCrAct, opts=optionsAct))

    # -- Comment --

    # label

    commCrLab = CTkLabel(cronoF, text="Comentario: ")
    commCrLab.configure( font=("", 26, 'bold'), justify="left" )
    commCrLab.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # entry
    commCrEntry = CTkEntry(cronoF)
    commCrEntry.configure(width=800, font=("", 18))
    commCrEntry.grid(row=2, column=1, padx=10, pady=10, sticky='w', columnspan=15)


    # -- Timer --

    # label

    actCrLab = CTkLabel(cronoF, text="Cronometro: ")
    actCrLab.configure( font=("", 26, 'bold'), justify="left" )
    actCrLab.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    # time 

    actCrLab = CTkLabel(cronoF, text="0:00:00")
    actCrLab.configure( font=("", 26, 'bold'), justify="left" )
    actCrLab.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    # start button

    startBtn = CTkButton(cronoF, text="Inciar", command=startTimer)
    startBtn.configure(font=("", 20, "bold"))
    startBtn.grid(row=4, column=0, padx=10, pady=10, sticky='w')


    # reset button

    resetBtn = CTkButton(cronoF, text="Reiniciar", command=resetTimer)
    resetBtn.configure(font=("", 20, "bold"))

    # post button

    postBtn = CTkButton(cronoF, text="Cargar", command=postTimer)
    postBtn.configure(font=("", 20, "bold"))



    return cronometer




# timer function

timRun = False

sec = 0
min = 0
hr = 0

def timer():
    global actCrLab, timRun, sec, min, hr
    while timRun:
        time.sleep(1)
        if sec != 59:
            sec += 1
        else:
            sec = 0
            if min != 59:
                min += 1
            else: 
                min = 0
                hr += 1
        if sec < 10:
            secT = f"0{sec}"
        else: secT = str(sec)
        if min < 10:
            minT = f"0{min}"
        else: minT = str(min)
        hrT = str(hr)
        timeTxt = f"{hrT}:{minT}:{secT}"
        actCrLab.configure(text=timeTxt)

# start function

def startTimer():
    global timRun, startBtn, resetBtn, postBtn
    timRun = True
    startBtn.configure(text="Parar", command=stopTimer)
    timeThr = thr.Thread(target=timer)
    resetBtn.grid_remove()
    postBtn.grid_remove()
    
    timeThr.start()

# stop function

def stopTimer():
    global timRun, resetBtn, postBtn
    timRun = False
    resetBtn.grid(row=4, column=1, padx=10, pady=10, sticky='w')
    postBtn.grid(row=4, column=2, padx=10, pady=10, sticky='w')
    startBtn.configure(text="Iniciar", command=startTimer)

# reset funcion

def resetTimer():
    global actCrLab, sec, min, hr
    actCrLab.configure(text="00:00:00")
    sec=0
    min=0
    hr=0

# post timer

def postTimer():
    global cronometer, comboCrAct, commCrEntry, comboIssCr, options, optionsAct, issArr, actList, hr, min, sec
    if ( comboIssCr.get() in options ) and ( comboCrAct.get() in optionsAct ):
        # -- Frame --
        postF = CTkFrame(cronometer)
        postF.pack(fill="x", pady=15, padx=15)

        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day
        

        issOpId = options.index(comboIssCr.get())
        actOpId = optionsAct.index(comboCrAct.get())

        issue = issArr[issOpId]['subject']
        issue_id = issArr[issOpId]['id']

        activity = actList[actOpId]['name']
        activity_id = actList[actOpId]['id']

        hrs = hr + min/60 + sec/3600
        hrs = round(hrs, 2)


        comment = commCrEntry.get()
        # -- date --
        dateL = CTkLabel(postF, text=f"{day}/{month}/{year}")

        dateL.configure( font=("", 26, 'bold'), justify="left" )
        dateL.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # issue / activity
        issueL = CTkLabel(postF, text=f"{issue}, {activity}")
        issueL.configure( font=("", 26, 'bold'), justify="left" )
        issueL.grid(row=1, column=0, padx=10, pady=10, sticky='w', columnspan=6)


        # -- comment --
        cmmL = CTkLabel(postF, text=f'"{comment}"')
        cmmL.configure( font=("", 26, 'bold'), justify="left" )
        if comment != "":
         cmmL.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # hours

        # label

        hrsLab = CTkLabel(postF, text="Horas: ")
        hrsLab.configure( font=("", 26, 'bold'), justify="left" )
        hrsLab.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # entry 

        hrsCrText = StringVar()

        hrsCrEntry = CTkEntry(postF, textvariable=hrsCrText)
        hrsCrEntry.configure(width=125, font=("", 18))
        hrsCrText.set(str(hrs))
        hrsCrEntry.grid(row=3, column=2, padx=10, pady=10, sticky='w')

        subCrBut = CTkButton(postF, text="-", command= lambda: hrsAdd(hrsCrEntry, hrsCrText, False))
        subCrBut.configure(width=30, font=("", 16, "bold"))
        subCrBut.grid(row=3, column=1, pady=10, sticky='w')

        addCrBtn = CTkButton(postF, text="+", command= lambda: hrsAdd(hrsCrEntry, hrsCrText, True))
        addCrBtn.configure(width=30, font=("", 16, "bold"))
        addCrBtn.grid(row=3, column=3, pady=10, sticky='w')

        if month < 10:
            monthStr = f"0{month}"
        else: 
            monthStr = str(month)
        if day < 10:
            dayStr = f"0{day}"
        else:
            dayStr = str(day)
        yearStr = str(year)

        spent_on = f"{yearStr}-{monthStr}-{dayStr}"

        entry = {'issue_id': issue_id, 'activity_id':activity_id, 'hours':'', 'spent_on':spent_on, 'comments':comment, 'issue':issue, 'activity': activity}

        # confirm post
        msg = f"{day}/{month}/{year}\n{issue}: {activity}\nComentario: {comment}"
        confBtn = CTkButton(postF, text="Confirmar", command=lambda:confPost(entry, hrsCrText, msg))
        confBtn.configure(font=("", 20, "bold"))
        confBtn.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # cancel post
        cancBtn = CTkButton(postF, text='Cancelar', command=lambda: cancelPost(postF))
        cancBtn.configure(font=("", 20, "bold"), fg_color="#BF3A3A", hover_color="#992e2e")
        cancBtn.grid(row=4, column=1, padx=10, pady=10, sticky='w', columnspan=6)
# confirm post

def confPost(entry, hrTxt, msg):
    if ( is_decimal(hrTxt.get()) ) and ( float(hrTxt.get()) > 0):
        entry['hours'] = hrTxt.get()


        msg = f"{msg}\n{hrTxt.get()}"
        response = timeEntryPost(entry)

        
        if response == 201:
            postMessage(succes=True, frame=cronometer, entry=entry)
        else:
            postMessage(succes=False, frame=cronometer)

# cancel post
def cancelPost(postF):
    postF.destroy()

