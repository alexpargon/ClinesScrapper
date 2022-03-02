# ClinesScrapper
Clines scrapper script written on python that is able to create the required files to feed the oscam server work

## Installation in openATV images with python 3.0
The installation requires the following steps
```
 opkg install culr
 opkg install python3-pkgutil
 opkg install python3-xmlrpc
 
 curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 pip install -r requirements.txt

 python cccamScrapper.py log
 ```
 
 ### The log flag
 Serves the purpose of making the script work in verbose mode, usefull for debugging purposes.
