import lichesspy.api
import requests


def analyse_team(teamname: str, ignore_user: list) -> list:
    """
    Analyses all players of a team and returns a list of cheaters.

    Args:
        teamname (str): The name of the team to be analyzed.
        ignore_user (list): List of usernames to be ignored during analysis.

    Returns:
        list: List of usernames identified as cheaters.
    """
    cheaters = []
    # Get the list of users in the specified team
    users = lichesspy.api.users_by_team(teamname)
    for i in users:
        # Check for TOS violations or closed accounts
        if i.get("tosViolation") or i.get("closed"):
            username = i.get("username")
            # Add the cheater to the list if not in the ignore list
            if username not in ignore_user:
                cheaters.append(username)
    return cheaters


def kick(team: str, user: str, token: str) -> requests.Response:
    """
    Kicks a specified player from the team using the provided bot token.

    Args:
        team (str): The name or ID of the team.
        user (str): The username of the player to be kicked.
        token (str): The bot token with necessary permissions.

    Returns:
        requests.Response: The response from the Lichess API after the kick attempt.
    """
    user = user.lower()
    # Construct the URL for kicking the user from the team
    url = f"https://lichess.org/team/{team}/kick/{user}"
    header = {"Authorization": f"Bearer {token}"}
    # Send a POST request to the Lichess API to kick the user
    return requests.post(url, headers=header)


def check(level: requests.Response) -> bool:
    """
    Checks if the response indicates success.

    Args:
        level (requests.Response): The response object from a Lichess API request.

    Returns:
        bool: True if the response indicates success, False otherwise.
    """
    # Check if the string "true" is present in the response text
    return bool("true" in level.text)


def status(level: requests.Response) -> str:
    """
    Retrieves the status message from the response.

    Args:
        level (requests.Response): The response object from a Lichess API request.

    Returns:
        str: The status message.
    """
    if "true" not in level.text:
        # Determine the specific error based on the response text
        if "No such token" in level.text:
            return "Invalid Token! (Wrong Token or not authorized)"
        if "Not your team" in level.text:
            return "Invalid Token! (Not your Team)"
        return "Undefined Error!"
    return "No Error"


def check_team_name(team: str) -> bool:
    """
    Checks if the team name is valid and returns the corrected name.

    Args:
        team (str): The name or ID of the team.

    Returns:
        str: The corrected team name.
    """
    if "/team/" in team:
        runner = len(team)
        while runner > 0:
            # Remove any "/" characters from the team name
            if "/" in team[-runner::]:
                runner -= 1
            else:
                return team[-runner::]
    return team
