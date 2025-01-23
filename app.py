from openai import OpenAI
import streamlit as st


#streamlit/style.css 파일 열기
with open("./style.css") as css:
    # CSS 파일을 읽어와서 스타일 적용
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("## Chatbot for Academic Stress Assessment💭", unsafe_allow_html=True)

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
        {"role": "assistant", "content": f"Nice to meet you! I'm Jessica😊"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.conversation_history:        
    if message["role"] == 'system':
        continue
    formatted_message = f"<b>{message['content']}</b>"  # 메시지를 볼드체로 변경
    st.markdown(formatted_message, unsafe_allow_html=True)  # HTML로 렌더링


if user_input := st.chat_input():            
    # Add user message to chat history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    formatted_user_input = f"<b>{user_input}</b>"  # 사용자 입력을 볼드체로 변경
    st.markdown(formatted_user_input, unsafe_allow_html=True)
    
    with st.spinner('Yeonwoo is typing...'):
        # response generation
        response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.conversation_history,
            max_tokens=1000,
            temperature=0.7,      
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        formatted_assistant_reply = f"<b>{assistant_reply}</b>"  # 챗봇 응답을 볼드체로 변경
        st.markdown(formatted_assistant_reply, unsafe_allow_html=True)

        
