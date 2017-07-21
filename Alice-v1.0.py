#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import sys
import time
from time import strftime
import os
import webbrowser
sys.path.append('/usr/local/lib/python2.7/site-packages/pyobjc_core-3.2.1-py2.7-macosx-10.12-x86_64.egg/')
import objc
sys.path.append('/usr/local/lib/python2.7/site-packages/pyobjc_framework_Cocoa-3.2.1-py2.7-macosx-10.12-x86_64.egg/')
from AppKit import NSSpeechSynthesizer
import requests
from bs4 import BeautifulSoup
import googlemaps
from googlemaps import distance_matrix
from googlemaps import Client
#from geolocation.distance_matrix.main import *
#from geolocation.distance_matrix.client import *
import random
from google import search


#Manual import of speech synthasizer from pyobjc pip files
#Weren't synching to the python directory


    
#-------------------------------------------------------------------------------------------------------------------------

class AliceClass:
    """A class setup to handle the AI Assistant"""
    def __init__(self):
        voice = NSSpeechSynthesizer.alloc().initWithVoice_("com.apple.speech.synthesis.voice.karen")
        self.voice = voice
        rate = NSSpeechSynthesizer.setRate_(self.voice,163)
        self.rate = rate
        pitch = NSSpeechSynthesizer._setPitchBase_(self.voice,182.00)
        self.pitch = pitch
        self.destination = None
        self.lat = None
        self.lon = None
        self.googleUrl = None
        self.postalCode = None
        self.greetingWords = ["hey","hello","what's up","alice","sup","hi","hey alice","hello alice"]
        self.responseWords = ["Hello","What's up John","Hey John","Hello John","What should we do today","How's it going"]
        self.whoWords = ["what is your name","what's your name","who are you","what are you","who am i talking to"]
        
        
        
        



    
    def speak(self,audioString):
        print(audioString)
#nssp -- variable for NSSpeechSynthesizer    
#Karen is the variable for AI Assistant and initial attributes , set the voice to karen
#have karen start speaking the audiostring for response to conversation
        self.voice.startSpeakingString_(audioString)
    
    

    def recordAudio(self):
    # Record Audio
        r = sr.Recognizer()
#Name source of audio recording as master microphone at time of use
        with sr.Microphone() as source:
#variable audio -- recognizer's listener module to source(microphone)
            audio = r.listen(source)
# Speech recognition using Google Speech Recognition
        data = ""
        try:
        
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            data = r.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
        return data



 
    def jarvis(self,data):
        data = data.lower()

#Greeting words response
        for word in self.greetingWords:
            if word in data.lower():
                self.speak(random.choice(self.responseWords))
        
        
#How are you response
        if "how are you" in data:
            self.speak("I am fine")


#Who are you response
        for word in self.whoWords:
            if word in data.lower():
                response = ["Alice","My name is Alice","Hello I am Alice","Alice, what's your name?"]
                self.speak(random.choice(response))




#The time and date response
        if "what time is it" in data:
            NSSpeechSynthesizer.setRate_(self.voice,150)
            self.speak(strftime("%a,%b %d %I:%M%p"))



#Google search from search command response
        if "search" in data:
            data = data.split(" ")
            if "for" in data:
                info = " ".join(data[data.index("for")+1:])
                webbrowser.open("http://www.google.com/search?q="+info)
            else:
                info = " ".join(data[data.index("search")+1:])
                webbrowser.open("http://www.google.com/search?q="+info)                


#Google maps search from "Where is" command response 
        if "where is" in data:
            data = data.split(" ")
            location = " ".join(data[data.index("is")+1:])
            self.speak("Hold on John, I will show you where " + location + " is.")
            webbrowser.open('https://www.google.com/maps/place/'+location)


#The distance from current location to commanded destination
        if "how far is" in data:
             
             data = data.split(" ")
             if "from" in data:
                 num = data.index('from')
                 dest = " ".join(data[data.index("is")+1:int(num)])
                 print("dest: "+dest)
                 self.dest = dest
                 self.address()
                 self.destinationLoc(dest)
                 
             else:
                 dest = " ".join(data[data.index("is")+1:])
                 print("dest: "+dest)
                 self.dest = dest
                 self.address()
                 self.destinationLoc(dest)


