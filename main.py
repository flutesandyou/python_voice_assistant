import speech_recognition as sr
import pyttsx3
import openai

# Set up the OpenAI ChatGPT API
openai.api_key = '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'  # Replace with your actual OpenAI API key

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_for_keyword(keyword="jarvis"):
    """Function to listen for the specified keyword"""
    while True:
        with sr.Microphone() as source:
            print("Listening for keyword...")
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            if keyword in query.lower():
                return True
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            print("Sorry, I'm currently offline. Please try again later.")

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
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        print("Sorry, I'm currently offline. Please try again later.")

    return ""

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
speak("Waiting for keyword 'Jarvis'...")
listen_for_keyword("jarvis")
speak("Keyword detected. How can I assist you?")

while True:
    command = listen().lower()

    if "exit" in command:
        speak("Goodbye!")
        break
    else:
        chat_with_gpt()