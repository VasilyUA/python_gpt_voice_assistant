from time import sleep

import speech_recognition as sr
from gtts import gTTS
import os
import atexit
import uuid
import pygame

from gpt_chat import GPT


def remove_temp_file(temp_file=None):
    if os.path.exists(temp_file):
        os.remove(temp_file)


class VoiceAssistant:
    def __init__(self):
        self.r = sr.Recognizer()

        self.gpt = GPT()

        self.temp_file = f"temp_{uuid.uuid4().hex}.mp3"

    def listen(self):

        while True:
            sleep(0.5)
            print("Чим можу допомогти?")
            with sr.Microphone() as source:
                audio = self.r.listen(source)
                try:
                    text = self.r.recognize_google(audio, language="uk-UA")
                    yield text
                except sr.UnknownValueError:
                    print("Я не зрозумів про що ви говорите")
                except sr.RequestError:
                    print("Сервіс не доступний")

    def speak(self, text):
        tts = gTTS(text=text, lang='uk', slow=False, lang_check=False)
        tts.save(self.temp_file)

        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

        remove_temp_file(self.temp_file)

    def run(self):
        print("Привіт, я ваш допоміжник!")
        self.speak("Привіт, я ваш допоміжник! Чим можу допомогти?")
        for text in self.listen():
            print("Ви кажете:", text)
            answer = self.gpt.request(text)
            print("Jarvis відповідає:", answer)
            self.speak(answer)


if __name__ == '__main__':
    assistant = VoiceAssistant()
    assistant.run()
    atexit.register(remove_temp_file, assistant.temp_file)
