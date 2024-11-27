import streamlit as st
import sys

PAGE_PATH = "pages"
sys.path.append(PAGE_PATH)

#import torch
#state_dict = torch.load('/home/t0192782/perso/ASCII-Art-Generator/weights/face_parsing.pth', map_location="cpu")
#for key, value in state_dict.items():
#    print(f"{key}: {value.device}")

#/home/t0192782/perso/ASCII-Art-Generator/weights/face_parsing.pth

home_page = st.Page(PAGE_PATH + "/home.py", title="Home page", icon=":material/home:")
classic_page = st.Page(PAGE_PATH + "/classic.py", url_path='classic', title="Classic mode", icon=":material/photo_frame:")
portrait_page = st.Page(PAGE_PATH + "/portrait.py", url_path='portrait', title="Portrait mode", icon=":material/person:")
multiportrait_page = st.Page(PAGE_PATH + "/multiportrait.py", url_path='multiportrait', title="Multi-portrait mode", icon=":material/group:")
gallery_page = st.Page(PAGE_PATH + "/gallery.py", url_path='gallery', title="Gallery", icon=":material/gallery_thumbnail:")
reference_page = st.Page(PAGE_PATH + "/reference.py", url_path='reference', title="Reference", icon=":material/question_mark:")

pg = st.navigation(
    {
        "Welcome": [home_page],
        "ASCII Tools": [classic_page, portrait_page, multiportrait_page],
        "More": [gallery_page, reference_page]
    }
)

st.set_page_config(page_title="ASCII Art Creator",
                   page_icon=":material/edit:",
                   menu_items={
                    'Get Help': 'https://github.com/PierreMarieCurie/ASCII-Art-Generator',
                    'Report a bug': "https://github.com/PierreMarieCurie/ASCII-Art-Generator/issues",
                    'About': "# This is a ASCCI art creator. Have fun with it!"
                    })
pg.run()