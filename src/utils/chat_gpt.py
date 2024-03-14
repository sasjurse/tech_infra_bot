import os
import time

import openai

RATE_LIMIT_DELAY = 45


path = os.path.join(os.path.expanduser('~'), 'secrets/open_ai_key')
with open(path) as file:
    api_key = file.read()

openai.api_key = api_key


def ask_chatgpt(messages: list, model='gpt-4', temperature=1.0):

    try:
        response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=1_000, temperature=temperature)
    except openai.error.RateLimitError as e:
        print(f'Hit RateLimitError, waiting {RATE_LIMIT_DELAY} seconds')
        print(e)
        time.sleep(RATE_LIMIT_DELAY)
        response = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=1_000)

    return response['choices'][0]['message']['content']