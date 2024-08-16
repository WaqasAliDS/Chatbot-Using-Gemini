import streamlit as st
import google.generativeai as genai

# Configure the API key
api_key = "AIzaSyDSbi754tXuuMbH5_oi5vRQBTVPAmpiJy4"
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(conversation_context):
    """Generate a response from the Gemini model using the conversation context."""
    response = model.generate_content([conversation_context])
    return response.text

# Streamlit app setup
st.title("Conversational Chatbot")

# Initialize session state variables to maintain conversation context and user's name
if 'conversation_context' not in st.session_state:
    st.session_state.conversation_context = ""

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Display a text input widget for the user to type their message
user_input = st.text_input("You: ", "")

if st.button("Send") and user_input:
    if st.session_state.user_name is None:
        # If the user's name has not been provided yet
        if user_input.lower() in ['hi', 'hello', 'hey']:
            response = "Hello there! It's nice to meet you. What's your name?"
            st.session_state.conversation_context += f"You: {user_input}\nChatbot: {response}\n"
        else:
            # The user provides their name
            st.session_state.user_name = user_input
            response = f"Hello there! It's nice to meet you, {st.session_state.user_name}. I'm ready to chat and answer any questions you might have."
            st.session_state.conversation_context += f"You: {user_input}\nChatbot: {response}\n"
    else:
        # Once the user's name is known, include the context in the prompt to the model
        conversational_prompt = f"{st.session_state.conversation_context}You: {user_input}\nChatbot:"
        response = get_gemini_response(conversational_prompt)
        st.session_state.conversation_context += f"You: {user_input}\nChatbot: {response}\n"

    # Display the conversation context
    st.text_area("Conversation", value=st.session_state.conversation_context, height=400, max_chars=None)

    # Clear the input after sending the message
    #st.text_input("You: ", "", key="input_clear")

if st.button("Reset Chat"):
    # Clear conversation and reset state
    st.session_state.conversation_context = ""
    st.session_state.user_name = None
    st.experimental_rerun()
