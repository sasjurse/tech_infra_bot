from utils.chat_gpt import ask_chatgpt
from utils.stored_data import retrieve_document, add_to_history, retrieve_history

SYSTEM_INTRO = ("You are a discussion partner for a coding project. "
                "We are designing a roadmap and sketching a tech stack.")


def ask_about_project(question: str, project_id: int):
    if check_if_question_is_repeated(question, project_id):
        return "We have already discussed this question. Please ask a new question."

    current_plan = retrieve_document('project_plan', project_id)
    requirements = retrieve_document('requirements', project_id)
    system_prompt = (SYSTEM_INTRO
                     + f" Here are the current requirements: {requirements}."
                     + f" Here is the current plan: {current_plan}")

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
    answer = ask_chatgpt(messages, model='gpt-3.5-turbo-0125')

    for message in messages:
        add_to_history(message['role'], message['content'], project_id=project_id)
    add_to_history('assistant', answer, project_id=project_id)

    return answer


def summarize_tech_stack(project_id: int):
    question = 'Can you summarize the tech stack in 5 bullet points?'
    system_prompt = (SYSTEM_INTRO + f" Here are the current requirements: " +
                     f" Here is the current plan: {retrieve_document('project_plan', project_id)}")
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}]
    answer = ask_chatgpt(messages, model='gpt-4')

    return answer


def check_if_question_is_repeated(question: str, project_id: int):
    # Streamlit can ask the same question when it refreshes the page. This is just a workaround.
    # Return value of the function is not used in the streamlit app.
    history = retrieve_history(project_id=project_id)
    for chat_entry in history.entries:
        if chat_entry.role == 'user' and chat_entry.content == question:
            return True
    return False
