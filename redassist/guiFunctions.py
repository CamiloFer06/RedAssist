from api import issuesList, activityList
from customtkinter import CTkLabel, CTkButton, CTkFrame
import re


issList = issuesList()
actList = activityList()



issArr = issList['issues']
options = []
for issue in issArr:
    options.append(issue["subject"])

optionsAct = []
for activity in actList:
    optionsAct.append(activity["name"])
        

def filterOptions(event, combobox, opts):
    search_term = combobox.get()
    if search_term == "":
        combobox.configure(values=opts)
    else:
        vals = [option for option in opts if search_term.lower() in option.lower()]
        combobox.configure(values = vals)


def postMessage(succes,frame, before, entry=None, program=False, dates='', totCount=0):
    global options, optionsAct

    msgFrame = CTkFrame(frame)

    okBtn = CTkButton(msgFrame, text='OK', command = msgFrame.destroy)
    okBtn.configure(font=("", 20, "bold"))

    if totCount!=0:
        issue = entry['issue']
        activity = entry['activity']
        hours = entry['hours']
        comment = entry['comments']

        msgFrame.pack( before=before, fill="x", pady=15, padx=15 )

        
        # message
        
        msgL = CTkLabel(msgFrame, text=f"{totCount} días cargados con éxito")
        msgL.configure( font=("", 20, 'bold'), justify="left", text_color="#7adb80" )
        msgL.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=6)

        #date
        dateL = CTkLabel(msgFrame, text=dates)
        dateL.configure( font=("", 20, 'bold'), justify="left" )
        dateL.grid(row=1, column=0, padx=10, pady=10, sticky='w')
       

        # issue / activity
        issueL = CTkLabel(msgFrame, text=f"{issue}; {activity}")
        issueL.configure( font=("", 20, 'bold'), justify="left" )
        issueL.grid(row=2, column=0, padx=10, pady=10, sticky='w', columnspan=6)

        # hours
        cmmL = CTkLabel(msgFrame, text=f"Horas: {hours}")
        cmmL.configure( font=("", 20, 'bold'), justify="left" )
        cmmL.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # comment
        cmmL = CTkLabel(msgFrame, text=f'"{comment}"')
        cmmL.configure( font=("", 20, 'bold'), justify="left" )
        if comment != "":
            cmmL.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        if not succes:
            msgL = CTkLabel(msgFrame, text="Error al cargas los demás días")
            msgL.configure( font=("", 20, 'bold'), justify="left", text_color="#f0685d" )
            msgL.grid(row=5, column=0, padx=10, pady=10, sticky='w', columnspan=6)
            okBtn.grid(row=6, column=0, padx=10, pady=10, sticky='w')
        else:

            okBtn.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        



    elif succes:
        if not program:
            date = entry['spent_on'].split('-')

            year = date[0]
            month = date[1]
            day = date[2]
            dateL = CTkLabel(msgFrame, text=f"{day}/{month}/{year}")
            dateL.configure( font=("", 20, 'bold'), justify="left" )
            dateL.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        issue = entry['issue']
        activity = entry['activity']
        hours = entry['hours']
        comment = entry['comments']

        msgFrame.pack( before=before, fill="x", pady=15, padx=15 )

        
        # message
        if program:
            msgL = CTkLabel(msgFrame, text="Cargar horas porgramado con éxito")
        else:
            msgL = CTkLabel(msgFrame, text="Horas cargadas con éxito")
        msgL.configure( font=("", 20, 'bold'), justify="left", text_color="#7adb80" )
        msgL.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=6)

        #date
        

        

        # issue / activity
        issueL = CTkLabel(msgFrame, text=f"{issue}; {activity}")
        issueL.configure( font=("", 20, 'bold'), justify="left" )
        issueL.grid(row=2, column=0, padx=10, pady=10, sticky='w', columnspan=6)

        # hours
        cmmL = CTkLabel(msgFrame, text=f"Horas: {hours}")
        cmmL.configure( font=("", 20, 'bold'), justify="left" )
        cmmL.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # comment
        cmmL = CTkLabel(msgFrame, text=f'"{comment}"')
        cmmL.configure( font=("", 20, 'bold'), justify="left" )
        if comment != "":
            cmmL.grid(row=4, column=0, padx=10, pady=10, sticky='w')


        okBtn.grid(row=5, column=0, padx=10, pady=10, sticky='w')
    else:

        msgFrame.pack( before=before, fill="x", pady=15, padx=15 )

        
        # message
        if program:
            msgL = CTkLabel(msgFrame, text="Error al programar horas")
        else:
            msgL = CTkLabel(msgFrame, text="Error al cargar horas")
        msgL.configure( font=("", 20, 'bold'), justify="left", text_color="#f0685d" )
        msgL.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=6)
        okBtn.grid(row=1, column=0, padx=10, pady=10, sticky='w')

def is_decimal(string):
    #sglobal hrsText
    if bool(re.match(r'^[0-9][0-9]*\.', string)):
        while not bool(re.match(r'^[0-9]*\.?[0-9]?[0-9]?$', string)):
            string = string[:-1]
        
        #hrsText.set(string)

    if bool(re.match(r'^[0-9][0-9]*\.$', string)):
        string = string[:-1]
        #hrsText.set(string)
    
    return bool(re.match(r'^[0-9][0-9]*\.?[0-9]?[0-9]?', string))

def hrsAdd(entry, text, sum):
    
    if is_decimal(text.get().replace(",", ".")) and (sum or float(text.get().replace(",", "."))>= 0.5):
        if sum:
            newNum = float(text.get().replace(",", ".")) + 0.5
        
        else:
            newNum = float(text.get().replace(",", ".")) - 0.5
        text.set(str(newNum))
        entry.configure(text_color= ['#DCE4EE', '#DCE4EE'])
    else:
        entry.configure(text_color = "red")
if __name__ == '__main__':
    print (issArr[0].keys())