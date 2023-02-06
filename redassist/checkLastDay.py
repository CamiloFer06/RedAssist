import os
import subprocess
from api import chechYesterday
from datetime import datetime
from time import sleep

dir = os.path.dirname(os.path.abspath(__file__))

day = datetime.now().weekday()
if day == 0:
    msg = "El viernes no cargaste horas"
else: 
    msg = "Ayer no cargaste horas"

if not chechYesterday():
    sleep(30)
    subprocess.run(["notify-send","-i", f"{dir}/icon.png", msg])
    os.system('echo adios >> /home/usuario/Escritorio/hola.txt')
