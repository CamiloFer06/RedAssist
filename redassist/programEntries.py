#!/usr/bin/python

from crontab import CronTab
import configparser as cp
import os

dir = os.path.dirname(os.path.abspath(__file__))

config = cp.ConfigParser()
config.read(f"{dir}/.data/.data.cfg")

totCount = config['ProgramedEntries'].getint('totCount')


def createJob(entry, days, hr, min):
    global dir, config, totCount
    totCount += 1
    config['ProgramedEntries']['totCount'] = str(totCount)
    entry['minute'] = min
    entry['hrs'] = hr
    entry['days'] = days
    config['ProgramedEntries'][f'redassist-{totCount}'] = f"{entry}"
    config['ProgramedEntries'][f'redassist-{totCount}_Active'] = '1'
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)

    cron = CronTab(user=True)
    job = cron.new(command=f'XDG_RUNTIME_DIR=/run/user/$(id -u) {dir}/programedentry "{entry}"', comment=f"redassist-{totCount}")
    job.dow.on(*days)
    job.minute.on(min)
    job.hour.on(hr)
    cron.write()
    cron2 = CronTab(user=True)
    exist = False
    for job in cron:
          if job.comment == f"redassist-{totCount}":
               exist = True
               break
    return exist

    
def removeProgEntry(id):
    global dir, config, totCount
    config.read(f"{dir}/.data/.data.cfg")
    for i in range(id, totCount):
        config['ProgramedEntries'][f'redassist-{i}'] = config['ProgramedEntries'][f'redassist-{i+1}']
        config['ProgramedEntries'][f'redassist-{i}_Active'] = config['ProgramedEntries'][f'redassist-{i+1}_Active']
    config.remove_option('ProgramedEntries', f'redassist-{totCount}')
    config.remove_option('ProgramedEntries', f'redassist-{totCount}_Active')
    totCount -= 1
    config['ProgramedEntries']['totCount'] = str(totCount)
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)
    cron = CronTab(user=True)
    cron.remove_all(comment=f"redassist-{id}")
    jobs = [job for job in cron if "redassist" in job.comment]
    for job in jobs:
        comm = job.comment
        i = int(comm.split('-')[1])
        if i >= id:
            job.comment = f"redassist-{i-1}"
    cron.write()
        



def updateProgEntry(id ,entry, min,  hr, days):
    global dir, config
    config.read(f"{dir}/.data/.data.cfg")
    entry['minute'] = min
    entry['hrs'] = hr
    entry['days'] = days
    config['ProgramedEntries'][f'redassist-{id}'] = f"{entry}"
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)
    cron = CronTab(user=True)
    
    jobs = list(cron.find_comment(f"redassist-{id}"))
    job = jobs[0]
    job.minute.on(min)
    job.hour.on(hr)
    job.dow.on(*days)
    job.set_command(f'XDG_RUNTIME_DIR=/run/user/$(id -u) {dir}/programed.py "{entry}"')
    cron.write()

def removeAll():
    cron = CronTab(user=True)
    jobs = [job for job in cron if "redassist" in job.comment]
    for job in jobs:
        cron.remove(job)
    cron.write()

def unableEntry(id):
    global dir, config
    config.read(f"{dir}/.data/.data.cfg")
    config['ProgramedEntries'][f'redassist-{id}_Active'] = '0'
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)

    cron = CronTab(user=True)
    jobs = list(cron.find_comment(f"redassist-{id}"))
    job = jobs[0]
    job.enable(False)
    cron.write()

def enableEntry(id):
    global dir, config
    config.read(f"{dir}/.data/.data.cfg")
    config['ProgramedEntries'][f'redassist-{id}_Active'] = '1'
    with open(f'{dir}/.data/.data.cfg', "w") as cfgfile:
            config.write(cfgfile)

    cron = CronTab(user=True)
    jobs = list(cron.find_comment(f"redassist-{id}"))
    job = jobs[0]
    job.enable(True)
    cron.write()

def progRemind():
    global dir, config
    config.read(f"{dir}/.data/.data.cfg")
    cron = CronTab(user=True)
    job = cron.new(command=f'XDG_RUNTIME_DIR=/run/user/$(id -u) {dir}/reminder', comment='redassist-rermider')
    job.setall('@reboot')
    cron.write()
    cron2 = CronTab(user=True)
    exist = False
    for job in cron2:
          if job.comment == 'redassist-rermider':
               exist = True
               break
    return exist

def remmRemid():
    cron = CronTab(user=True)
    cron.remove_all(comment='redassist-rermider')
    cron.write()
    cron2 = CronTab(user=True)
    exist = False
    for job in cron2:
          if job.comment == 'redassist-rermider':
               exist = True
               break
    return exist


