import pyttsx3
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit as wk
import random
import subprocess
import cv2
import threading
import pyautogui
import time
import sys
import requests
import operator
import pyjokes
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

camera_open = False

engine = pyttsx3.init('sapi5')     #voice function
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty("rate",200)

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def speak(audio):   #text to speech
    engine.say(audio)
    engine.runAndWait()

def wishme():  #greet function
        hour = datetime.datetime.now().hour
        current_time = datetime.datetime.now().strftime("%I:%M %p")  # Get current time in 12-hour format

        if 4 <= hour < 12:
            message = 'Good morning Sir'
        elif 12 <= hour < 18:
            message = 'Good afternoon Sir'
        else:
            message = 'Good evening Sir'

        print(message)
        speak(message)
        print("It's", current_time)
        speak("It's " + current_time)
        print('I am Shambhu Sir. Please tell me how can I help you')
        speak('I am Shambhu Sir. Please tell me how can I help you')

def takeCommand():    #voice to text
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio,language='en-in')
        print(f"you said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

#open and close the camera 
def open_camera():
    global camera_open
    cap = cv2.VideoCapture(0)
    camera_open = True
    while camera_open:
        ret, img = cap.read()
        cv2.imshow("Camera", img)
        k = cv2.waitKey(50)  # Wait for a key press for 50 milliseconds
        if k == 27:  # 'Esc' key is pressed
            break
    cap.release()
    cv2.destroyAllWindows()
def close_camera():
    global camera_open
    camera_open = False

def news(): #news function
    main_url = 'https://newsapi.org/v2/everything?q=tesla&from=2024-04-24&sortBy=publishedAt&apiKey=a0b7d15a1c7641e6ae658d7d469c6d82'

    main_page = requests.get(main_url).json()
    #print main page
    articles = main_page["articles"]
    #print articles
    head =[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        #print(f"today's {day[i]} news is:{head[i]}")
        speak(f"today's {day[i]} news is:{head[i]}")


def calculator():   #calculation 
    print("I'm ready to perform calculations. Please tell me the operation you want to perform.")
    print("You can say 'add', 'subtract', 'multiply', or 'divide'.")
    speak("I'm ready to perform calculations. Please tell me the operation you want to perform.")
    speak("You can say 'add', 'subtract', 'multiply', or 'divide'.")
    while True:
        query = takeCommand()
        if query == "":
            continue  # Skip further processing if the query is empty

        if "add" in query:
            print("Please tell me the first number.")
            speak("Please tell me the first number.")
            num1 = float(takeCommand())
            print("Please tell me the second number.")
            speak("Please tell me the second number.")
            num2 = float(takeCommand())
            result = num1 + num2 
            print("The result of addition is ", result)
            speak(f"The result of addition is {result}")
        elif "subtract" in query:
            speak("Please tell me the first number.")
            num1 = float(takeCommand())
            speak("Please tell me the second number.")
            num2 = float(takeCommand())
            result = num1 - num2
            speak(f"The result of subtraction is {result}")
        elif "multiply" in query:
            speak("Please tell me the first number.")
            num1 = float(takeCommand())
            speak("Please tell me the second number.")
            num2 = float(takeCommand())
            result = num1 * num2
            speak(f"The result of multiplication is {result}")
        elif "divide" in query:
            speak("Please tell me the first number.")
            num1 = float(takeCommand())
            speak("Please tell me the second number.")
            num2 = float(takeCommand())
            if num2 == 0:
                speak("Error: Cannot divide by zero.")
            else:
                result = num1 / num2
                speak(f"The result of division is {result}")
        elif "stop" in query or "enough" in query:
            speak("Calculator mode deactivated.")
            break
        else:
            speak("Sorry, I didn't understand that. Please try again.")

def openai_conversation(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        ########################        NORMAL CONVERSATION          #####################################################
        if "shambhu" in query:
            print("yes sir")
            speak("yes sir")
        
        elif"hello " in query or "hey" in query:
            speak("hello sir, may I help you with something?")
        
        elif"how are you shambhu" in query:
            print("I am good sir. what about you?")
            speak("I am good sir. what about you?")
        
        elif"also good " in query or "fine" in query or "I am good" in query:
            print("that's great to hear from you sir")
            speak("that's great to hear from you sir")
            
        elif"thank you " in query or "thanks" in query:
            speak("It's my pleasure to assist you sir")

        elif "who are you" in query:
            print('My Name Is Shambhu')
            speak('My Name Is Shambhu')
            print('I can Do Everything that my creator programmed me to do') 
            speak('I can Do Everything that my creator programmed me to do')

        elif "who created you" in query:
            print('Shivam Gopal is My creator, I created with Python Language, in visual studio code')
            speak('Shivam Gopal is my creator, I created with Python Language, in visual studio code')
        
        elif"what is " in query:
            speak("Searching on wikipedia....")
            query = query.replace("what is ", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)
        
        elif"who is " in query:
            speak("Searching on wikipedia....")
            query = query.replace("who is ", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)

        elif "open google" in query:
            speak("sir, what should I search on google")
            cm = takeCommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}") 
        
        elif "open youtube" in query:
            print("What do you want to search on YouTube?")
            speak("What do you want to search on YouTube?")
            search_query = takeCommand().lower()  # Assuming take_command() is a function that captures user input
            if search_query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif "close browser " in query:
            os.system("taskkill /f /im msedge.exe")
        
        elif "close chrome " in query:
            os.system("taskkill /f /im chrome.exe")
        
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif "where i am" in query or "where we are" in query or "tell me my location" in query:
             speak("Wait sir, let me check")
             try:
               ipAdd = requests.get('http://api.ipify.org').text
               print(ipAdd)
               url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'  # Corrected URL construction
               geo_requests = requests.get(url)
               geo_data = geo_requests.json()
               # print(geo_data)
               city = geo_data['city']
               state = geo_data['region']
               country = geo_data['country']
               print(f"Sir, I am not sure, but I think we are in {city} city of {state} state in {country}")
               speak(f"Sir, I am not sure, but I think we are in {city} city of {state} state in {country}")
             except Exception as e:
                speak("Sorry sir, due to network issues I'm not able to find where we are.")
        
        elif"tell me news" in query:
            speak("please wait sir, fetching the latest news")
            news()
        
        
        
    #####################################   APPS   ###################################################
        elif "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)
        elif "close notepad" in query:
              print("Okay sir, closing Notepad.")
              os.system("taskkill /f /im notepad.exe") 
        
        elif "open ms office" in query:
            npath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(npath)
        elif "close ms office" in query:
              print("Okay sir, closing Ms office.")
              speak("Okay sir, closing Ms office.")
              os.system("taskkill /f /im WINWORD.exe")
        elif "open Ms powerpoint" in query or "open powerpoint" in query:
            npath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
            os.startfile(npath)
        elif "close powerpoint" in query:
              print("Okay sir, closing powerpoint.")
              speak("Okay sir, closing powerpoint.")
              os.system("taskkill /f /im WINWORD.exe")
        

        elif "open command prompt" in query:
            cmd_path = r"C:\\Windows\\System32\\cmd.exe"  # Full path to command prompt
            os.system(f"start {cmd_path}")
        elif "close command prompt" in query:
            print("Okay, closing Command Prompt.")
            os.system("taskkill /f /im cmd.exe")

        elif "play music" in query:
            music_dir = "C:\\Users\\Shivam Gopal\\Music\\Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))
        
        elif"play a video" in query:
            npath = "C:\\Users\\Shivam Gopal\\Videos\\Gym Videos"
            videos = os.listdir(npath)
            os.startfile(os.path.join(npath, random.choice(videos)))

        elif"what is the time" in query or "tell me the time" in query or "tell me time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print("Sir, the current time is ", strTime)
            speak(f"sir, the current time is {strTime}")
        
        elif "shutdown system" in query:
            speak("Shutting down the system in 5 seconds.")
            os.system("shutdown /s /t 5")
        
        elif "restart system" in query:
            speak("Restarting the system in 5 seconds.")
            subprocess.run(["shutdown", "/r", "/t", "5"], check=True)
        
        elif"lock the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        
        elif "close all windows" in query:
         print("Okay, closing all windows.")
         os.system("taskkill /f /fi \"STATUS eq RUNNING\"")
        
        elif "take screenshot" in query or "take a screenshot" in query:
            print("sir, please tell me the name for this soreenshot file")
            speak("sir, please tell me the name for this soreenshot file")
            name = takeCommand().lower()
            print("please sir hold the screen for few seconds, i am taking sreenshot")
            speak("please sir hold the screen for few seconds, i am taking sreenshot")
            time.sleep(3)
            img = pyautogui.screenshot() 
            img.save(f"{name}.png")
            print("i am done sir, the screenshot is saved in our main folder. now i am ready for next command")
            speak("i am done sir, the screenshot is saved in our main folder. now i am ready for next command")
        


#################################################    OTHER COMPLEX APPS     ##########################################################################
        elif "open camera" in query and not camera_open:
            threading.Thread(target=open_camera).start()
        elif "close camera" in query and camera_open:
            close_camera()
        
        
        
        elif "ip address" in query or "tell me my ip address" in query or "what is my Ip address" in query:
            print("Fetchin your IP Address please wait sir!")
            speak("Fetchin your IP Address please wait sir!")
            try:
                ip = requests.get('https://api.ipify.org').text  # Corrected URL
                print("Your IP address is ",ip)
                speak(f"Your IP address is {ip}")
            except Exception as e:
                speak("network is weak, please try gain after sometime later")

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(5)
            pyautogui.keyUp("alt")
        
        elif "tell me the temperature" in query or "what is the temprature" in query or "today's temprature" in query:
            search = "temperature in delhi"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            print("Today's temprature is",temp )
            speak(f"Current {search} is {temp}")
        elif "perform calculation" in query or "can you perform some calculations" in query:
            calculator()
       ###############################################       BUTTON ACTIONS        #####################################################
       
        elif "volume up" in query: 
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup") 
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")

        elif "volume down" in query: 
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
        elif "mute" in query:
            pyautogui.press("volumemute")
        elif"scroll down" in query:
            pyautogui.scroll(1000)

        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak("sir please tell me you want to hide this folder or make it visible for everyone")
            condition = takeCommand().lower()
            if "hide" in condition:
                os.system("attrib +h /s /d") #os module
                speak("sir, all the files in this folder are now hidden.")
            elif "make all files visible" in condition:
                os.system("attrib -h /s /d")
                speak("sir, all the files in this folder are now visible to everyone. i wish you are taking taking this decision in your peace")
            elif "leave it" in condition or "leave for now" in condition:
                speak("Ok sir")
        
        else:
            print("Thinking...")
            response = openai_conversation(query)
            print(response)
            speak(response)


        

            
                

