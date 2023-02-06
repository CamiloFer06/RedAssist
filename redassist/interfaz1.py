#!/usr/bin/python

import customtkinter as ctk
import configparser
from tkinter import PhotoImage
from api import getDataUser, updateKey
import os
import runpy

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

dir = os.path.dirname(os.path.abspath(__file__))

root = ctk.CTk()
root.title("RedAssist")
root.geometry("600x400")
photo = PhotoImage(file = f"{dir}/icon.png")
root.iconphoto(False, photo)

def login():
    global checkbox, dir
    user = entry1.get()
    pswd = entry2.get()
    response = getDataUser(user, pswd)
    if response.status_code == 401:
        ctk.CTkLabel(master=frame, text="Usuario o contraseña incorrecto", font=("", 12), justify="center", text_color="red").pack(pady=5, padx=5)
    else:
        datos = response.json()
        config = configparser.ConfigParser()
        config.read(f'{dir}/.data/.data.cfg')
        config['User']['login'] = datos['user']['login']
        config['User']['key'] = datos['user']['api_key']
        config['User']['id'] = str(datos['user']['id'])
        config['User']['remember'] = str(checkbox.get())

        with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)
        updateKey()
        root.destroy()
        #runpy.run_path(f"{dir}/interfaz2.py")





# --- Frame
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# --- Label
label = ctk.CTkLabel(master=frame, text="Iniciar sesión", font=("", 28), justify="center")
label.pack(pady=12, padx=10)


# --- Entries
entry1 = ctk.CTkEntry(master=frame, placeholder_text="Usuario") 
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="contraseña", show="*")
entry2.pack(pady=12, padx=10 )

button = ctk.CTkButton(master=frame, text="Iniciar sesión", command=login)
button.pack(pady=12, padx=10)


checkbox = ctk.CTkCheckBox(master=frame, text="Mantener sesión iniciada")
checkbox.pack(pady=12, padx=10)



root.mainloop()
