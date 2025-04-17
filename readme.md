# HARDCODED local virtual assistant (No AI api)

An intelligent, feature-rich voice assistant built in Python that responds to voice commands and performs a wide variety of tasks.

## Features

- **Voice Recognition & Speech Synthesis**: Understands spoken commands and responds with natural-sounding speech
- **Contextual Awareness**: Greets based on time of day and maintains conversation history
- **Web Integration**:
  - Wikipedia searches
  - Weather forecasts with location support
  - News headlines based on preferred topics
  - Website navigation
- **Productivity Tools**:
  - Email sending capability
  - Calendar view
  - Reminders system
  - Time and date information
- **System Functions**:
  - Hardware and system information
  - Music playback
- **Knowledge & Computation**:
  - Wolfram Alpha integration for calculations and knowledge queries
  - Translation framework
- **Entertainment**:
  - Jokes
  - Music playback
- **Personalization**:
  - User preferences and settings
  - Customizable responses

## Requirements

- Python 3.7+
- Internet connection
- Microphone and speakers

## Installation

1. Clone this repository or download the code
2. Install required packages:

```bash
pip install pyttsx3 SpeechRecognition wikipedia wolframalpha pyjokes psutil newsapi-python beautifulsoup4 pytz requests
```

3. Register for required API keys:
   - [OpenWeatherMap API](https://openweathermap.org/api) (weather forecasts)
   - [Wolfram Alpha API](https://products.wolframalpha.com/api/) (calculations and knowledge queries)
   - [News API](https://newsapi.org/) (news headlines)

4. Update the API keys in the code:
```python
# Replace these values with your actual API keys
OPENWEATHER_API_KEY = "your_openweather_api_key"
WOLFRAM_APP_ID = "your_wolfram_alpha_api_key"
NEWS_API_KEY = "your_news_api_key"
```

## Usage

1. Run the assistant:
```bash
python voice_assistant.py
```

2. Wait for the greeting message and the prompt that it's listening
3. Speak your command clearly

## Example Commands

- "What's the weather like in New York?"
- "Search Wikipedia for artificial intelligence"
- "Open YouTube"
- "What time is it?"
- "Tell me a joke"
- "Play some music"
- "What's my system information?"
- "Show me the calendar"
- "Set a reminder to call mom at 5 PM"
- "Calculate the square root of 144"
- "What are the latest news headlines?"
- "Send email to example@mail.com saying hello how are you"

## Email Configuration

To use the email functionality, update these lines with your email credentials:
```python
email_address = "your_email@example.com"  # Replace with actual email
email_password = "your_password"          # Replace with actual password
```

Consider using environment variables or a secure configuration file rather than hardcoding credentials.

## Customization

### Voice Settings

You can adjust the voice properties:
```python
engine.setProperty('voice', preferred_voice)  # Change the voice
engine.setProperty('rate', 180)  # Adjust speaking rate (words per minute)
```

### User Preferences

Modify the `user_preferences` dictionary to customize:
- Name ("Sir" by default)
- Default location for weather
- Temperature unit (celsius/fahrenheit)
- Favorite websites
- News topics of interest

## Troubleshooting

- **"No module named X"**: Run `pip install X` to install the missing package
- **Microphone not working**: Check your microphone settings and permissions
- **Voice recognition issues**: Speak clearly and reduce background noise
- **API errors**: Verify your API keys and internet connection

## Further Development

Potential areas for enhancement:
- Add machine learning for better command recognition
- Implement task scheduling
- Integrate with smart home devices
- Add voice authentication
- Create a GUI interface
- Implement multi-language support
- Add more API integrations (calendar, tasks, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python and various open-source libraries
- Uses multiple API services for enhanced functionality
