import setup
import lichess.api


user = lichess.api.users_by_team('spielplatzrabauken')

# Set Flag
flag = False

# Dummy
users = lichess.api.users_by_team("the-big-greek-subscriber")
for i in users:
    username = i.get('username')
    print(username)

# Output
print(flag)