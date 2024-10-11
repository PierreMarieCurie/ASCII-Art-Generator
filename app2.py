import streamlit as st
import sys

PAGE_PATH = "pagess"
SOURCE_PATH = "src"
sys.path.append(PAGE_PATH)

def multiportraitpage():
    st.title("hehe")
    
def to_do():
    st.title("blabla")
    
home_page = st.Page(PAGE_PATH + "/home.py", title="Home page", icon=":material/home:")
classic_page = st.Page(PAGE_PATH + "/classic.py", url_path='classic', title="Classic mode", icon=":material/photo_frame:")
portrait_page = st.Page(PAGE_PATH + "/portrait.py", url_path='portrait', title="Portait mode", icon=":material/face:")
multiportrait_page = st.Page(multiportraitpage, url_path='multiportrait', title="Multi-portrait mode", icon=":material/group:")
more_page = st.Page(to_do, url_path='tttt', title="to to", icon=":material/face:")


pg = st.navigation(
    {
        "Home page": [home_page],
        "ASCII Tools": [classic_page, portrait_page, multiportrait_page],
        "Ressources": [more_page]
    }
)
    
st.set_page_config(page_title="ASCII Art Creator", page_icon=":material/edit:")
pg.run()