import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title='NextPlay', page_icon='🎮', layout="wide")

# Load datasets
l_data = pd.read_csv('data extraction and preprocessing/data3.csv')
l_data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

# Session state to check if user data is submitted
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'guardian_confirmed' not in st.session_state:
    st.session_state.guardian_confirmed = False

# Function to display the main page
def display_main_page():
    st.title('🎮 NextPlay 🎮')

    st.write("Imagine you're wandering through a vast library of games, and suddenly, a quirky little friend pops up, saying, ")

    st.markdown("""<div style="text-align: center;">
                        <p><em><strong>"Hey there! Feeling lost in this jungle of pixels? Let me be your guide!"</strong></em></p>
                    </div>
                """, unsafe_allow_html=True)

    st.write("That's what a game recommender system is like—it's your trusty sidekick in the world of gaming, "
             "helping you find the perfect game without getting lost in the maze of choices."
             " Think of it as your own personal game genie 🧞‍♂️, but instead of granting wishes, it grants you "
             "hours of entertainment and fun! It's like having a friend who knows you better than you know "
             "yourself when it comes to gaming...")

    st.write("\nSo, next time you're scratching your head, wondering what "
             "game to play next, just come here and follow the set of instructions on the sidebar!")

    st.write("<h4>Recommended games based on your preferences</h4>", unsafe_allow_html=True)
    
    # Iterate through each preference and display relevant games
    for preference in st.session_state.preferences:
        st.write(f"### {preference} Games:")
        filtered_games = l_data[l_data['Tags'].str.contains(preference, case=False, na=False)]

        if not filtered_games.empty:
            col1, col2 = st.columns(2)
            for i, row in filtered_games.head(4).iterrows():
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                        <a href="{row['Steam Page']}" target="_blank"><img src="{row['header_image']}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                        <div style="text-align: center;">
                            <p style="margin: 0; font-size: 20px;"><b>Title: </b>{row['name']}</p>
                            <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{row['developer']}</p>
                        </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("No games available for this category.")

    # Sidebar instructions
    st.sidebar.header("Set of instructions 🙂")
    st.sidebar.markdown("1. Choose a game from the dropdown menu.")
    st.sidebar.markdown("2. Click the 'Recommend' button.")
    st.sidebar.markdown("3. Explore the recommended games.")
    st.sidebar.markdown("4. Click on image to visit Steam page. ")
    st.sidebar.markdown("5. Enjoy!")
    st.sidebar.markdown('---')

    # Sidebar tags
    st.write("<h4>Choose games here</h4>", unsafe_allow_html=True)

    games = st.multiselect('', l_data['name'], [], key='games')

    recommed = st.button('Recommend')
    col1, col2 = st.columns(2)

    if recommed:
        top_recommendations = []

        for game in games:
            index = l_data[l_data['name'] == game].index[0]
            top_six = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:7]
            top_recommendations.extend([top_six[i][0] for i in range(len(top_six))])

        top_recommendations = list(set(top_recommendations))[:6]

        for i, k in enumerate(top_recommendations):
            if i % 2 == 0:
                with col1:
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                        <a href="{l_data['Steam Page'][k]}" target="_blank"><img src="{l_data['header_image'][k]}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                        <div style="text-align: center;">
                            <p style="margin: 0; font-size: 20px;"><b>Title: </b>{l_data['name'][k]}</p>
                            <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{l_data['developer'][k]}</p>
                        </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                with col2:
                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                        <a href="{l_data['Steam Page'][k]}" target="_blank"><img src="{l_data['header_image'][k]}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                        <div style="text-align: center;">
                            <p style="margin: 0; font-size: 20px;"><b>Title: </b>{l_data['name'][k]}</p>
                            <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{l_data['developer'][k]}</p>
                        </div>
                        </div>
                    """, unsafe_allow_html=True)

    # Trending games section
    st.markdown('---')

    st.subheader('Trending games')

    st.write("**Need a break from reality?** 🙃")

    st.write("\nGames offer the perfect escape! They whisk us away to fantastical realms, where we can "
             "embark on thrilling adventures, solve mind-bending puzzles, or simply unwind after a long day."
             " Whether you're battling dragons in a mythical land or building your dream city from scratch, "
             "games provide a welcome reprieve from the stresses of everyday life. ")

    st.write("\nDive into the world of gaming and discover why millions around the globe turn to Steam for their dose of fun and relaxation. "
             "Check out the trending games on Steam now and treat yourself to some well-deserved entertainment! **Click on the image...**")

    col3, col4 = st.columns(2)
    for i in range(4):
        if i % 2 == 0:
            with col3:
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                    <a href="{l_data['Steam Page'][i]}" target="_blank"><img src="{l_data['header_image'][i]}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 20px;"><b>Title: </b>{l_data['name'][i]}</p>
                        <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{l_data['developer'][i]}</p>
                    </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            with col4:
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                    <a href="{l_data['Steam Page'][i]}" target="_blank"><img src="{l_data['header_image'][i]}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 20px;"><b>Title: </b>{l_data['name'][i]}</p>
                        <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{l_data['developer'][i]}</p>
                    </div>
                    </div>
                """, unsafe_allow_html=True)

# Main logic
if not st.session_state.submitted:
    st.title('Welcome to NextPlay!')
    st.write("Before we get started, we'd like to know a little more about you.")

    with st.form("user_info_form"):
        age = st.number_input("Please enter your age:", min_value=1, max_value=120)
        gaming_hours = st.number_input("How many hours do you spend gaming each week?", min_value=0, max_value=15 if age < 17 else 168)
        
        preferences = st.multiselect(
            "Select your game preferences:",
            ['Action', 'Adventure', 'Action-Adventure', 'Puzzle', 'RPG', 'Shooter', 'Sports', 'Strategy', 'Simulation', 'Casual']
        )
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if age < 14:
                st.write("You must be at least 14 years old to use this platform.")
                st.session_state.submitted = False
                st.session_state.guardian_confirmed = False
            else:
                st.session_state.submitted = True
                st.session_state.age = age
                st.session_state.gaming_hours = gaming_hours
                st.session_state.preferences = preferences
                st.session_state.guardian_confirmed = True
                st.experimental_rerun()

if st.session_state.submitted and st.session_state.guardian_confirmed:
    display_main_page()
