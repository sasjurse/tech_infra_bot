from utils.chat_gpt import ask_chatgpt
from utils.stored_data import retrieve_plan, add_to_history, retrieve_requirements, retrieve_history

SYSTEM_INTRO = ("You are a discussion partner for a coding project. "
                "We are designing a roadmap and sketching a tech stack.")


def ask_about_project(question: str):
    # Streamlit can ask the same question when it refreshes the page. This is just a workaround.
    # Return value of the function is not used in the streamlit app.
    if check_if_question_is_repeated(question):
        return "We have already discussed this question. Please ask a new question."

    current_plan = retrieve_plan()
    requirements = retrieve_requirements()
    system_prompt = (SYSTEM_INTRO
                     + f" Here are the current requirements: {requirements}."
                     + f" Here is the current plan: {current_plan}")

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
    answer = ask_chatgpt(messages, model='gpt-4')

    for message in messages:
        add_to_history(message['role'], message['content'])
    add_to_history('assistant', answer)

    return answer


def check_if_question_is_repeated(question: str):
    history = retrieve_history()
    for chat_entry in history.entries:
        if chat_entry.role == 'user' and chat_entry.content == question:
            return True
    return False
