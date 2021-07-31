# Imports
import lichesspy.api
import requests


# Checks if a player has violated the rules of Lichess.
def check_user(username):
    """ Check User """
    flag = False
    try:
        # The system marks such players with a TOS mark.
        # This can be obtained as an array from the API.
        flag = lichesspy.api.user(username)['tosViolation']
    except lichesspy.api.ApiError():
        # Since it is either there or not, the try catch block is misused as an if statement
        flag = False
    else:
        flag = False
    return flag


# Checks the user and outputs whether he has cheated.
# Since python has a problem with boolean values, this function outputs them as strings.
def check_user_ausgabe(username):
    """ Check User Ausgabe """
    if check_user(username):
        return True
    return False


# The function checks all players of a team and returns a list of all cheaters.
def analyse_team(teamname):
    cheaters = []
    # The wrapper classes are used, because the PyPi functions have a wrong scope.
    # Please note the commit time.
    users = lichesspy.api.users_by_team(teamname)
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


# Unfortunately, the API returns only an array.
# This is checked here.
def check(level):
    """ check """
    # Since it is a request response, it cannot be interpreted as a string.
    return bool("true" in level.text)


# The function investigates why a request failed.
def status(level):
    """ get status """
    if "true" not in level.text:
        # The Lichess API actually works very well.
        # Therefore either the token is wrong or the error is about one meter behind the screen.
        if "No such token" in level.text:
            return "Invalid Token! (Wrong Token or not authorized)"
        return "Undefined Error!"
    return "No Error"


# If anyone operates the bot incorrectly, it will be checked again for errors here.
def check_team_name(team):
    # The program uses the static links from lichess
    if "/team/" in team:
        runner = len(team)
        while runner > 0:
            # Lichess cannot process teams with the "/" character for syntax reasons.
            # Therefore there are no such teams.
            if "/" in team[-runner::]:
                runner -= 1
            else:
                return team[-runner::]
    return team
