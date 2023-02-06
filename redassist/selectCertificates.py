from customtkinter import *
from tkinter import *
import configparser as cp
import os

dir = os.path.dirname(os.path.abspath(__file__))



set_appearance_mode("dark")
set_default_color_theme("dark-blue")

root = CTk()
root.title("RedAsist")
photo = PhotoImage(file = f"{dir}/icon.png")
root.iconphoto(False, photo)

frame = CTkFrame(root)

# --- Frame
frame = CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# --- Label
label = CTkLabel(master=frame, text="Select Certificates", font=("", 28, 'bold'), justify="center")
label.grid(row=0, column=0, pady=12, padx=10, columnspan=2, sticky='wesn')


def search(txt):
    file_path = filedialog.askopenfilename()
    
    txt.set(file_path)

def check_file(file_path, extension):
    if os.path.isfile(file_path) and file_path.endswith(extension):
        return True
    else:
        return False


label1 = CTkLabel(frame, text="crt certificate:")

label1.configure( font=("", 24), justify="left" )
label1.grid(row=1, column=0, padx=10, pady=10, sticky='w')


text1 = StringVar()
entry1 = CTkEntry(master=frame, textvariable=text1) 
entry1.configure(font=("", 18), width=700)
entry1.grid(row=2, column=0, pady=12, padx=10)

btn1 = CTkButton(frame, text='Search', command=lambda: search(text1))
btn1.configure(font=("", 20, "bold"))
btn1.grid(row=2, column=1, pady=12, padx=10)



label2 = CTkLabel(frame, text="key:")

label2.configure( font=("", 24), justify="left" )
label2.grid(row=3, column=0, padx=10, pady=10, sticky='w')

text2 = StringVar()
entry2 = CTkEntry(master=frame, textvariable=text2)
entry2.configure(font=("", 18), width=700)
entry2.grid(row=4, column=0, pady=12, padx=10)

btn2 = CTkButton(frame, text='Search', command=lambda: search(text2))
btn2.configure(font=("", 20, "bold"))
btn2.grid(row=4, column=1, pady=12, padx=10)


def confirm():
    global text1, text2, dir, root

    config = cp.ConfigParser()
    config.read(f"{dir}/.data/.data.cfg")

    if check_file(text1.get(), ".crt") and check_file(text2.get(), '.key'):
        os.system(f'cp {text1.get()} {dir}/.certificates/')
        os.system(f'cp {text2.get()} {dir}/.certificates/')
        crt = os.path.basename(text1.get())
        key = os.path.basename(text2.get())

        config['Certificates']['crt'] = crt
        config['Certificates']['key'] = key

        with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)
        config.read(f'{dir}/.data/.data.cfg')
        cert = (config['Certificates']['crt'] != '' and config['Certificates']['key'] != '')
        if cert:
            root.destroy()

btn3 = CTkButton(frame, text='Confirm', command=confirm)
btn3.configure(font=("", 20, "bold"))
btn3.grid(row=5, column=0, pady=12, padx=10, columnspan=2, sticky='wesn')


root.mainloop()