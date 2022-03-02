from aifc import Error
import re
import os
import sys
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen

original_stdout = sys.stdout  # Save a reference to the original standard output
logging = False
filePath = "/etc/tuxbox/config/oscam-trunk"
fileName = r"oscam.server"
fileNameOLD = r"oscam.server.OLD"

args = str(sys.argv)
if "log" in args:
    logging = True


def log(msgs):
    if logging:
        for msg in msgs:
            print(msg)


def cleanSTR(str):
    return re.sub(r"[\n\t\s]*", "", str)


try:
    url = "https://cccamprime.com/cccam48h.php"
    html = urlopen(url)
    log(["Correctly opened " + url + " url"])

except HTTPError as e:
    log([e, "Error when loading " + url + " url with HTTP"])

except URLError:
    log(["Server down or incorrect domain"])

else:
    res = BeautifulSoup(html.read(), "html5lib")
    data = res.findAll("div", {"class": "border rounded"})[1]

    # Removing OLD file used as Backup
    log(["Removing older file from " + filePath])
    try:
        os.remove(os. path. join(filePath, fileNameOLD))
        log(["Removed"])
    except:
        log(["Old file was not found"])
        pass

    # Reading current file to check changes, and if present, rename to OLD
    log(["Reading and renaming old file..."])
    try:
        currentFile = open(os. path. join(filePath, fileName), "r")
        file = currentFile.readlines()
        OLDUser = file[4].split("=")[1]
        for child in data.children:
            aux = cleanSTR(child.getText())
            if "user=" in aux:
                NEWUser = aux.split("=")[1]

        log(["checking comparison between users: " +
            cleanSTR(OLDUser) + " is OLD and " + cleanSTR(NEWUser) + " is NEW"])
        if cleanSTR(OLDUser) != cleanSTR(NEWUser):
            currentFile.close()
            os.rename(os. path. join(filePath, fileName),
                      os. path. join(filePath, fileNameOLD))
            log(["Renamed", "Writing file again..."])
            # Open the removed file again to be overwritten
            with open(os. path. join(filePath, fileName), 'w') as f:
                # Change the standard output to the file we created.
                sys.stdout = f
                for child in data.children:
                    aux = cleanSTR(child.getText())
                    if aux != "":
                        print(aux)
                sys.stdout = original_stdout  # Reset the standard output to its original value
            # sudo service oscam stop
            # sudo service oscam start
            log(["Success", "Stopping script..."])
        else:
            log(["current lines are updated"])
    except:
        log([fileName + " was not found"])
        pass
