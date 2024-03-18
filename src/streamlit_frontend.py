import streamlit as st

from utils.stored_data import retrieve_document, store_document, retrieve_history
from context_creation import ask_about_project, summarize_tech_stack

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([3, 1, 3])

PROJECT_ID = 1


def update_document_callback(document_type: str, project_id: int):
    new_text = st.session_state[document_type]
    store_document(document_type, new_text, project_id)


def updated_plan_callback():
    new_text = st.session_state['plan']
    store_document(document_type='project_plan', document=new_text, project_id=PROJECT_ID)


def updated_requirements_callback():
    new_text = st.session_state['requirements']
    store_document('requirements', new_text, project_id=PROJECT_ID)


with col1:
    st.title('The Project')
    list_of_tabs = ['Requirements', 'Edit requirements', 'Project plan', 'Edit project plan', 'Summary']
    tab1, tab2, tab3, tab4, tab5 = st.tabs(list_of_tabs)

    with tab1:
        st.write(retrieve_document('requirements'))

    with tab2:
        st.text_area(value=retrieve_document('requirements', PROJECT_ID),
                     key='requirements',
                     on_change=update_document_callback,
                     args=('requirements', PROJECT_ID),
                     label='Requirements',
                     height=800)

    with tab3:
        st.write(retrieve_document('project_plan'))

    with tab4:
        st.text_area(value=retrieve_document('project_plan', PROJECT_ID),
                     key='project_plan',
                     on_change=update_document_callback,
                     args=('project_plan', PROJECT_ID),
                     label='Project Plan',
                     height=800)

    with tab5:
        st.title('Tech summary')
        current_summary = retrieve_document('tech_summary', PROJECT_ID)
        st.write(current_summary)

        if st.button('Propose tech summary'):
            proposed_summary = summarize_tech_stack(project_id=PROJECT_ID)
            store_document('tech_summary', proposed_summary, project_id=PROJECT_ID)
            st.title('Proposed tech summary')
            st.write(proposed_summary)


with col3:
    st.title('Chat')
    st.markdown('_Note that chat is presented in reverse order_')

    if prompt := st.text_input('Prompt'):
        answer = ask_about_project(prompt, project_id=PROJECT_ID)

    history = retrieve_history(project_id=PROJECT_ID)

    # we want to display the newest entries on top
    for chat_entry in reversed(history.entries):
        if chat_entry.role != 'system':
            st.title(chat_entry.role.capitalize())
            st.write(chat_entry.content)


# streamlit run streamlit_frontend.py --browser.serverAddress localhost