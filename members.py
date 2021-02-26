import requests
import json
import datetime
from os import sys
from configparser import ConfigParser
import re 


def getfaulty(id_team):
    data = getdata(id_team)
    if data:
        faultys = splitdata(data)
    else:
        faultys = 1
    return faultys


def getdata(id_team):
    url = "https://lichess.org/api/team/" + id_team + "/users"
    param = dict()
    resp = requests.get(url=url, params=param)
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
    fault_users.sort()
    if fault_users:
        trennzeichen = "\n"
        userlist = trennzeichen.join(fault_users)
        return userlist
    else:
        userlist = ""
        return userlist

