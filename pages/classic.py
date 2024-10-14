import streamlit as st
import utils

# Welcome title
st.title("Portrait mode 🎨")

# Upload image
st.session_state, is_file, is_new_image = utils.get_image(st.session_state)
if is_file:
    
    # User settings
    setting, is_small_art, flag_darkmode = utils.create_user_settings()
           
    # Check if the settings changed
    is_new_setting = utils.is_it_new_session_state_value(st.session_state, "setting", setting)
    st.session_state["setting"] = setting
    
    with st.spinner('ASCII in progress...'):

        # Perform ASCII transformation
        if (is_new_setting | is_new_image):
            ascii = utils.transform_image(st.session_state["img"], setting, is_small_art)
            st.session_state["ascii"] = ascii
        ascii = st.session_state["ascii"]

        # Display images        
        if flag_darkmode:
            ascii_to_display = ascii[0]
        else:
            ascii_to_display = ascii[1]    
        if is_small_art:
            _, center, _ = st.columns([2, 3.5, 2])
            center.code(ascii_to_display)
        else:
            st.code(ascii_to_display)      
        