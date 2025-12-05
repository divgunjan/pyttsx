import time
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
lang_model = "gemini-2.5-flash"
speech_model = "gemini-2.0-pro-exp-02-05"

#client creation
def create_client():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    return client

#response model
def generate_response(client, prompt):
    return client.models.generate_content(
    model=lang_model,
    contents=prompt
)
#lambda function for generate_response
# gr = lambda client, prompt: client.models.generate_content(
#     model = lang_model,
#     contents=prompt
# ) 

def speech(filename, client, text):
    response = client.models.generate_content(
        model=speech_model,
        contents=text,
        audio_config={
            "voice": "phoenix",
            "format": "mp3"
        }
    )

    with open(filename, "wb") as f:
        f.write(response.audio)

    print("Audio saved as", filename)


#token counter
def token_counter(client, prompt):
    return client.models.count_tokens(
    model=lang_model,
    contents=prompt
)
    return result.total_tokens

def main():
    client = create_client() #client calling
    prompt = input("Ask: ")
    say_or = input("TTS?(Y for yes/N for no)")
    response = generate_response(client=client, prompt=prompt)
    tokens = token_counter(client, prompt)
    text = response.text
    if say_or.upper() == "Y":
        print("\nResponse:")
        print(text)
        speech("out_audio.mp3",client,text)        
        print(f"Tokens used: {tokens.total_tokens}") 
    else: 
        print(f"\nResponse:")
        print(text)
        print(f"Tokens used: {tokens.total_tokens}")

if __name__ == "__main__":
    main() # main runs before all else
