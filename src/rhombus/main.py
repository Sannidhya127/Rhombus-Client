from ast import arg
from email.mime import application
import smtplib
from email.message import EmailMessage
from wsgiref.util import application_uri
from colored import fg, bg, attr
import os
from email.parser import BytesParser, Parser
from datetime import *
from email.policy import default
import tkinter
import threading
import queue
import imghdr
import json
import sys, traceback, types
import getpass
import win32ui
import multiprocessing
import win32con
import ctypes
import enum
import win32api
from alive_progress import alive_bar
import win32con
import win32event
import re
import win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'




def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()

            # log_warn("debug.log", "isUserAdmin", "User already admin")
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")

            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getpid() == 0
    else:
        raise RuntimeError(
            "Unsupported operating system for this module: %s" % (os.name,))


def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType, types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        # print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc


def test():
    rc = 0
    if not isUserAdmin():
        print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        #rc = runAsAdmin(["c:\\Windows\\notepad.exe"])
        rc = runAsAdmin()
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    x = input('Press Enter to exit.')
    return rc


class SW(enum.IntEnum):

    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):

    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def main():
    print(" ")


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))

        


def CheckLogin():
    #taking the username
    uName = getpass.getuser()

    #defining the file path and name
    pathPy = "C:/Users/"+uName+"/rhombus.json"
    path = os.path.exists(pathPy)
    if path == True:
        pass
    else:
        # file = open(pathPy, 'w')
        print("You are not logged in, please log in to continue")
        username = input("Username: ")
        global email
        email = input('Email: ')
        application_password = input("Application Password (should be linked with the Email entered): ")
        if(re.fullmatch(regex, email)):
            jsonData = {
                'username' : username,
                'email' : email,
                'app_pass' : application_password
            }
            json_object = json.dumps(jsonData, indent = 4)
            with open(pathPy, "w") as outfile:
                outfile.write(json_object)
            print(f"User Logged in successfully {username}[USERNAME] {email}[EMAIL]")
        else:
            print("Not an email")
            CheckLogin()


def loading():
    while True:
        print(".", end="")

def checkEntry():
    uName = getpass.getuser()

    #defining the file path and name
    pathPy = "C:/Users/"+uName+"/rhombus.json"

    path = os.path.exists(pathPy)
    if path == True:
        with open(pathPy) as f:
            data = json.load(f)
            global email_adress
            email_adress = data['email']
            global application_password
            application_password = data['app_pass']
    else:
        pass


def sendMail(mail_data):
    checkEntry()
    credentials = mail_data.split(" ")
    recipent = credentials[1]
    if len(recipent) == 0:
        print("No email given. Use 'mail <recipent_mail_id>'")
    else:
        subject = input("Subject: ")
        body = input("body: ")
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_adress
        msg['To'] = recipent
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_adress, application_password)
            smtp.send_message(msg)  
            
if __name__ == '__main__':
    bootstrap()

    CheckLogin()
    while True:
        
        command = input(f"{fg('green_1')}rhombus client cli[vAlpha]: {attr('reset')}")
        if command == "q" or command == "exit":
            exit()
        if command[0:4] == "mail":
            sendMail(command)