import time
import os
from dotenv import load_dotenv
import pyttsx3
from datetime import datetime
from certifi import contents
from google import genai
import sounddevice as sd

load_dotenv()

#client creation
def create_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)

#response model
def generate_response(client, prompt):
    return client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

#token counter
def token_counter(client, prompt):
    return client.models.count_tokens(
    model="gemini-2.5-flash",
    contents=prompt
)
    return result.total_tokens

def main():
    client = create_client()
    current_time = datetime.now()
    prompt = input("Ask: ")
    say_or = input("TTS?(Y for yes/N for no)")
    response = generate_response(client, prompt)
    text=response.text
    tokens = token_counter(client, prompt)
    #file write and read, speak
    def response_output(filename,text):
        with open(filename,"w", encoding="UTF-8") as file:
            file.write(text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    if say_or.upper() == "Y":
        print("\nResponse:")
        print(response.text)
        response_output("output.txt",text)
        print(f"Tokens used: {tokens.total_tokens}")
        print(current_time.strftime("At %H:%M On %D"))
    else: 
        print(f"\nResponse:")
        print(response.text)
        print(f"Tokens used: {tokens.total_tokens}")

if __name__ == "__main__":
    main() # main runs before all else
