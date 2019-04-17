import pyttsx3
import os
import datetime
import math
import calendar
import keyboard
import speech_recognition as sr
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 150)
r = sr.Recognizer()
mic = sr.Microphone()
marker = True


def reset():
    now = datetime.datetime.now()
    year =  now.year
    month = calendar.month_name[now.month]
    day = now.day
    hour = now.hour
    minute = now.minute
    seconds = now.second
    if hour > 12:
        ap = 'P.M.'
    else:
        ap = 'A.M.'
    hour = now.hour%12
    return [year,month,day,hour,minute,seconds,ap]

def speak(date):
    engine.say(date)
    engine.runAndWait()
    
def generate():
    global str1,str2,str3
    year,month,day,hour,minute,seconds,ap = reset()
    str1 = 'Hey Sammy It is {} {} {}'.format(hour,minute,ap)
    str2 = 'Good Morning Sammy the date is {} {}, {} and the time is {} {} {}'.format(month,day,year,hour,minute,ap)
    str3 = 'Layla is the best!'
    
def inactive():
    global marker
    if marker == True:
        print('Inactive')
        marker = False

def grabclip():
    print('Listening')
    print('')
    with mic as source:
        audio = r.listen(source)
        try:
            audioclip = r.recognize_google(audio)
            speak(audioclip)
            print(audioclip)
        except:
            print('Voice error')
            marker = True
    return audioclip

def reminders():
    f = open('reminders.txt','r')
    content = f.read()
    speak(content)

def weather(zipcode):
    appid= 'e350e196492bc67d38775f1b4dfdd574'
    url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',us&appid=' + appid
    res = requests.get(url)
    data = res.json()
    temperature = int((data['main']['temp']-273.15)*(9/5)+32)
    areaname = data['name']
    condition = data['weather'][0]['main']
    weatherstr = 'WEATHER. It is {} degrees outside and the forecast is {} in {}.'.format(temperature,condition,areaname)
    speak(weatherstr)
    
def startup():
    generate()
    speak(str2)
    reminders()
    
startup()
weather('07013')

while True:
    inactive()
    try:
        if keyboard.is_pressed('up') and keyboard.is_pressed('down'):
            audioclip = grabclip()
            print('x')
            if audioclip == 'Layla':
                generate()
                speak(str3)
            if audioclip == 'weather':
                weather('07013')
            if audioclip == 'time':
                print('in time')
                generate()
                speak(str1)
            if audioclip == 'morning':
                generate()
                speak(str2)
            if audioclip == 'reminders':
                reminders()
            marker = True
    except:
        print('Key Error')
        marker = True
        continue

