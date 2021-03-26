import setup
from wrapper.api import *


user = wrapper.api.user('Gambit-troll')

# Set Flag
flag = False


# IF-ELSE Statement
try:
  flag = user['tosViolation']
except:
  flag = False

# Output
print(flag)