#Google search questions for automated answers
        if "what movies" in data:
            
            
            urlString = requests.get("https://www.fandango.com/moviesintheaters")
            soup = BeautifulSoup(urlString.content, "html.parser")
            stuff = soup.prettify()
            matches = soup.find('ul','mega-menu-movie-list')
            items = matches.findAll("li")
            movies = 'Movies currently playing in theaters are: '
            for i in range(len(items)-1):
                items[i] = items[i].find('a')
                if i < (len(items)-2):
                    movies+=' '.join(items[i].contents)+","
                else:
                     movies+=' '.join(items[i].contents)
            self.speak(movies)





        if "what time" and "playing" in data:
            
            movieNum = []
            self.address()
            playing = data.index('playing')
            isNum = data.index('is')
            movie = data[(isNum+3):(playing-1)]
            times = movie + "'s showtimes today are: "
            urlString = requests.get("https://www.fandango.com/"+self.postalCode+"_movietimes?q="+self.postalCode)
            soup = BeautifulSoup(urlString.content, "html.parser")
            stuff = soup.prettify()
            
            matches = soup.findAll('span',itemprop='event')
            for i in range(len(matches)):
                items = matches[i].find('meta',itemprop='name')
                
                if movie in str(items).lower().split('"'):
                    movieNum.append(i)
                
            for num in movieNum:
                movies = matches[num]
                infoList = movies.findAll('meta',itemprop='startDate')
                for i in range(len(infoList)):
                    info = str(infoList[i]).split('"')
                    info = info[1].split("T")
                    info =info[1].split("-")
                    militime = info[0]
                    militime = militime[0:-3]
                    hours, minutes = militime.split(":")
                    hours, minutes = int(hours), int(minutes)
                    setting = "AM"
                    if hours > 12:
                        setting = "PM"
                        hours -= 12
                    if i < (len(infoList)-1):
                        times += ("%02d:%02d" + setting) % (hours, minutes) + ", "
                    
            self.speak(times)
                        
                               
            
            
            
            
            movies = 'Movies currently playing in theaters are: '
##            for i in range(len(items)-1):
##                items[i] = items[i].find('a')['href']
##                playing = data.index('playing')
##                isNum = data.index('is')
##                movie = data[(isNum+3):(playing-1)]
##                if movie in items[i]:
##                    urlString = requests.get(items[i])
##                    soup = BeautifulSoup(urlString.content, "html.parser")
##                    stuff = soup.prettify()
##                    print(stuff)
                    
                

#Address function
#Uses geocoder API different from Google API to grab computers
#server IP Address and compute the longitude and latitude from that IP server location           
    def address(self):
 
        freegeoip = "http://freegeoip.net/json"
        geo_r = requests.get(freegeoip)
        geo_json = geo_r.json()
        self.postalCode = geo_json["zip_code"]
        user_position = [geo_json["latitude"], geo_json["longitude"]]
        lat_ip=user_position[0]
        lon_ip=user_position[1]
        self.lat = lat_ip
        self.lon = lon_ip
        location = lat_ip,lon_ip
        print("Address Function: ",location)

      
            
#looks up destination longitude and latitude
#Commences the distance function
    def destinationLoc(self,position):
        
        userAddress = position
        google_maps = googlemaps.Client(key='AIzaSyBccaOBwoaN4bA47yLrXTG-H2Bp4hXvkVI') 
        my_location = google_maps.geocode(address=userAddress) # sends search to Google Maps.
        self.destination = (my_location[0]["geometry"]["location"]["lat"],my_location[0]["geometry"]["location"]["lng"])
        self.distance()


#uses Googls Maps API to find the distance and duration of travel from current
#location to destination location

    def distance(self):
        google_maps = googlemaps.Client(key='AIzaSyCpNvG8hdPXMMRvG6vPvx9RNtBnJdZw9-M')
        # default mode parameter is const.MODE_DRIVING.
        origins = (self.lat,self.lon)
        destinations = self.destination
        items = google_maps.distance_matrix(origins,destinations,mode=None, avoid=None)
        meters = int(items["rows"][0]["elements"][0]["distance"]["value"])
        miles = int(meters / float(1609.344))
        duration = items["rows"][0]["elements"][0]["duration"]["text"]
        distanceString = ("Your destination is "+ str(miles) + " miles and " + str(duration) + " away from your current location.")
        self.speak(distanceString)
    
    
# initialization




AliceClass().speak("HI John, can I help you with something?")
##while True:
##    time.sleep(3)
 #   data = AliceClass().recordAudio()
AliceClass().jarvis("What movies")
                                
                                
                                


