from openai import OpenAI
import streamlit as st


#streamlit/style.css 파일 열기
with open("./style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("# Chatbot for Academic Stress Assessment💭", unsafe_allow_html=True)

# Set a default model
if "openai_model" not in st.session_state:    
    st.session_state["openai_model"] = "gpt-4o"

# Set OpenAI API key 
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
                organization=st.secrets['OPENAI_ORGANIZATION'])
openai_api_key = st.secrets['OPENAI_API_KEY']

# Initialize chat history
if "conversation_history" not in st.session_state:    
    st.session_state.conversation_history = [
        {"role": "system", "content": st.secrets['system_prompt']},
        {"role": "assistant", "content": f"Nice to meet you! I'm Yeonwoo😊"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.conversation_history:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 

if user_input := st.chat_input():            
    #Add user message to chat history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)      
    with st.spinner('Yeonwoo is typing...'):
        #response generation
        response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.conversation_history,
            #stream=True,
            max_tokens=1000,
            temperature=0.7,      
            )
        assistant_reply = response.choices[0].message.content
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.chat_message("assistant").write(assistant_reply)     
        
