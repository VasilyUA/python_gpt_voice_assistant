import openai
from config import gpt_key


class GPT:
    def __init__(self):
        openai.api_key = gpt_key
        self._messages = []

    def request(self, message):
        self._messages.append({"role": "user", "content": message})
        print('Jarvis відповідає...')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages
        )
        self._messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        return completion.choices[0].message.content


if __name__ == '__main__':
    gpt = GPT()
    data = input("Введіть ваше повідомлення: ")
    print(gpt.request(data))
