import subprocess
import sys
import os
try:
    import httplib
except:
    import http.client as httplib


def post_install():
    if sys.version_info[:2][0] < 3:
        print("Please update Python")
        sys.exit(0)
    else:
        if sys.version_info[:2][1] < 8:
            print("Please update Python")
            sys.exit(0)
    print("Python is up to date")
    try:
        conn = httplib.HTTPConnection("https://www.google.com", timeout=3)
        conn.request("HEAD", "/")
        conn.close()
    except Exception as x:   
        print(x)
        sys.exit(0)
    print("You are online")
    try:
        subprocess.run("pip install -U pip")
    except Exception as x:
        print("Pip was not found. It will now be reinstalled. ")
        print(x)
        subprocess.run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        if os.system == "nt":
            subprocess.run("python get-pip.py")
        else:
            subprocess.run("python3 get-pip.py")
    print("Pip has now been installed and can be used")
    try:
        subprocess.run("pip install -r requirements.txt")
    except Exception as x:
        print(x)
        sys.exit(0)
    print("All necessary packages have been installed.")

post_install()