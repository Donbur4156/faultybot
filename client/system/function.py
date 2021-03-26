# Function
import lichess.api 


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
        if check_user(username):
            cheaters.append(username)
    print(cheaters)        