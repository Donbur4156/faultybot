import sys
from installer import *
from flag import *

# Test Version
def post_db():
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