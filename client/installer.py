import subprocess
import sys
import urllib


if sys.version_info[:2][0] < 3:
    print("Please update Python")
    sys.exit(0)
else:
    if sys.version_info[:2][1] < 8:
        print("Please update Python")
        sys.exit(0)
try:
    urllib.request.urlopen('http://google.com')
except Exception as x:
    print(x)
    sys.exit(0)
try:
    subprocess.run("pip install -U pip")
except Exception as x:
    print(x)
    sys.exit(0)