import subprocess
import sys
import platform
import os

def post_install():
    try:
        if sys.version_info[:2][0] < 3:
            print("Please update Python")
            sys.exit(0)
        else:
            if sys.version_info[:2][1] < 8:
                print("Please update Python")
                sys.exit(0)
        print("Python is up to date")
        try:
            subprocess.run("pip install -U pip")
        except Exception as x:
            print("Pip was not found. It will now be reinstalled. ")
            print(x)
            try:
                subprocess.run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
            except Exception as e:
                print("The PIP script could not be downloaded")     
            if "Windows" in platform.platform():
                subprocess.run("python get-pip.py")
            elif "Ubuntu" in platform.platform() or "Linux" in platform.platform():
                subprocess.run("sudo apt-get install python3-pip -y")
        print("Pip has now been installed and can be used")
        try:
            if "client" in os.getcwd():
                subprocess.run("pip install -r "+os.getcwd()+"\\requirements.txt")
            else:
                subprocess.run("pip install -r "+os.getcwd()+"\\client\\requirements.txt")
        except Exception as x:
            print(x)
            sys.exit(0)
        print("All necessary packages have been installed.")
    except Exception as e:
        print(e)
        print("Install")

post_install()