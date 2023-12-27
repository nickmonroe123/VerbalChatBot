import os
import time
import pyaudio
import speech_recognition as sr
import playsound
from gtts import gTTS
# pip install openai==0.28
# needed to use this version. Newer openai does not have ChatCompletion module
import openai
import uuid

api_key = "your-code-here"
lang = 'en'

openai.api_key = api_key

guy = ""

while True:
    def talk_to_bot():
        r = sr.Recognizer()
        # Might need to set device_index=1
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                global guy
                guy = said

                if "Nick" in said:
                    new_string = said.replace("Nick", "")
                    new_string = new_string.strip()

                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                    text = completion.choices[0].message.content
                    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                    file_name = f"welcome_{str(uuid.uuid4())}.mp3"
                    speech.save(file_name)
                    playsound.playsound(file_name, block=False)

            except Exception as e:
                print(f"Exception: {str(e)}")

        return said

    if "Finished" in guy:
        break

    talk_to_bot()