import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from backend.model import chatbot
from langchain_core.messages import HumanMessage
import uuid
#####################_Utility_Functions##############################################
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
####################_Session_Setup_##########################################
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}
########################_Side_Bar_#######################################
st.sidebar.title("My Chatbot")
st.sidebar.header('Your Conversations')
if st.sidebar.button('New Chat'):
    reset_chat()

for thread_id in st.session_state['chat_threads']:
    st.sidebar.button(str(thread_id))
###############################################################

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type Your Message.....')

if user_input:

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config = CONFIG)
    # ai_message = response['messages'][-1].content[0]['text']

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.text for message_chunk,metadeta in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ) if message_chunk.text
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})