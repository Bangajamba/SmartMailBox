import speech_recognition as sr
import smtplib
from email.mime.text import MIMEText
import time
import RPi.GPIO as GPIO

# Mail

# This should not be so obvious in future
mailAcc = "MAIL"
mailPass = "PASSWORD" 
mailReceiver = "Receiver"
mail = smtplib.SMTP('smtp.gmail.com:587')
mail.ehlo()
mail.starttls()
mail.login(mailAcc, mailPass)

# Voice
r = sr.Recognizer()

# GPIO
pirPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirPin, GPIO.IN)
## GPIO.setup("ledpin", GPIO.OUT)


def sendMail(content):

    message = "Subject: Incomming Message \n" + content
    message  = MIMEText(message, _charset="UTF-8")
    try:
        mail.sendmail(mailAcc, mailReceiver, message.as_string())
    except Exception as e:
        print(e)


def listen():
    result = ""
    with sr.Microphone() as source:
        print('Say Something!')
        audio = r.listen(source)
    try:
        result = r.recognize_google(audio,language="sv-SE")
        #print("Google thinks you said:\n" + result)
    except Exception as e:
        print(e)
    print("wait")
    return result


def loop():
    result = []
    while True:

        print("Pir")
        print(str(GPIO.input(pirPin)))
        if GPIO.input(pirPin) == 0: #Sensor on
            result.append(listen())
        else:
            size = len(result)
            if(size > 0):
                msg = ""
                for i in range (size):
                    msg += result[i]
                    if(i < size - 1):
                        msg += " "
                sendMail(msg)
                print("SendMail")
                result = []
            else:
                time.sleep(1)

try:
    loop()
except Exception as e:
    print(e)
    GPIO.cleanup()