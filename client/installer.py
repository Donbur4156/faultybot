import subprocess
import sys
import urllib


def test_version(kernel, version):
    if sys.version_info[:2][0] < kernel or kernel == 2:
        print("Please update Python")
        sys.exit(0)
    if sys.version_info[:2][1] < version:
        print("Python does not meet the required conditions.")
        sys.exit(0)

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
        result = subprocess.run("pip install -U pip")
        print("PIP was updated")
        return True
    except:
        # Install pip
        # subprocess.run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        subprocess.run("python get-pip.py")
        return True

# Install Skript
def install():
    test_pip()
    try:
        subprocess.run("pip install -U -r requirements.txt")
        return True
    except:
        return False

 # Delete PIP


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
