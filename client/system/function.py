# Function
import lichess.api
import requests


# check_user() : bool 
def check_user(username):
    flag = False
    try:
        flag = lichess.api.user(username)['tosViolation']
    except:
        flag = False
    return flag


# check_user_ausgabe : str
def check_user_ausgabe(username):
    if check_user(username):
        return "True"
    else: 
        return "False"


# analyse Team
def analyse_team(teamname):
    cheaters = []
    users = lichess.api.users_by_team(teamname)
    for i in users:
        username = i.get('username')
        is_cheater = i.get('tosViolation')
        if is_cheater:
            cheaters.append(username)
    return cheaters


# kick User
def kick(team, user, token):
    user = user.lower()
    url = 'https://lichess.org/team/'+team+'/kick/'+user
    header = {'Authorization': 'Bearer ' + token}
    r = requests.post(url, headers=header)
    print(r)
    return r


# Kick User  
def runner(team, token):
    for c in analyse_team(team.lower()):
                kick(team.lower(), c, token)
