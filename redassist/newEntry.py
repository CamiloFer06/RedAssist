from customtkinter import *
from functools import partial
from guiFunctions import issList, actList,options, optionsAct,issArr, filterOptions, postMessage, is_decimal, hrsAdd

from datetime import datetime, timedelta
import calendar
from api import timeEntryPost

newTimeEntries = None
newEntFrame = None
combo = None
comboAct = None
hrsText = None
comboYear = None
comboMonths = None
comboDays = None
commEntry = None
comboDays2 = None
comboYear2 = None
comboMonths2 = None
fromLabel = None
toLabel = None
switch = None


def createNewEntry(master):
    global actList, issList, optionsAct, options, newTimeEntries, combo, comboAct, hrsText, comboYear, comboMonths, comboDays, commEntry, issArr, newEntFrame, comboDays2, comboYear2, comboMonths2, fromLabel, toLabel, switch
    newTimeEntries = CTkFrame(master=master, bg_color="#0a0a0a", corner_radius=0)

    # --- new entry ---

    # -- Frame --
    newEntFrame = CTkFrame(newTimeEntries)
    newEntFrame.pack(fill="x", pady=15, padx=15)

    # -- Issue --

    # label
    issueLab = CTkLabel(newEntFrame, text="Issue: ")
    issueLab.configure(font=("", 26, "bold"))
    issueLab.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # combo box
    

    combo = CTkComboBox(newEntFrame, values=options)
    combo.configure(width=500, font=("", 18))
    combo.grid(row=0, column=1, padx=10, pady=10, sticky='w', columnspan=10)
    combo.set('')
    combo.bind("<Key>", partial(filterOptions, combobox=combo, opts=options))


    # -- Activity --

    # label

    actLab = CTkLabel(newEntFrame, text="Activity: ")
    actLab.configure( font=("", 26, "bold"))
    actLab.grid(row=1, column=0, padx=10, pady=10, sticky='w', columnspan=2)

    # combo box

    comboAct = CTkComboBox(newEntFrame, values=optionsAct)
    comboAct.configure(width=250, font=("", 18))
    comboAct.grid(row=1, column=1, padx=10, pady=10, sticky='w', columnspan=8)
    comboAct.bind("<Key>", partial(filterOptions, combobox=comboAct, opts=optionsAct))
    comboAct.set('')


    # -- Hours --

    # label

    hrsLab = CTkLabel(newEntFrame, text="Horas: ")
    hrsLab.configure(font=("", 26, "bold")) 
    hrsLab.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # entry

    hrsText = StringVar()

    hrsEntry = CTkEntry(newEntFrame, textvariable=hrsText)
    hrsEntry.configure(width=125, font=("", 18)) 
    hrsText.set("0.0")
    hrsEntry.grid(row=2, column=2, padx=10, pady=10, sticky='w')#, columnspan=2)

    # buttons
    


    subBut = CTkButton(newEntFrame, text="-", command= lambda: hrsAdd(hrsEntry, hrsText, False))
    subBut.configure(width=30, font=("", 16, "bold"))
    subBut.grid(row=2, column=1, pady=10, sticky='w')

    addBtn = CTkButton(newEntFrame, text="+", command= lambda: hrsAdd(hrsEntry, hrsText, True))
    addBtn.configure(width=30, font=("", 16, "bold"))
    addBtn.grid(row=2, column=4, pady=10, sticky='w')


    # -- Date --

    
    # label

    hrsLab = CTkLabel(newEntFrame, text="Fecha: ")
    hrsLab.configure( font=("", 26, 'bold'), justify="left")
    hrsLab.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    fromLabel = CTkLabel(newEntFrame, text="Desde: ")
    fromLabel.configure( font=("", 16))

    toLabel = CTkLabel(newEntFrame, text="Hasta: ")
    toLabel.configure( font=("", 16))

    # coomboBoxes
    date = datetime.now()

    years = [str(year) for year in range(2000, date.year+1)]
    months = list(calendar.month_name)
    months.pop(0)
    days = [str(day) for day in range(calendar.monthrange(date.year, date.month)[1]+1)]
    days2 = [str(day) for day in range(calendar.monthrange(date.year, date.month)[1]+1)]

    # ****** list days ******
    def listDays(comboYear, comboMonths, comboDays, days):
        year = int(comboYear.get())
        month = months.index(comboMonths.get()) + 1
        days = [str(day) for day in range(calendar.monthrange(year, month)[1]+1)]
        comboDays.configure(values=days)
    # ***********************


    comboYear = CTkComboBox(newEntFrame, values=years, state='readonly', command=lambda e: listDays(comboYear, comboMonths, comboDays, days))
    comboYear.configure(width=80, font=("", 16))
    comboYear.set(date.year)
    comboYear.grid(row=3, column=4, padx=10, pady=10, sticky='w')#, columnspan=2)

    comboMonths = CTkComboBox(newEntFrame, values=months, state='readonly', command=lambda e: listDays(comboYear, comboMonths, comboDays, days))
    comboMonths.configure(width=150, font=("", 16))
    comboMonths.set(months[date.month-1])
    comboMonths.grid(row=3, column=5, padx=10, pady=10, sticky='w')

    comboDays = CTkComboBox(newEntFrame, values=days, state='readonly')
    comboDays.configure(width=80, font=("", 16))
    comboDays.set(date.day)
    comboDays.grid(row=3, column=6, padx=10, pady=10, sticky='w')

