
from customtkinter import *
import configparser as cp
import ast
from functools import partial
from programFrame import timeOk
from guiFunctions import optionsAct, options, issArr, actList,filterOptions, is_decimal, postMessage
from programEntries import updateProgEntry, removeProgEntry, unableEntry, enableEntry


dir = os.path.dirname(os.path.abspath(__file__))

mainFrame = None
yourPFrame = None

def createYourProgramed(master):
    global mainFrame

    mainFrame = CTkFrame(master, bg_color="#0a0a0a", corner_radius=0)
    pFrame()
    return mainFrame

def pFrame():
    global dir, yourPFrame, mainFrame
    yourPFrame = CTkFrame(mainFrame)
    yourPFrame.pack(fill="x", pady=15, padx=15)


    
    config = cp.ConfigParser()
    config.read(f"{dir}/.data/.data.cfg")
    totCount = config['ProgramedEntries'].getint('totCount')

    timeLabel = CTkLabel(yourPFrame, text='Time')
    timeLabel.configure(font=("", 26, "bold"))
    timeLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    daysLabel = CTkLabel(yourPFrame, text='Days')
    daysLabel.configure(font=("", 26, "bold"))
    daysLabel.grid(row=0, column=1, padx=10, pady=10, sticky='w', columnspan=5)

    issLabel = CTkLabel(yourPFrame, text='Issue')
    issLabel.configure(font=("", 26, "bold"))
    issLabel.grid(row=0, column=6, padx=10, pady=10, sticky='w')

    actLabel = CTkLabel(yourPFrame, text='Activity')
    actLabel.configure(font=("", 26, "bold"))
    actLabel.grid(row=0, column=7, padx=10, pady=10, sticky='w')

    hoursLabel = CTkLabel(yourPFrame, text='Hours')
    hoursLabel.configure(font=("", 26, "bold"))
    hoursLabel.grid(row=0, column=8, padx=10, pady=10, sticky='w')

    commLabel = CTkLabel(yourPFrame, text='Comment')
    commLabel.configure(font=("", 26, "bold"))
    commLabel.grid(row=0, column=9, padx=10, pady=10, sticky='w')

    reloadBtn = CTkButton(yourPFrame, text='RELOAD', width=100)
    reloadBtn.configure(command=reload)
    reloadBtn.grid(row=0, column = 11, padx=5, pady=10)


    for i in range(totCount):
        entryStr = config["ProgramedEntries"][f'redassist-{i+1}']
        entry = ast.literal_eval(entryStr)
        
    # -- time --
        timeText = StringVar()

        timeEntry = CTkEntry(yourPFrame, textvariable=timeText)
        timeEntry.configure(width=90, font=("", 11), state='disable')
        min = entry['minute']
        hr = entry['hrs']
        if min<10: 
            timeText.set(f"{hr}:0{min}")
        else:
            timeText.set(f"{hr}:{min}")
        #print (timeEntry.get())
        timeEntry.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')

    # -- days --
        monCheck = CTkCheckBox(yourPFrame, text='MON')
        monCheck.configure(width=30, font=("", 11), checkbox_width=20, checkbox_height=20)
        monCheck.grid(row=i+1, column=1, pady=10, padx=15, sticky='w')
        if 'MON' in entry['days']:
            monCheck.select()
        monCheck.configure(state='disable')

        tueCheck = CTkCheckBox(yourPFrame, text='TUE')
        tueCheck.configure(width=30, font=("", 11), checkbox_width=20, checkbox_height=20)
        tueCheck.grid(row=i+1, column=2, pady=10, padx=15, sticky='w')
        if 'TUE' in entry['days']:
            tueCheck.select()
        tueCheck.configure(state='disable')

        wedCheck = CTkCheckBox(yourPFrame, text='WED')
        wedCheck.configure(width=30, font=("", 11), checkbox_width=20, checkbox_height=20)
        wedCheck.grid(row=i+1, column=3, pady=10, padx=15, sticky='w')
        if 'WED' in entry['days']:
            wedCheck.select()
        wedCheck.configure(state='disable')

        thuCheck = CTkCheckBox(yourPFrame, text='THU')
        thuCheck.configure(width=30, font=("", 11), checkbox_width=20, checkbox_height=20)
        thuCheck.grid(row=i+1, column=4, pady=10, padx=15, sticky='w')
        if 'THU' in entry['days']:
            thuCheck.select()
        thuCheck.configure(state='disable')

        friCheck = CTkCheckBox(yourPFrame, text='FRI')
        friCheck.configure(width=30, font=("", 11), checkbox_width=20, checkbox_height=20)
        friCheck.grid(row=i+1, column=5, pady=10, padx=15, sticky='w')
        if 'FRI' in entry['days']:
            friCheck.select()
        friCheck.configure(state='disable')
        
    # -- issue --
        comboIss = CTkComboBox(yourPFrame, values=options)
        comboIss.configure(width=250, font=("", 11), text_color_disabled='gray84')
        comboIss.grid(row=i+1, column=6, padx=10, pady=10, sticky='w')
        comboIss.bind("<Key>", partial(filterOptions, combobox=comboIss, opts=options))
        
        comboIss.set(entry['issue']) 
        comboIss.configure(state='disable')


    # -- activity -- 
        comboAct = CTkComboBox(yourPFrame, values=optionsAct)
        comboAct.configure(width=125, font=("", 11), text_color_disabled='gray84')
        comboAct.grid(row=i+1, column=7, padx=10, pady=10, sticky='w')
        comboAct.bind("<Key>", partial(filterOptions, combobox=comboAct, opts=optionsAct))
        comboAct.set(entry['activity'])
        comboAct.configure(state='disable')

    # -- hours --
        hrsText = StringVar()

        hrsEntry = CTkEntry(yourPFrame, textvariable=hrsText)
        hrsEntry.configure(width=125, font=("", 11), state='disable')

        hrsText.set(entry['hours'])
        hrsEntry.grid(row=i+1, column=8, padx=10, pady=10, sticky='w')

    # -- comment --
        commText = StringVar()

        commEntry = CTkEntry(yourPFrame, textvariable=commText)
        commEntry.configure(width=125, font=("", 11), state='disable')

        commText.set(entry['comments'])
        commEntry.grid(row=i+1, column=9, padx=10, pady=10, sticky='w')

    # -- buttons --
        widgets = [timeEntry, comboIss, comboAct, hrsEntry, commEntry]
        checks = [monCheck, tueCheck, wedCheck, thuCheck, friCheck]

        disBtn = CTkButton(yourPFrame, width=100)
        disBtn.grid(row=i+1, column = 10, padx=5, pady=10)

        active = config['ProgramedEntries'].getboolean(f'redassist-{i+1}_Active')
        print (active)
        if active:
            disBtn.configure(text='Disable', command=lambda i=i :unableEntry(i+1))
        else:
            disBtn.configure(text='Enable', command=lambda i=i :enableEntry(i+1))
            for widget in widgets:
                try:
                    widget.configure(text_color_disabled='gray45')
                except:
                    widget.configure(text_color='gray45')
            for widget in checks:
                widget.configure(text_color='gray45')
            


        delBtn = CTkButton(yourPFrame, text='Delete', width=100)
        delBtn.configure(command= lambda id = i+1: removeProgEntry(id), fg_color="#BF3A3A", hover_color="#992e2e")
        delBtn.grid(row=i+1, column = 12, padx=5, pady=10)


        

        editBtn = CTkButton(yourPFrame, text='Edit', width=100)
        editBtn.configure(command= lambda widgets = widgets, btn = editBtn, i = i, disBtn = disBtn, checks = checks, delBtn=delBtn: edit(widgets, btn, disBtn, i,checks, delBtn))
        editBtn.grid(row=i+1, column = 11, padx=5, pady=10)


