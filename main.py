import speech_recognition as sr
import pyttsx3
import openai

# Set up the OpenAI ChatGPT API
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual OpenAI API key

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to user's speech"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.8
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        print("Sorry, I'm currently offline. Please try again later.")
        return ""

    return query

def chat_with_gpt():
    """Function to chat with ChatGPT"""
    speak("Sure, go ahead and ask your question.")
    question = listen()
    
    if question:
        speak("Let me find the answer for you.")
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=question,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        
        if answer:
            print(f"ChatGPT: {answer}")
            speak(answer)
        else:
            print("Sorry, I couldn't find an answer.")
            speak("Sorry, I couldn't find an answer.")
    else:
        speak("Sorry, I didn't hear your question.")

# Main program loop
while True:
    speak("How can I assist you?")
    command = listen().lower()

    if "chat" in command:
        chat_with_gpt()
    elif "exit" in command:
        speak("Goodbye!")
        break
    else:
        speak("Sorry, I don't understand that command.")
