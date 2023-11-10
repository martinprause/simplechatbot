#conda --version
#conda info --envs

#pip install openai
#pip install streamlit

from openai import OpenAI
import streamlit as st

import os
APIKEY=os.environ["OPENAI_API_KEY"]


client = OpenAI()

class MyMessage:
    def __init__(self, name, avatar, message):
        self.name = name
        self.avatar = avatar
        self.message = message

def showChatHistory():
    if 'chat_history' in st.session_state:
        for msg in st.session_state.chat_history:
            st.chat_message(msg.name, avatar=msg.avatar).write(msg.message)


def addMessage(msg):
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append(msg)
    else:
        st.session_state.chat_history.append(msg)


def generateMessages(prompt):
    messages=[]
    if 'chat_history' in st.session_state:
        for msg in st.session_state.chat_history:
            m={"role": msg.name, "content": msg.message}
            messages.append(m)
    u={"role": "user", "content": prompt}
    messages.append(u)
    return messages

def getBotResponse(prompt): 
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=generateMessages(prompt)
    )
    return response.choices[0].message.content


def main():
    if APIKEY is None:
        st.write("Please set OPENAI_API_KEY environment variable.")
        return
    st.write("ChatBot")
    reset = st.button("Reset")

    if reset:
        st.session_state.chat_history = []
        st.experimental_rerun()

    showChatHistory()
    
    prompt = st.chat_input("Say something nice to the bot!")

    if prompt:
        addMessage(MyMessage("user", "👩‍💻", prompt))
        addMessage(MyMessage("assistant", "🤖", getBotResponse(prompt)))
        st.experimental_rerun()

if __name__ == "__main__":
    main()