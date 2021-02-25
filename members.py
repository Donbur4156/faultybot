import requests
import json
import datetime
from os import sys
from configparser import ConfigParser
import re 

id_team = ''
'''
if len(re.findall("s.py$", sys.argv[-1])) == 0:
    id_team = sys.argv[-1]
else: 
    parser = ConfigParser()
    parser.read("parameter.ini")
    configObject = parser["TEAM-CONFIG"]
    id_team = configObject["TeamID"]  


if len(id_team) == 0:
    id_team = input("Team:")
'''
def getfaulty(id_team):
    data = getdata(id_team)
    faultys = splitdata(data)
    return faultys

def getdata(id_team):
    url = "https://lichess.org/api/team/" + id_team + "/users"
    param = dict()
    resp = requests.get(url=url,params=param)
    list_resp = resp.text.splitlines()
    data = list(map(lambda x: json.loads(x), list_resp))
    return data

def splitdata(data):
    fault_users = []
    for i in data:
        is_faulti = i.get("tosViolation")
        if is_faulti:
            user = i.get("username")
            fault_users.append(user)
    print(fault_users)
    if fault_users:
        trennzeichen = "\n"
        userlist = trennzeichen.join(fault_users)
        return userlist
    else:
        userlist = ""
        return userlist