def edit(widgets, btn, disBtn, i, checks, delBtn):
    global yourPFrame
    for widget in widgets:
        widget.configure(state='normal')
    for check in checks:
        check.configure(state='normal')
    btn.grid_remove()
    disBtn.grid_remove()
    delBtn.grid_remove()

    confBtn = CTkButton(yourPFrame, text='Confirm', width=125)
    confBtn.grid(row=i+1, column = 10, padx=5, pady=10)

    canBtn = CTkButton(yourPFrame, text='Cancel', width=125, fg_color="#BF3A3A", hover_color="#992e2e")
    canBtn.grid(row=i+1, column = 11, padx=5, pady=10)


    confBtn.configure(command=lambda widgets=widgets, confBtn=confBtn, canbtn=canBtn, editbtn=btn,i=i, disBtn = disBtn, checks=checks, delBtn=delBtn: confirm(widgets,confBtn,canbtn, editbtn, i,disBtn, checks, delBtn))
    canBtn.configure(command=lambda widgets=widgets, confBtn=confBtn, canbtn=canBtn, editbtn=btn, disBtn=disBtn,i=i, checks=checks, delBtn=delBtn: cancel(widgets, confBtn,canbtn, editbtn, disBtn, i,checks, delBtn))


def reload():
    global yourPFrame, mainFrame
    yourPFrame.destroy()
    pFrame()

