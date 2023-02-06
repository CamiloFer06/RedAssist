import configparser
import runpy
import os

dir = os.path.dirname(os.path.abspath(__file__))




def loggedIn():
    global dir
    config = configparser.ConfigParser()
    config.read(f"{dir}/.data/.data.cfg")

    cert = (config['Certificates']['crt'] != '' and config['Certificates']['key'] != '')
    remember = config["User"].getboolean('remember')
    if not cert:
        runpy.run_path(f"{dir}/selectCertificates.py")
        config.read(f"{dir}/.data/.data.cfg")
        cert = (config['Certificates']['crt'] != '' and config['Certificates']['key'] != '')
    if cert:
        if remember:
            return True
        else:
            runpy.run_path(f"{dir}/interfaz1.py")
            config.read(f"{dir}/.data/.data.cfg")
            if config['User']['key'] != '':
                return True
            else: return False
    else: 
        return False
    
        