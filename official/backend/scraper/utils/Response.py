import platform
import json 
from pathlib import Path
import shutil
import sqlite3
import time
import os

class Response:
    os = None
    cookie = None
    expiry = None
    conf_file = None
    conf_path = Path(__file__).parent / 'files' / 'configuration.json'

    def __init__(self):
        with open(self.conf_path, "r") as file:
            self.conf_file = json.load(file)
            
        try:
            self.os  = self.conf_file["os"]
            self.cookie = self.conf_file["cookie"]
            self.expiry = self.conf_file["expiry"]

            now = time.time()
            if now > self.expiry:
                self.set_cookies()

        except KeyError:
            self.set_os()
            self.set_cookies()    


    def set_os(self):
        # find os
        self.os = platform.system()

        # update os in file 
        with open(self.conf_path, "r") as file:
            conf_file = json.load(file)

        conf_file["os"] = self.os

        with open(self.conf_path, "w") as file:
            json.dump(conf_file, file)



    def set_cookies(self):
        # find cookie
        if self.os == "Linux":
            source = f"/home/{os.getenv('USER')}/snap/firefox/common/.mozilla/firefox/9v6m6flb.default/cookies.sqlite"
            
        elif self.os == "Windows":
            source = "C:\Users\%USERNAME%\AppData\Roaming\Mozilla\Firefox\Profiles\4snz9eyi.default-release\cookies.sqlite" 
        
        destination = Path(__file__).parent / 'files' / 'configuration.json'
        shutil.copy(source, destination)


        # Read li_at
        con =   sqlite3.connect(destination)
        moz_cookie = con.execute("select expiry, value from moz_cookies where name = 'li_at';")
        moz_cookie = moz_cookie.fetchone()
        self.expiry = moz_cookie[0] 
        self.cookie = moz_cookie[1]

        # update cookie in file 
        with open(self.conf_path, "r") as file:
            conf_file = json.load(file)

        conf_file["expiry"] = self.expiry
        conf_file["cookie"] = self.cookie

        with open(self.conf_path, "w") as file:
            json.dump(conf_file, file)

    def get_os(self):
        if self.os == None:
            self.set_os()
        return self.os

    def get_cookies(self):
        if self.cookie == None:
            self.set_cookie()
        return self.cookie
