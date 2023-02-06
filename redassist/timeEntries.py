from customtkinter import *
from functools import partial
import calendar
from datetime import datetime 
from api import listEntries, updateEntry
from guiFunctions import optionsAct, options, issArr, actList,filterOptions, is_decimal, postMessage

entriesF = None
timeEntries = None

def createEntries(notebook):
    global optionsAct, entriesF, timeEntries
    timeEntries = CTkFrame(master=notebook, bg_color="#0a0a0a", corner_radius=0)
    
    # frame 

    entriesF = CTkFrame(timeEntries)
    entriesF.pack(fill="x", pady=15, padx=15)

    entrieslist = getList()
    
    for i in range(15):
        entry = entrieslist[i]


        #date
        dateText = StringVar()

        dateEntry = CTkEntry(entriesF, textvariable=dateText)
        dateEntry.configure(width=90, font=("", 11), state='disable')
        date = entry['spent_on'].split('-')

        dateText.set(f"{date[2]}/{date[1]}/{date[0]}")
        #print (dateEntry.get())
        dateEntry.grid(row=i, column=1, padx=10, pady=10, sticky='w')

        # issue
        comboIss = CTkComboBox(entriesF, values=options)
        comboIss.configure(width=250, font=("", 11), text_color_disabled='gray84')
        comboIss.grid(row=i, column=2, padx=10, pady=10, sticky='w')
        comboIss.bind("<Key>", partial(filterOptions, combobox=comboIss, opts=options))
        
        issname = ''
        j=0
        while issname == '' and j < len(options):
            if issArr[j]['id'] == entry['issue']['id']:
                issname = issArr[j]['subject']
            else:
                j += 1
        comboIss.set(issname) 
        comboIss.configure(state='disable')


        # activity 
        comboAct = CTkComboBox(entriesF, values=optionsAct)
        comboAct.configure(width=125, font=("", 11), text_color_disabled='gray84')
        comboAct.grid(row=i, column=3, padx=10, pady=10, sticky='w')
        comboAct.bind("<Key>", partial(filterOptions, combobox=comboAct, opts=optionsAct))
        comboAct.set(entry['activity']['name'])
        comboAct.configure(state='disable')

        # hours
        hrsText = StringVar()

        hrsEntry = CTkEntry(entriesF, textvariable=hrsText)
        hrsEntry.configure(width=125, font=("", 11), state='disable')

        hrsText.set(entry['hours'])
        hrsEntry.grid(row=i, column=4, padx=10, pady=10, sticky='w')

        # comment
        commText = StringVar()

        commEntry = CTkEntry(entriesF, textvariable=commText)
        commEntry.configure(width=125, font=("", 11), state='disable')

        commText.set(entry['comments'])
        commEntry.grid(row=i, column=5, padx=10, pady=10, sticky='w')

        # buttons
        widgets = [dateEntry, comboIss, comboAct, hrsEntry, commEntry]
        editBtn = CTkButton(entriesF, text='Edit', width=125)
        editBtn.configure(command= lambda widgets = widgets, btn = editBtn, i = i, id = entry['id']: edit(widgets, btn, i, id))
        editBtn.grid(row=i, column = 6, padx=5, pady=10)
    notebook.add(timeEntries, text='Your Time Enties')

    

k = 0
def getList():
    global k
    return listEntries(k)

def edit(widgets, btn, i, id):
    for widget in widgets:
        widget.configure(state='normal')
    btn.grid_remove()
    confBtn = CTkButton(entriesF, text='Confirm', width=125)
    confBtn.grid(row=i, column = 6, padx=5, pady=10)

    canBtn = CTkButton(entriesF, text='Cancel', width=125, fg_color="#BF3A3A")
    canBtn.grid(row=i, column = 7, padx=5, pady=10)


    confBtn.configure(command=lambda widgets=widgets, confBtn=confBtn, canbtn=canBtn, editbtn=btn,i=i, id=id: confirm(widgets,confBtn,canbtn, editbtn, i,id))
    canBtn.configure(command=lambda widgets=widgets, confBtn=confBtn, canbtn=canBtn, editbtn=btn,i=i: cancel(widgets, confBtn,canbtn, editbtn, i))

def confirm(widgets, confbtn, canbtn, editbtn, i, id):
    global options, timeEntries, optionsAct, issArr, actList
    date = widgets[0].get().split('/')

    isgood = True
    for d in date:
        if d[0] == '0':
            d=d[1:]
        if not d.isdigit():
            widgets[0].configure(text_color="red")
            isgood = False
            break
    
    if isgood:
        if int(date[2]) > datetime.now().year or int(date[2]) < 2000:
            widgets[0].configure(text_color="red")
            isgood = False
        elif (int(date[2]) == datetime.now().year and int(date[1]) > datetime.now().month) or int(date[1]) > 12 or int(date[1]) < 1:
            widgets[0].configure(text_color="red")
            isgood = False
        elif int(date[0]) < 1 or int(date[0]) > calendar.monthrange(int(date[2]), int(date[1]))[1]:
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

        spent_on = f"{date[2]}-{date[1]}-{date[0]}"

        entry = {'issue_id': issue_id, 'activity_id':activity_id, 'hours':widgets[3].get(), 'spent_on':spent_on, 'comments':widgets[4].get() , 'issue':issue, 'activity':activity}
        response = updateEntry(id,entry)
        

        if response == 201:
            postMessage(True, timeEntries,entriesF, entry, True)
            for widget in widgets:
                widget.configure(state='disable')
            
            editbtn.grid(row=i, column = 6, padx=5, pady=10)
            canbtn.grid_remove()
            confbtn.grid_remove()
        else:
            postMessage(False, timeEntries, entriesF, update=True)
        
def cancel(widgets, confbtn, canbtn, editbtn, i):
    for widget in widgets:
        widget.configure(state='disable')
            
    editbtn.grid(row=i, column = 6, padx=5, pady=10)
    canbtn.grid_remove()
    confbtn.grid_remove()
    
    