# ------------
    comboYear2 = CTkComboBox(newEntFrame, values=years, state='readonly', command=lambda e: listDays(comboYear2, comboMonths2, comboDays2, days2))
    comboYear2.configure(width=80, font=("", 16))
    comboYear2.set(date.year)
    #comboYear2.grid(row=3, column=2, padx=10, pady=10, sticky='w')#, columnspan=2)

    comboMonths2 = CTkComboBox(newEntFrame, values=months, state='readonly', command=lambda e: listDays(comboYear2, comboMonths2, comboDays2, days2))
    comboMonths2.configure(width=150, font=("", 16))
    comboMonths2.set(months[date.month-1])
    #comboMonths2.grid(row=3, column=3, padx=10, pady=10, sticky='w')

    comboDays2 = CTkComboBox(newEntFrame, values=days2, state='readonly')
    comboDays2.configure(width=80, font=("", 16))
    comboDays2.set(date.day + 1)
    #comboDays2.grid(row=3, column=4, padx=10, pady=10, sticky='w')

# ------------

# switch

    def switchOnOff(value):
        #global comboDays, comboMonths, comboYear, comboDays2, comboYear2, comboMonths2, fromLabel, toLabel
        if value:
            for widget in comboDays, comboMonths, comboYear:
                column = widget.grid_info()['column']
                widget.grid(column=column+1)
                

            fromLabel.grid(row=3, column=4, padx=10, pady=10, sticky='w')
            toLabel.grid(row=3, column=8, padx=10, pady=10, sticky='w')
            i = 9
            for widget in comboYear2, comboMonths2, comboDays2:
                widget.grid(row=3, column=i, padx=10, pady=10, sticky='w')
                i += 1
        else:
            fromLabel.grid_remove()
            for widget in comboDays, comboMonths, comboYear:
                column = widget.grid_info()['column']
                widget.grid(column=column-1)
            toLabel.grid_remove()
            for widget in comboDays2, comboYear2, comboMonths2:
                widget.grid_remove()

    
    switch = CTkSwitch(newEntFrame, text='varios días')
    switch.configure( font=("", 16), command= lambda: switchOnOff(switch.get()))
    switch.grid(row=3, column=1, padx=10, pady=10, sticky='w', columnspan=3)

    








    # -- Comment --

    # label

    commLab = CTkLabel(newEntFrame, text="Comentrario: ")
    commLab.configure(font=("", 26, "bold"), justify="left")
    commLab.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # entry
    commEntry = CTkEntry(newEntFrame)
    commEntry.configure(width=800, font=("", 18))
    commEntry.grid(row=4, column=1, padx=10, pady=10, sticky='w', columnspan=15)


    # --- Post entry ---

    postBtn = CTkButton(newEntFrame, text="Cargar", command=createPost)
    postBtn.configure(font=("", 20, "bold"))
    postBtn.grid(row=5, column=0, padx=10, pady=10, sticky='w')

    return newTimeEntries


    # --- Message ---

    # frame

def okDates():
    global comboYear, comboMonths, comboDays, comboYear2, comboMonths2, comboDays2

    year1 = int(comboYear.get())
    month1 = comboMonths.cget('values').index(comboMonths.get())+1
    day1 = int(comboDays.get())
    date1 = datetime(year1, month1, day1).date()

    year2 = int(comboYear2.get())
    month2 = comboMonths2.cget('values').index(comboMonths2.get())+1
    day2 = int(comboDays2.get())
    date2 = datetime(year2, month2, day2).date()
    print(date2 > date1)
    return date2 > date1


def createPost():
    global options,optionsAct ,combo, comboAct, hrsText, comboYear, comboMonths, comboDays, commEntry, issArr, actList, newEntFrame, switch

    if ( is_decimal(hrsText.get()) ) and ( combo.get() in options ) and ( comboAct.get() in optionsAct ) and ( float(hrsText.get()) > 0):

        issOpId = options.index(combo.get())
        actOpId = optionsAct.index(comboAct.get())

        issue = issArr[issOpId]['subject']
        issue_id = issArr[issOpId]['id']

        activity = actList[actOpId]['name']
        activity_id = actList[actOpId]['id']
        comment = commEntry.get()

        hours = hrsText.get()
        entry = {'issue_id': issue_id, 'activity_id':activity_id, 'hours':hours, 'comments':comment, 'issue':issue, 'activity':activity}
        if not switch.get():
            year = int(comboYear.get())
            month = comboMonths.cget('values').index(comboMonths.get())+1
            day = int(comboDays.get())
            
            date = str(datetime(year, month, day).date())

            

            entry['spent_on'] = date
            
            response = timeEntryPost(entry)
            

            succes =  response == 201
            postMessage(succes, frame=newTimeEntries, before=newEntFrame, entry=entry)
            
        elif okDates():
            year1 = int(comboYear.get())
            month1 = comboMonths.cget('values').index(comboMonths.get())+1
            day1 = int(comboDays.get())
            date1 = datetime(year1, month1, day1).date()

            year2 = int(comboYear2.get())
            month2 = comboMonths2.cget('values').index(comboMonths2.get())+1
            day2 = int(comboDays2.get())
            date2 = datetime(year2, month2, day2).date()

            succes = True
            k = 0
            lastDate = date2
            for i in range(int((date2 - date1).days) + 1):
                date = date1 + timedelta(i)

                entry['spent_on'] = date
                response = timeEntryPost(entry)
                if response != 201:
                    succes = False
                    lastDate = date
                    break
                else:
                    k += 1
            dates = f"From: {date1.day}/{date1.month}/{date1.year} -- To: {lastDate.day}/{lastDate.month}/{lastDate.year}"
            postMessage(succes, newTimeEntries, before=newEntFrame, entry=entry, dates=dates, totCount=k)
