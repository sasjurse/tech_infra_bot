from utils.chat_gpt import ask_chatgpt
from utils.stored_data import retrieve_current_plan

SYSTEM_INTRO = ("You are a discussion partner for a coding project. "
                "We are designing a roadmap and sketching a tech stack.")


def ask_about_project(question: str):
    current_plan = retrieve_current_plan()
    system_prompt = SYSTEM_INTRO + f" Here is the current plan: {current_plan}"

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]

    return ask_chatgpt(messages, model='gpt-4')
