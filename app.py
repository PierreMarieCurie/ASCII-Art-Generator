import streamlit as st
import sys

PAGE_PATH = "pages"
SOURCE_PATH = "src"
sys.path.append(PAGE_PATH)
    
def learnmorepage():
    st.title("to do")
    
home_page = st.Page(PAGE_PATH + "/home.py", title="Home page", icon=":material/home:")
classic_page = st.Page(PAGE_PATH + "/classic.py", url_path='classic', title="Classic mode", icon=":material/photo_frame:")
portrait_page = st.Page(PAGE_PATH + "/portrait.py", url_path='portrait', title="Portrait mode", icon=":material/person:")
multiportrait_page = st.Page(PAGE_PATH + "/multiportrait.py", url_path='multiportrait', title="Multi-portrait mode", icon=":material/group:")
gallery_page = st.Page(PAGE_PATH + "/gallery.py", url_path='gallery', title="Gallery", icon=":material/gallery_thumbnail:")
learnmore_page = st.Page(learnmorepage, url_path='learnmore', title="Learn more", icon=":material/question_mark:")

pg = st.navigation(
    {
        "Welcome": [home_page],
        "ASCII Tools": [classic_page, portrait_page, multiportrait_page],
        "More": [gallery_page, learnmore_page]
    }
)

st.set_page_config(page_title="ASCII Art Creator",
                   page_icon=":material/edit:",
                   menu_items={
                    'Get Help': 'https://www.extremelycoolapp.com/help',
                    'Report a bug': "https://www.extremelycoolapp.com/bug",
                    'About': "# This is a ASCCI art creator. Have fun with it!"
                    })
pg.run()