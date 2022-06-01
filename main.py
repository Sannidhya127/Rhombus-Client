import smtplib
from email.message import EmailMessage
from colored import fg, bg, attr
import os
from email.parser import BytesParser, Parser
from email.policy import default
import imghdr


def sendMail():
    pass




while True:
    command = input(f"{fg('green_1')}rhombus client cli[vAlpha]: {attr('reset')}")

    if command == "q" or command == "exit":
        exit()