def confirm(widgets, confbtn, canbtn, editbtn, i, disBtn, checks, delBtn):
    global options, mainFrame, optionsAct, issArr, actList

    time = widgets[0].get()

    isgood = True

    if not timeOk(widgets[0]):
        widgets[0].configure(text_color="red")
        isgood = False
    
    
    
    if not widgets[1].get() in options:
        widgets[1].configure(text_color="red")
        isgood = False
    if not widgets[2].get() in optionsAct:
        widgets[2].configure(text_color="red")
        isgood = False

    if not is_decimal(widgets[3].get()) or float(widgets[3].get()) <= 0:
        widgets[3].configure(text_color="red")
        isgood = False



    if isgood:
        issOpId = options.index(widgets[1].get())
        actOpId = optionsAct.index(widgets[2].get())

        issue = issArr[issOpId]['subject']
        issue_id = issArr[issOpId]['id']

        activity = actList[actOpId]['name']
        activity_id = actList[actOpId]['id']

        time = widgets[0].get().split(':')
        minute = time[1]
        hr = time[0]
        if minute[0] == '0':
            minute = minute[1:]
        minute = int(minute)
        hr = int(hr)
        days = []
        for check in checks:
            day = check.cget('text')
            if check.get():
                days.append(day)

        confbtn.destroy()
        canbtn.destroy()
        editbtn.grid(row=i+1, column = 11, padx=5, pady=10)
        disBtn.grid(row=i+1, column = 10, padx=5, pady=10)
        delBtn.grid(row=i+1, column = 12, padx=5, pady=10)

        for widget in widgets:
            widget.configure(state='disable')
        for check in checks:
            check.configure(state='disable')

        entry = {'issue_id': issue_id, 'activity_id':activity_id, 'hours':widgets[3].get(), 'comments':widgets[4].get() , 'issue':issue, 'activity':activity}
        updateProgEntry(i+1,entry,minute,hr, days)
        
        

        
        
def cancel(widgets, confbtn, canbtn, editbtn,disBtn, i, checks, delBtn):
    for widget in widgets:
        widget.configure(state='disable')
            
    for check in checks:
        check.configure(state='disable')
    
    canbtn.destroy()
    confbtn.destroy()
    disBtn.grid(row=i+1, column = 10, padx=5, pady=10)
    editbtn.grid(row=i+1, column = 11, padx=5, pady=10)
    delBtn.grid(row=i+1, column = 12, padx=5, pady=10)

