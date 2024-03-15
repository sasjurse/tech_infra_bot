import streamlit as st

from utils.stored_data import retrieve_plan, retrieve_history, store_plan, retrieve_requirements, store_requirements
from context_creation import ask_about_project

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([3, 1, 3])


def updated_plan_callback():
    new_text = st.session_state['plan']
    store_plan(new_text)


def updated_requirements_callback():
    new_text = st.session_state['requirements']
    store_requirements(new_text)


with col1:
    st.title('The Project')
    tab1, tab2, tab3, tab4 = st.tabs(['Requirements', 'Edit requirements', 'Project plan', 'Edit project plan'])

    with tab1:
        st.write(retrieve_requirements())

    with tab2:
        st.text_area(value=retrieve_requirements(), key='requirements', on_change=updated_requirements_callback,
                     label='Requirements', height=800)

    with tab3:
        st.write(retrieve_plan())

    with tab4:
        st.text_area(value=retrieve_plan(), key='plan', on_change=updated_plan_callback, label='Plan', height=800)

with col3:
    st.title('Chat')
    st.markdown('_Note that chat is presented in reverse order_')

    if prompt := st.text_input('Prompt'):
        answer = ask_about_project(prompt)

    history = retrieve_history()

    # we want to display the newest entries on top
    for chat_entry in reversed(history.entries):
        if chat_entry.role != 'system':
            st.title(chat_entry.role.capitalize())
            st.write(chat_entry.content)


# streamlit run streamlit_frontend.py --browser.serverAddress localhost