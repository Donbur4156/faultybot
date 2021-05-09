import subprocess
import sys
try:
    import urllib
except:
    test_pip()
    import urllib


# Test Network
def connect():
    try:
        urllib.request.urlopen('http://google.com') 
        return True
    except:
        return False

# Install Skript
def install():
    print("Hallo Welt")


def test_pip():
    # Test if pip is installed 
    try: 
        result = subprocess.run("pip install -U pip")
    except:
    # Install pip 
        quit()