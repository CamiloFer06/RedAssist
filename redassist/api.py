from requests import *
from datetime import datetime, timedelta
import configparser
import os

dir = os.path.dirname(os.path.abspath(__file__))

host = "https://redmine.netlabs.com.uy"

config = configparser.ConfigParser()
config.read(f"{dir}/.data/.data.cfg")
key = config["User"]['key']
userId = config["User"]['id']

crt = config['Certificates']['crt']
keyFile = config['Certificates']['key']

cert = (f"{dir}/.certificates/{crt}", f"{dir}/.certificates/{keyFile}")
verify = (f"{dir}/.certificates/nlca.netlabs.com.uy.crt")

def getDataUser(user, pswd):
    global host, cert, verify, key, userId, config
    response = get(host+"/my/account.json", cert=cert, verify=verify, auth=(user, pswd)) 
    return response

def updateKey():
    global key, userId
    config.read(f"{dir}/.data/.data.cfg")
    key = config["User"]['key']
    userId = config["User"]['id']

def issuesList():
    global host, cert, verify, key
    url = f"{host}/issues.json?key={key}"
    r = get(url, cert=cert, verify=verify)


    issuesJson = r.json()
    totCount = issuesJson['total_count']

    url = f"{url}&limit={totCount}"
    r = get(url, cert=cert, verify=verify)
    issuesJson = r.json()

    return issuesJson


def activityList():
    global host, cert, verify, key
    url = f"{host}/projects/26.json?include=time_entry_activities&key={key}"

    r = get(url, cert=cert, verify=verify)

    return r.json()['project']['time_entry_activities']


def timeEntryPost(entry):
    global host, cert, verify, key
    url = f"{host}/time_entries.xml?key={key}"

    issue_id = entry['issue_id']
    hours = entry['hours']
    comments = entry['comments']
    activity_id = entry['activity_id']
    spent_on = entry['spent_on']

    headers = {'Content-Type': 'application/xml'}
    data = f"""
<?xml version="1.0" encoding="UTF-8"?>  
<time_entry>
    <issue_id>{issue_id}</issue_id>
    <hours>{hours}</hours>
    <comments>{comments}</comments> 
    <activity_id>{activity_id}</activity_id>  
    <spent_on>{spent_on}</spent_on> 
</time_entry>"""
    timePost = post(url, cert=cert, verify=verify, data=data, headers=headers)
    
    
    return timePost.status_code


def listEntries(offset):
    global key, userId, cert, verify, host

    url = f"{host}/time_entries.json?key={key}&user_id={userId}&limit=25&offset={offset}"
    r = get(url, cert=cert, verify=verify)

    return r.json()['time_entries']


def updateEntry(id, entry):
    global host, cert, verify, key
    url = f"{host}/time_entries/{id}.xml?key={key}"

    issue_id = entry['issue_id']
    hours = entry['hours']
    comments = entry['comments']
    activity_id = entry['activity_id']
    spent_on = entry['spent_on']

    headers = {'Content-Type': 'application/xml'}
    data = f"""
<?xml version="1.0" encoding="UTF-8"?>  
<time_entry>
    <issue_id>{issue_id}</issue_id>
    <hours>{hours}</hours>
    <comments>{comments}</comments> 
    <activity_id>{activity_id}</activity_id>  
    <spent_on>{spent_on}</spent_on> 
</time_entry>"""
    timePost = post(url, cert=cert, verify=verify, data=data, headers=headers)
    print(url)
    print (timePost.content)
    return timePost.status_code

def chechYesterday():
    global host, cert, verify, key, userId
    today = datetime.now().date()

    if today.weekday() > 4:
        return True
    elif today.weekday() == 0:
        lastDay = today - timedelta(days=3)
    else:
        lastDay = today - timedelta(days=1)

    url = f"{host}/time_entries.json?key={key}&user_id={userId}&spent_on={lastDay}"

    r = get(url, cert=cert, verify=verify)
    j = r.json()
    return j['total_count'] != 0

if __name__ == '__main__':
    print (chechYesterday())