# Imports
import lichesspy.api as api
import requests
import time


# Checks if a player has violated the rules of Lichess.
def check_user(username):
    flag = False
    try:
        # The system marks such players with a TOS mark. This can be obtained as an array from the API.
        flag = api.user(username)['tosViolation']
    except:
        # Since it is either there or not, the try catch block is misused as an if statement
        flag = False
    return flag


# Checks the user and outputs whether he has cheated.
# Since python has a problem with boolean values, this function outputs them as strings.
def check_user_ausgabe(username):
    if check_user(username):
        return "True"
    else:
        return "False"


# The function checks all players of a team and returns a list of all cheaters.
def analyse_team(teamname):
    cheaters = []
    # The wrapper classes are used, because the PyPi functions have a wrong scope.
    # Please note the commit time.
    users = api.users_by_team(teamname)
    for i in users:
        username = i.get('username')
        is_cheater = i.get('tosViolation')
        if is_cheater:
            cheaters.append(username)
    return cheaters


# The function kicks the specified player from the team.
# The bot token is required for this.
def kick(team, user, token):
    user = user.lower()
    # The token is the one from the bot account.
    # The bot must also be a team leader to be able to kick people.
    url = 'https://lichess.org/team/'+team+'/kick/'+user
    header = {'Authorization': 'Bearer ' + token}
    # The Lichess API accepts the request as a POST request.
    # Therefore all data must be in the header.
    request = requests.post(url, headers=header)
    return request


# The function kicks all cheaters from the desired team.
def runner(team, token):
    # This is actually the complete backend for the kickfaulty
    for c in analyse_team(team.lower()):
        kick(team.lower(), c, token)


# Unfortunately, the API returns only an array.
# This is checked here.
def check(level):
    # Since it is a request response, it cannot be interpreted as a string.
    if "true" in level.text:
        return True
    else:
        return False


# The function investigates why a request failed.
def status(level):
    if "true" not in level.text:
        # The Lichess API actually works very well.
        # Therefore either the token is wrong or the error is about one meter behind the screen.
        if "No such token" in level.text:
            return "Invalid Token! (Wrong Token or not authorized)"
        return "Unkown Error!"
    return "No Error"


# This function kicks all people out of the team. No matter if they cheat or not.
# This function is usually only used for YouTube teams.
def clear_team(team, token):
    try:
        # The bot just goes through them all. With normal teams, lichess does not block the IP address either.
        for i in api.users_by_team(team):
            username = i.get('username').lower()
            url = 'https://lichess.org/team/' + team + '/kick/' + username
            header = {'Authorization': 'Bearer ' + token}
            r = requests.post(url, headers=header)
            # So that lichess doesn't think we're about to launch a DDOS attack,
            # we give them some time to catch their breath.
            time.sleep(1)
    except:
        return False
    return True


# If anyone operates the bot incorrectly, it will be checked again for errors here.
def check_team_name(team):
    # The program uses the static links from lichess
    if "/team/" in team:
        x = len(team)
        while x > 0:
            # Lichess cannot process teams with the "/" character for syntax reasons.
            # Therefore there are no such teams.
            if "/" in team[-x::]:
                x = x - 1
            else:
                return team[-x::]
    else:
        return team
    # The false can never be reached. It stands so that it looks better
    return False
