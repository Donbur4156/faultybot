import subprocess
import sys
import platform
import os

def post_install():
    version_check = True
    try:
        if sys.version_info[:2][0] < 3:
            print("Please update Python")
            version_check = False
        else:
            if sys.version_info[:2][1] < 8:
                print("Please update Python")
                version_check = False
        if version_check == False and "Ubuntu" in platform.platform() or "Linux" in platform.platform():
            subprocess.run("sudo apt-get install python3")
        if version_check == False and "Windows" in platform.platform():
            subprocess.run("curl https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe -o python.exe")
            subprocess.run("python.exe")
        if version_check == False:
            print("Error")
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
                subprocess.run("sudo apt-get install python3-pip")
                subprocess.run("sudo apt install python3-pip")
                subprocess.run("sudo apt-get update")
                subprocess.run("pip install -U pip")
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
    pip_test = True
    try: 
        import discord
    except Exception as e: 
        pip_test = False
        print("PIP Test import discord")
        print("Error: "+str(e))                
    if sys.version_info[:2][0] < 3:
            print("Please update Python")
            pip_test = False
    else:
        if sys.version_info[:2][1] < 8:
            print("Please update Python")
            pip_test = False
    if pip_test == False: 
        print("test failed")
        sys.exit(0)
    if pip_test and version_check:
        print("Test passed.")