import pyttsx3
import datetime


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetMe():
      hour = int(datetime.datetime.now().hour)

      if 4<= hour < 12:
          message = 'Good morning'
      elif 12 <= hour < 18:
        message = 'Good afternoon'
      else:
        message = 'Good evening'
        print(message)  # Print the message
        speak(message)  # Speak the message
      speak('I am Shambhu Sir. Please tell me how can I help you')