import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title='NextPlay',
                   page_icon='🎮',
                   layout="wide")

# DATASETS

l_data = pd.read_csv('data extraction and preprocessing/data3.csv')
l_data.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)

similarity = pickle.load(open('data/similarity.pkl','rb'))



# MAINPAGE

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



# RECOMMENDATION

st.write("<h4>Choose games here</h4>", unsafe_allow_html=True)
        
games = st.multiselect('', l_data['name'], [], key='games')
        
recommed = st.button('Recommend')
col1,col2 = st.columns(2)

if recommed:
    top_recommendations = []

    for game in games:
        index = l_data[l_data['name'] == game].index[0]
        top_six = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[1:7]
        top_recommendations.extend([top_six[i][0] for i in range(len(top_six))]) 

    top_recommendations = list(set(top_recommendations))[:6]
            
    for i, k in enumerate(top_recommendations):
        if i % 2 == 0:
            with col1:
                st.markdown("""
                            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                            <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                            <div style="text-align: center;">
                                <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                                <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                            </div>
                            </div>
                            """.format(link=l_data["Steam Page"][k], image=l_data["header_image"][k], name=l_data["name"][k], developer=l_data['developer'][k]), unsafe_allow_html=True)
        else:
            with col2:
                st.markdown("""
                            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                            <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                            <div style="text-align: center;">
                                <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                                <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                            </div>
                            </div>
                            """.format(link=l_data["Steam Page"][k], image=l_data["header_image"][k], name=l_data["name"][k], developer=l_data['developer'][k]), unsafe_allow_html=True)
 


# SIDEBAR
# sidebar.instructions
st.sidebar.header("Set of instructions 🙂")

st.sidebar.markdown("1. Choose a game from the dropdown menu.")
st.sidebar.markdown("2. Click the 'Recommend' button.")
st.sidebar.markdown("3. Explore the recommended games.")
st.sidebar.markdown("4. Click on image to visit Steam page. ")
st.sidebar.markdown("5. Enjoy!")

st.sidebar.markdown('---')

# sidebar.tags
for game in games:
    selected_game_categories = l_data.loc[l_data['name'] == game, 'Tags'].iloc[0]
    
    if selected_game_categories:
        st.sidebar.subheader(f"The chosen game '{game}' belongs to:")
        categories_list = selected_game_categories.split(',')
        for category in categories_list:
            st.sidebar.write(f"- {category.strip()}")



# TRENDING

st.markdown('---')
  
trending = st.subheader('Trending games')

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
                    st.markdown("""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                        <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                        <div style="text-align: center;">
                            <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                            <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                        </div>
                        </div>
                        """.format(link=l_data["Steam Page"][i], image=l_data["header_image"][i], name=l_data['name'][i], developer=l_data['developer'][i]), unsafe_allow_html=True)
            else:
                with col4:
                    st.markdown("""
                        <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                        <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                        <div style="text-align: center;">
                            <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                            <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                        </div>
                        </div>
                        """.format(link=l_data["Steam Page"][i], image=l_data["header_image"][i], name=l_data['name'][i], developer=l_data['developer'][i]), unsafe_allow_html=True)