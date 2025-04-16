import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import random
import requests
import json
import os
import sys
import time
import subprocess
import smtplib
import wolframalpha
import calendar
import pytz
import pyjokes
from email.message import EmailMessage
from newsapi import NewsApiClient
from bs4 import BeautifulSoup

# Initialize TTS engine with appropriate voice engine
try:
    engine = pyttsx3.init('nsss')  # macOS
except:
    engine = pyttsx3.init()  # Default fallback

voices = engine.getProperty('voices')

# Try to set Samantha as the voice, fallback to default if not found
preferred_voice = None
for voice in voices:
    if "samantha" in voice.name.lower():
        preferred_voice = voice.id
        break

engine.setProperty('voice', preferred_voice if preferred_voice else voices[0].id)
engine.setProperty('rate', 180)  # Adjust speaking rate

# API Keys and Configuration
OPENWEATHER_API_KEY = "sk"
DEFAULT_LAT = "40.735619"
DEFAULT_LON = "-74.175834"
WOLFRAM_APP_ID = "YOUR_WOLFRAM_ALPHA_API_KEY"  # Add your key here
NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Add your key here

# User preferences - can be updated via settings command
user_preferences = {
    "name": "Sir",
    "location": "New York",
    "weather_unit": "celsius",  # celsius or fahrenheit
    "news_topics": ["technology", "science"],
    "favorite_websites": {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "gmail": "https://mail.google.com"
    },
    "reminders": []
}

# Conversation memory - stores recent interactions
conversation_history = []
MAX_HISTORY = 10

