from tkinter import Frame, Label

def createSupFrame(root, usuario):
    supFrame = Frame(root, bg="#29333a")
    supFrame.pack(fill="x")

    #account
    accLabel = Label (supFrame, text=usuario, bg="#29333a", fg="white", font=("", 14, "bold"))
    accLabel.pack(side="right", pady=5, padx=5)

    #Join the future
    joinLabel = Label(supFrame, text="JOIN THE FUTURE", bg="#29333a", fg="white", font=("Trebuchet MS", 16, "bold"))
    joinLabel.pack(side="left", pady=5, padx=5)