import streamlit as st
import utils

# Welcome title
st.title("Classic mode 🎨")

# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=utils.ALLOWED_EXTENSIONS, label_visibility='hidden')
if uploaded_file is not None:
    st.session_state, is_new_image = utils.load_image(uploaded_file, st.session_state)
    
    # User settings
    setting, flag_small_art, flag_darkmode = utils.create_user_settings()
           
    # Check if the settings changed
    is_new_setting = utils.is_it_new_session_state_value(st.session_state, "setting", setting)
    st.session_state["setting"] = setting
    
    with st.spinner('ASCII in progress...'):

        # Perform ASCII transformation
        if (is_new_setting | is_new_image):
            ascii = utils.transform_image(st.session_state["img"], setting, flag_small_art)
            st.session_state["ascii"] = ascii
        ascii = st.session_state["ascii"]

        # Display images        
        utils.display_images(st.session_state['img'], ascii, flag_small_art, flag_darkmode)        
        