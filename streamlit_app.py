import openai
import os
import re
import streamlit as st

mood = 'humorous'
question_area = 'Cognitive Science'
openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        top_p=0.99,
        temperature=0.99, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def remove_special_strings(text):
        pattern = r'<0x[0-9A-Fa-f]{2}>'
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text


@st.cache_data(show_spinner=False, ttl=180, max_entries=1)
def ask_first_question(mood, question_area, player_name):
    prompt = f'''You are a {mood} moderator. Your job is to lead a conversation to test a player's knowledge in {question_area}, 
            then give the player some final assessments and helpful suggestions. 

            Now player {player_name} just joined, let's start by asking the first question. Please output in nice markdown format.'''

    first_question = get_completion(prompt)
    title = f'Starting session in {question_area}.........'
    text_content = remove_special_strings(first_question)
    styled_box = f"""
        <div style="color: #000080; background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
            <h5 style="color: #000080; margin-bottom: 10px;">{title}</h5>
            <p style="font-size: 16px; line-height: 1.5; text-align: justify;">{text_content}</p>
        </div>
        """

    # Display the styled box using Markdown with HTML
    st.markdown(styled_box, unsafe_allow_html=True)

    # Inject custom CSS for the format of buttons
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 340px; /* Adjust the width */
            height: 50px; /* Adjust the height */
            font-size: 16px; /* Adjust the font size */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    return first_question


@st.cache_data(show_spinner=False, ttl=180, max_entries=1)
def ask_second_question(mood, question_area, first_question, first_answer):
    prompt = f'''You are a {mood} moderator. Your job is to lead a conversation to test a player's knowledge in {question_area}, 
        then give the player some final assessments and helpful suggestions. You already
        asked your first question: {first_question}. And you received the player's answer: {first_answer}

        Now please move on to ask your second question in the area of {question_area}. 
        '''

    second_question = get_completion(prompt)
    text_content = remove_special_strings(second_question)
    styled_box = f"""
                <div style="color: #000080; background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
                    <h5 style="color: #000080; margin-bottom: 10px;">''</h5>
                    <p style="font-size: 16px; line-height: 1.5; text-align: justify;">{text_content}</p>
                </div>
                """

    # Display the styled box using Markdown with HTML
    st.markdown(styled_box, unsafe_allow_html=True)

    # Inject custom CSS for the format of buttons
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 340px; /* Adjust the width */
            height: 50px; /* Adjust the height */
            font-size: 16px; /* Adjust the font size */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    return second_question

@st.cache_data(show_spinner=False, ttl=180, max_entries=1)
def ai_concludes(mood, first_question, first_answer, second_question, second_answer):


        prompt = f'''You are a {mood} moderator. Your job is to lead a conversation to test a player's knowledge in {question_area}, 
        then give the player some final assessments and helpful suggestions. You have already asked the player 2 questions. 
        Your first question: {first_question}. And you received the player's answer to your first question: {first_answer}
        Then, you asked your second question: {second_question}. And you received the player's answer to your second question: {second_answer}

        Now it is time to give the player some final assessments and helpful suggestions. Go ahead.
        '''
        final_words = get_completion(prompt)
        text_content = remove_special_strings(final_words)
        styled_box = f"""
                <div style="color: #000080; background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
                    <h5 style="color: #000080; margin-bottom: 10px;">''</h5>
                    <p style="font-size: 16px; line-height: 1.5; text-align: justify;">{text_content}</p>
                </div>
                """

        # Display the styled box using Markdown with HTML
        st.markdown(styled_box, unsafe_allow_html=True)

        # Inject custom CSS for the format of buttons
        st.markdown(
                """
                <style>
                .stButton > button {
                    width: 340px; /* Adjust the width */
                    height: 50px; /* Adjust the height */
                    font-size: 16px; /* Adjust the font size */
                }
                </style>
                """,
                unsafe_allow_html=True
        )
        return final_words

########################## UI ##########################
# draw the nice header at the top of the page using HTML code
header_html = """
<div style="background-color: #800080; color: #FFF; padding: 8px; text-align: Left;">
    <h1 style="color: #FFF; font-size: 32px;"> Fun In Learning - Powered By GenAI</h1>
    <h3 style="color: #FFF; font-size: 20px;"> * Application developed by Oliver Ouyang. All questions and comments generated are automated by AI; humans assume no responsibility:)</h3>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)# Add a header using HTML
st.title(f'Let The Fun Begin!')
st.write("")    # Empty line

# ############################# First Question ############################################
form = st.form(key="start")
# mood = form.text_input('How Are You Feeling Right Now?', key='mood', value='humorous')

player_name = form.text_input('What is Your Name?', key='player_name')
question_area = form.text_input('What Area Are You Interested In Exploring?', key='question_area')
player_name_button = form.form_submit_button('Start Game')
if st.session_state.get('player_name_button') != True:
        st.session_state['player_name_button'] = player_name_button
if st.session_state['player_name_button'] == True:
        first_question = ask_first_question(mood, question_area, player_name)

        ############################# Player Answers First Question; AI Asks Second Question ##############
        st.write("")  # Empty line
        first_answer = st.text_input(f"{player_name}, Enter Your First Answer")
        first_answer_button = st.button('Submit Your First Answer')

        if st.session_state.get('first_answer_button') != True:
                st.session_state['first_answer_button'] = first_answer_button

        if st.session_state['first_answer_button'] == True:
                second_question = ask_second_question(mood, question_area, first_question, first_answer)

                ############################# Player Answers Second Question; AI Concludes ##############
                st.write("")  # Empty line
                second_answer = st.text_input(f"{player_name}, Enter Your Second Answer")
                second_answer_button = st.button('Submit Your Second Answer')

                if st.session_state.get('second_answer_button') != True:
                        st.session_state['second_answer_button'] = second_answer_button

                if st.session_state['second_answer_button'] == True:
                        final_words = ai_concludes(mood, first_question, first_answer, second_question, second_answer)
