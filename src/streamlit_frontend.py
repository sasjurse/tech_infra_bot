import streamlit as st

from utils.stored_data import retrieve_current_plan
from context_creation import ask_about_project

tab1, tab2 = st.tabs(['Project plan', 'Chat'])


with tab1:
    st.title('Project plan')
    st.write(retrieve_current_plan())

with tab2:
    st.title('Chat')

    if prompt := st.text_input('Prompt'):
        answer = ask_about_project(prompt)
        st.title('You wrote')
        st.write(prompt)
        st.title('Assistant answered')
        st.write(answer)



# streamlit run streamlit_frontend.py --browser.serverAddress localhost