from client.installer import connect
import sys
from installer import *
from flag import *


# Test Version
try:
   if test_version(py_version) == False:
        print("Test Failed")
        sys.exit(0)
        
    # Test Connection
    if connect() == False:
        print("Connection Error")
        sys.exit(0)

    # install
    if test_pip() == False:
        print("PIP ERROR")
        sys.exit(0)

    # install
    if install() == False:
        print("Dependencie Error")
        sys.exit(0)
except:
    print("ERROR")
    sys.exit(0)