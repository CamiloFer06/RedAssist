#!/usr/bin/python


from tkinter import *
from customtkinter import *
from tkinter import ttk
import configparser as cp
from newEntry import createNewEntry
from cronometer import createCronometer
from frameSup import createSupFrame
from programFrame import createProgramFrame
from timeEntries import createEntries
from yourProgramed import createYourProgramed
from programEntries import removeAll
import webbrowser
import subprocess
import os

dir = os.path.dirname(os.path.abspath(__file__))
data = cp.ConfigParser()
data.read(f"{dir}/.data/.data.cfg")

usuario = data['User']['login']
key = data["User"]['key']
remember = data["User"].getboolean('remember')




root = Tk()


root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.config(bg="#1a1a1a")
root.title("RedAssist")
photo = PhotoImage(file = f"{dir}/icon.png")
root.iconphoto(False, photo)




# --- Superior Frame

createSupFrame(root,usuario)








# ---------------- style ----------------
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

style = ttk.Style()
settings = {"TNotebook.Tab": {
                "configure": {
                    "padding": [5, 1],
                    "background": "#3D3A3A",
                    "font": ("", 10, 'bold'),
                    "borderwidth": 0
                                           },
                "map": {
                    "background": [("selected", "#1f538d"), ("active", "#242424")],
                    "foreground": [("selected", "#DCE4EE"), ("active", "white")]
                }
            },
            "custom.TNotebook":{
                "configure":{
                    "borderwidth": 0,
                    "background": "#4D4A4A"
                }
            }
           }  

style.theme_create("my_style", parent="alt", settings=settings)
style.theme_use("my_style")


# ---------------- end style ----------------



# --- Notebook
notebook = ttk.Notebook(root)

notebook.config(style='custom.TNotebook')
notebook.pack( fill="both", expand=True)


notebook.add(createNewEntry(notebook), text='Cargar horas')
notebook.add(createCronometer(notebook), text='Cronometro')
notebook.add(createProgramFrame(notebook), text='Program horas')
notebook.add(createYourProgramed(notebook), text='Horas programadas')

#----------------- onClosing ---------------
mainConfigFrame = CTkFrame(root, bg_color="#0a0a0a", corner_radius=0)
configFrame = CTkFrame(mainConfigFrame)
configFrame.pack(fill="x", pady=15, padx=15)

def logOut():
    global dir, data, root
    data['User']['login'] = ''
    data['User']['key'] = ''
    data['User']['id'] = ''
    data['User']['remember'] = '0'
    data['ProgramedEntries'] = {'totcount':0}
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
        data.write(cfgfile)
    removeAll()
    root.destroy()
    subprocess.run([f'{dir}/redassist'])
    

def delCert():
    global data, root, dir
    crt = data['Certificates']['crt']
    keyCert = data['Certificates']['key']
    os.system(f"rm {dir}/.certificates/{crt}")
    os.system(f"rm {dir}/.certificates/{keyCert}")
    data["Certificates"]['crt'] = ''
    data['Certificates']['key'] = ''
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
        data.write(cfgfile)
    logOut()

opredBtn = CTkButton(configFrame, text="Abrir Redmine", command=lambda: webbrowser.open('https://redmine.netlabs.com.uy'))
opredBtn.configure(font=("", 20, "bold"))
opredBtn.grid(row=0, column=0, padx=10, pady=10, sticky='w')


def appletOnOff():
    global appSwitch, data
    data['Applet']['active'] = str(appSwitch.get())
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
        data.write(cfgfile)

appSwitch = CTkSwitch(configFrame, text='Applet Idicator', command=appletOnOff)
applet = data['Applet'].getboolean('active')
if applet:
    appSwitch.select()
else:
    appSwitch.deselect()

appSwitch.configure(font=("", 20, "bold"))
appSwitch.grid(row=1, column=0, padx=10, pady=10, sticky='w')


def remindOnOff():
    global remSwitch, data
    if remSwitch.get():
        
        data['Reminder']['active'] = str(1)
        with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            data.write(cfgfile)
    else:
        data['Reminder']['active'] = str(0)
        with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            data.write(cfgfile)


remSwitch = CTkSwitch(configFrame, text='Recordar al no cargar horas', command=remindOnOff)
remind = data['Reminder'].getboolean('active')
if remind:
    remSwitch.select()
else:
    remSwitch.deselect()

remSwitch.configure(font=("", 20, "bold"))
remSwitch.grid(row=2, column=0, padx=10, pady=10, sticky='w')

delCertBtn = CTkButton(configFrame, text="Borrar certificados", command=delCert)
delCertBtn.configure(font=("", 20, "bold"))
delCertBtn.grid(row=3, column=0, padx=10, pady=10, sticky='w')

logoutBtn = CTkButton(configFrame, text="Cerrar sesión", command=logOut)
logoutBtn.configure(font=("", 20, "bold"))
logoutBtn.grid(row=4, column=0, padx=10, pady=10, sticky='w')

notebook.add(mainConfigFrame, text='Configuración')



def onClosing():
    global remember, data, root, dir, remSwitch
    if not remember:
        data['User']['login'] = ''
        data['User']['key'] = ''
        data['User']['id'] = ''
        data['User']['remember'] = '0'
        data['ProgramedEntries'] = {'totcount':0}
        data['Reminder']['active'] = str(0)
        remSwitch.deselect()
        remSwitch()
        with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            data.write(cfgfile)
        removeAll()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", onClosing)

root.mainloop()