def speak(audio):
    """Convert text to speech"""
    print(f"🔊 Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()

def log_conversation(role, text):
    """Add conversation to history"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    conversation_history.append({"timestamp": timestamp, "role": role, "text": text})
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

def wishMe():
    """Greet user based on time of day"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    speak(f"{greeting} {user_preferences['name']}. I am Jarvis, your personal assistant. How can I help you today?")

def takeCommand():
    """Listen for user command"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🗣️ You said: {query}")
        log_conversation("user", query)
    except Exception as e:
        print(f"🤔 Recognition error: {e}")
        return "None"
    return query.lower()

def get_weather(city=None):
    """Get weather for a specific city or default location"""
    try:
        if city:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        else:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={DEFAULT_LAT}&lon={DEFAULT_LON}&appid={OPENWEATHER_API_KEY}"
        
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract weather information
        weather_desc = data["weather"][0]["description"]
        temp_kelvin = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_name = data["name"]
        
        # Convert temperature based on user preference
        if user_preferences["weather_unit"] == "celsius":
            temp = round(temp_kelvin - 273.15, 1)
            temp_unit = "Celsius"
        else:
            temp = round((temp_kelvin - 273.15) * 9/5 + 32, 1)
            temp_unit = "Fahrenheit"
        
        weather_report = f"Weather in {city_name}: {weather_desc}. Temperature is {temp} degrees {temp_unit}. "
        weather_report += f"Humidity is {humidity}% and wind speed is {wind_speed} meters per second."
        
        return weather_report
    except Exception as e:
        print(f"Weather error: {e}")
        return "Sorry, I couldn't fetch the weather information right now."

def search_wikipedia(query):
    """Search Wikipedia for information"""
    try:
        speak("Searching Wikipedia...")
        # Remove 'wikipedia' from the query
        query = query.replace("wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia:")
        print(f"📚 {results}")
        speak(results)
    except Exception as e:
        print(f"Wikipedia error: {e}")
        speak("Sorry, I couldn't find relevant information on Wikipedia.")

def get_news():
    """Get latest news headlines"""
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        topics = " OR ".join(user_preferences["news_topics"])
        top_headlines = newsapi.get_top_headlines(q=topics, language='en', page_size=5)
        
        if top_headlines["totalResults"] > 0:
            speak(f"Here are the top {min(5, top_headlines['totalResults'])} news headlines:")
            for i, article in enumerate(top_headlines["articles"], 1):
                headline = f"{i}. {article['title']}"
                print(f"📰 {headline}")
                speak(headline)
                time.sleep(0.5)
        else:
            speak("Sorry, I couldn't find any relevant news at the moment.")
    except Exception as e:
        print(f"News API error: {e}")
        speak("I'm having trouble fetching the latest news. Please try again later.")

def set_reminder(query):
    """Set a reminder for a specific time or date"""
    try:
        # Simple parsing for time-based reminders
        # Example: "remind me to call mom at 5 pm"
        reminder_text = query.split("remind me to")[1].split("at")[0].strip()
        reminder_time = query.split("at")[1].strip()
        
        # Basic reminder storage
        user_preferences["reminders"].append({
            "text": reminder_text,
            "time": reminder_time,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        speak(f"I've set a reminder for you to {reminder_text} at {reminder_time}")
    except Exception:
        speak("I couldn't understand the reminder format. Please try again with something like 'remind me to call mom at 5 pm'.")

def tell_joke():
    """Tell a random joke"""
    joke = pyjokes.get_joke()
    print(f"😂 {joke}")
    speak(joke)

def perform_calculation(query):
    """Use Wolfram Alpha for calculations and queries"""
    try:
        client = wolframalpha.Client(WOLFRAM_APP_ID)
        
        # Remove trigger words for cleaner query
        query = query.replace("calculate", "").replace("solve", "").replace("what is", "").strip()
        
        res = client.query(query)
        answer = next(res.results).text
        
        print(f"🧮 {answer}")
        speak(f"The answer is {answer}")
    except Exception as e:
        print(f"Calculation error: {e}")
        speak("I'm sorry, I couldn't solve that calculation.")

def get_system_info():
    """Get basic system information"""
    try:
        import platform
        import psutil
        
        system_info = f"Operating System: {platform.system()} {platform.version()}"
        system_info += f"\nProcessor: {platform.processor()}"
        
        # Get memory information
        memory = psutil.virtual_memory()
        system_info += f"\nMemory: {memory.percent}% used ({round(memory.used/1024/1024/1024, 2)}GB of {round(memory.total/1024/1024/1024, 2)}GB)"
        
        # Get disk information
        disk = psutil.disk_usage('/')
        system_info += f"\nDisk: {disk.percent}% used ({round(disk.used/1024/1024/1024, 2)}GB of {round(disk.total/1024/1024/1024, 2)}GB)"
        
        # Get battery information if available
        if hasattr(psutil, "sensors_battery") and psutil.sensors_battery():
            battery = psutil.sensors_battery()
            system_info += f"\nBattery: {battery.percent}% {'charging' if battery.power_plugged else 'discharging'}"
        
        print(f"💻 {system_info}")
        speak("Here's your system information:")
        speak(system_info.replace("\n", ". "))
        return system_info
    except Exception as e:
        print(f"System info error: {e}")
        speak("I couldn't retrieve complete system information.")
        return "Basic system info unavailable."

def send_email(query):
    """Send an email using configured account"""
    try:
        # Extract recipient and content from query
        # Example: "send email to john@example.com saying hello how are you"
        to_email = query.split("to")[1].split("saying")[0].strip()
        content = query.split("saying")[1].strip()
        
        # Configure email sender (would need real credentials)
        email_address = "your_email@example.com"  # Replace with actual email
        email_password = "your_password"          # Replace with actual password
        
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = f"Message from Voice Assistant"
        msg['From'] = email_address
        msg['To'] = to_email
        
        speak(f"Preparing to send email to {to_email}")
        speak("Here's the content of your email:")
        speak(content)
        speak("Should I send this email? Say yes or no.")
        
        confirm = takeCommand()
        if "yes" in confirm:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
            speak("Email has been sent successfully")
        else:
            speak("Email sending cancelled")
    except Exception as e:
        print(f"Email error: {e}")
        speak("I'm sorry, I couldn't send the email. Please check your email configuration.")

def open_website(query):
    """Open a website based on name or URL"""
    try:
        # Check if it's a favorite website
        for name, url in user_preferences["favorite_websites"].items():
            if name in query:
                speak(f"Opening {name}")
                webbrowser.open(url)
                return
        
        # If not found in favorites, try to open directly
        if "open" in query:
            website = query.replace("open", "").strip()
            if not website.startswith(("http://", "https://")):
                website = "https://" + website
            if not website.endswith(".com") and "." not in website:
                website = website + ".com"
            
            speak(f"Opening {website}")
            webbrowser.open(website)
    except Exception as e:
        print(f"Website error: {e}")
        speak("I couldn't open that website. Please try again.")

def play_music():
    """Play music from a local directory or streaming service"""
    try:
        music_dir = os.path.expanduser("~/Music")  # Adjust path as needed
        songs = os.listdir(music_dir)
        if songs:
            song = random.choice(songs)
            song_path = os.path.join(music_dir, song)
            speak(f"Playing {song}")
            
            # Choose appropriate player based on OS
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", song_path])
            elif sys.platform == "win32":  # Windows
                os.startfile(song_path)
            else:  # Linux
                subprocess.run(["xdg-open", song_path])
        else:
            speak("No music files found in your music directory.")
    except Exception as e:
        print(f"Music error: {e}")
        speak("I couldn't play music at the moment.")

def get_calendar_events():
    """Show calendar for current month"""
    now = datetime.datetime.now()
    cal = calendar.month(now.year, now.month)
    print(f"📅 Calendar:\n{cal}")
    speak(f"Here's the calendar for {calendar.month_name[now.month]} {now.year}")

def translate_text(query):
    """Translate text to another language"""
    try:
        # Example: "translate hello to spanish"
        text = query.split("translate")[1].split("to")[0].strip()
        target_lang = query.split("to")[1].strip()
        
        # Using a web service for translation would be ideal
        # This is a simplified placeholder
        speak(f"Translating '{text}' to {target_lang}")
        speak("Translation feature requires an additional API integration.")
    except Exception:
        speak("I couldn't understand the translation request format.")

def main():
    """Main function to run the assistant"""
    wishMe()
    
    while True:
        query = takeCommand()
        
        # Skip processing for empty queries
        if query == "None":
            continue
            
        # Wikipedia searches
        if 'wikipedia' in query:
            search_wikipedia(query)
            
        # Open websites
        elif any(site in query for site in ["open youtube", "open google", "open github", "open gmail"]):
            open_website(query)
            
        # Time related queries
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            
        # Date related queries
        elif 'date today' in query or 'what is the date' in query:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")
            
        # Weather information
        elif 'weather' in query:
            if "in" in query:
                city = query.split("in")[1].strip()
                weather_info = get_weather(city)
            else:
                weather_info = get_weather()
            speak(weather_info)
            
        # System information
        elif 'system info' in query or 'system information' in query:
            get_system_info()
            
        # Calendar
        elif 'calendar' in query or 'show calendar' in query:
            get_calendar_events()
            
        # Play music
        elif 'play music' in query or 'play a song' in query:
            play_music()
            
        # Tell jokes
        elif 'joke' in query or 'make me laugh' in query:
            tell_joke()
            
        # News updates
        elif 'news' in query or 'headlines' in query:
            get_news()
            
        # Email functionality
        elif 'send email' in query or 'send mail' in query:
            send_email(query)
            
        # Set reminders
        elif 'remind me' in query:
            set_reminder(query)
            
        # Show reminders
        elif 'show reminders' in query or 'my reminders' in query:
            if user_preferences["reminders"]:
                speak("Here are your reminders:")
                for i, reminder in enumerate(user_preferences["reminders"], 1):
                    speak(f"Reminder {i}: {reminder['text']} at {reminder['time']}")
            else:
                speak("You don't have any reminders set.")
                
        # Math calculations
        elif any(word in query for word in ['calculate', 'solve', 'what is']):
            perform_calculation(query)
            
        # Translation
        elif 'translate' in query:
            translate_text(query)
            
        # Conversation history
        elif 'what did i say' in query or 'conversation history' in query:
            if conversation_history:
                speak("Here are our recent interactions:")
                for i, conv in enumerate(conversation_history[-5:], 1):
                    print(f"{conv['timestamp']} - {conv['role']}: {conv['text']}")
                    if i <= 3:  # Only speak the last 3 for brevity
                        speak(f"At {conv['timestamp']}, {conv['role']} said: {conv['text']}")
            else:
                speak("We haven't had any conversations yet.")
                
        # Assistant information
        elif 'who are you' in query or 'what can you do' in query:
            capabilities = """
            I'm your personal voice assistant. I can help you with:
            - Web searches and Wikipedia lookups
            - Weather forecasts and news updates
            - Playing music and telling jokes
            - Setting reminders and checking calendars
            - Simple calculations and translations
            - System information and website navigation
            - Sending emails and much more
            """
            speak(capabilities.strip())
            
        # Settings and preferences
        elif 'change my name' in query:
            speak("What should I call you?")
            new_name = takeCommand()
            if new_name != "None":
                user_preferences["name"] = new_name
                speak(f"I'll call you {new_name} from now on.")
                
        # Exit command
        elif any(word in query for word in ['exit', 'quit', 'stop', 'goodbye', 'bye']):
            speak(f"Goodbye {user_preferences['name']}. Have a great day!")
            break
            
        # Default response
        else:
            speak("I'm not sure how to help with that yet. Is there something else you'd like to know?")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Program terminated by user. Goodbye!")
    except Exception as e:
        print(f"Critical error: {e}")
        speak("I encountered an error and need to shut down. Please restart the program.")