import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/harsha/Downloads/radicalx-428205-b778cce1aff3.json"

project =  "radicalx-428205"
vertexai.init(project=project)
config = generative_models.GenerationConfig(
    temperature=0.4
)
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()
#user_prompt = "Tell me a joke"
#response = chat.send_message(user_prompt)
#print(response)
def llm_function(chat:ChatSession, query):
    # Code for handling messages and displaying them in Streamlit
    response=chat.send_message(query)
    output=response.candidates[0].content.parts[0].text
    with st.chat_message("model"):
        st.markdown(output)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )
st.title("Gemini Explorer")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initial_prompt_sent" not in st.session_state:
    st.session_state.initial_prompt_sent = False
for index, message in enumerate(st.session_state.messages):
    # Code for displaying and loading chat history
    content= Content(
        role=message["role"],
        parts=[ Part.from_text(message["content"])]
    )
    if index!=0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    chat.history.append(content)
# For initial message startup
# if "username_collected" not in st.session_state:
#     st.session_state.username_collected = False

# user_name = st.text_input("enter your name", disabled=st.session_state.initial_prompt_sent)
if len(st.session_state.messages) == 0 :
    user_name = st.text_input("enter your name", disabled=st.session_state.initial_prompt_sent)
    if user_name:
        initial_prompt = f"Hey, {user_name} I'm ReX, your super cool assistant powered by Google Gemini. Let's vibe together with some interactive emoji fun! :sunglasses::call_me_hand:"
        llm_function(chat, initial_prompt)
        st.session_state.initial_prompt_sent = True

query = st.chat_input("Gemini Explorer")  #

if query:
    # Code for processing user input using the llm_function
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)


