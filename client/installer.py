import subprocess
import sys
import urllib
import os 


# Analyse OS
def os_system():
    if os.system == "nt":
        return "Windows"
    else:
        return "Linux"
    return False

# Test Version
def test_version(pyv):
    if isinstance(pyv[0], int) and isinstance(pyv[1], int) and len(pyv) == 2: 
        if sys.version_info[:2][0] < pyv[0] or pyv[0] == 2:
            print("Please update Python")
            return False
        if sys.version_info[:2][1] < pyv[1]:
            print("Python does not meet the required conditions.")
            return False
        return True    
    else:
        print("Unknown Python Version")
        return False
    return False

# Test Network
def connect():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

# Teste pip
def test_pip():
    # Test
    if connect():
        tdl = False
    else:
        tdl = True
        return False

    # Test if pip is installed
    try:
        subprocess.run("pip install -U pip")
        print("PIP was updated")
        return True
    except:
        # Install pip
        # subprocess.run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        if os_system() == "Windows":
            subprocess.run("python get-pip.py")
        else:
            subprocess.run("python3 get-pip.py")
        subprocess.run("pip install -U pip")
        return True

# Install Skript
def install():
    test_pip()
    try:
        subprocess.run("pip install -U -r requirements.txt")
        return True
    except:
        return False



# Delete Pip
def delete_pip():
    try:
        subprocess.run("pip uninstall pip -y")
        return True
    except:
        return False


# Delete all libarys
def delete_lib():
    subprocess.run("pip freeze > delete_pip_libary.txt")
    try:
        subprocess.run("pip uninstall -r delete_pip_libary.txt -y")
        return True
    except:
        print("Library could not be uninstalled")
        return False
    return False

# install Module
def install_module(modul):
    try:
        subprocess.run("pip install "+modul)
        return True
    except:
        return False
    return False
