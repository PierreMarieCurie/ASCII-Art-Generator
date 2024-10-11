import streamlit as st
import utils
import cv2

# Welcome title
st.title("Portrait mode 🎨")
        
# Upload image
uploaded_file = st.file_uploader("Upload an Image", type=utils.ALLOWED_EXTENSIONS, label_visibility='hidden')
if uploaded_file is not None:
    st.session_state, is_new_image = utils.load_image(uploaded_file, st.session_state)
    
    # User settings
    setting, flag_small_art, flag_darkmode = utils.create_user_settings()
           
    # Check if the settings changed
    is_new_setting = utils.is_it_new_session_state_value(st.session_state, "setting", setting)
    st.session_state["setting"] = setting

    # Face segmentation model initializing
    st.session_state = utils.load_face_segmentation_model(st.session_state)

    with st.spinner('ASCII in progress...'):

        # Extract face parts from the images
        _, masks, bboxes, face_parts = st.session_state['model'].predict(st.session_state['img'])

        # Set the minimal area : from eyebrows to the mouth
        dimension = None
        for i_face_part in [2, 3, 4, 5, 10, 11, 12, 13]:
            dimension = utils.get_largest_box(dimension, bboxes[i_face_part])
        
        # No face detected
        if dimension is None:
            st.write("No face detected")
        
        else:        
            # User choice for background, left ear, right ear, neck, clothes
            face_toggles = [[]] * 7
            for i, i_face_part in enumerate([0, 1, 7, 8, 14, 16, 17]):
                face_toggles[i], dimension = utils.get_new_dimension_from_toggle(dimension, bboxes[i_face_part], face_parts[i_face_part])
            is_new_face_parts = True
        
            is_new_face_part = utils.is_it_new_session_state_value(st.session_state, "face_toggles", face_toggles)
            st.session_state["face_toggles"] = face_toggles
        
            # Reshape the image
            im_cut = st.session_state["img"][dimension[1]:dimension[3]+1, dimension[0]:dimension[2]+1]

            # Perform ASCII transformation
            if (is_new_setting | is_new_image | is_new_face_parts):
                ascii = utils.transform_image(im_cut, setting, flag_small_art)
                st.session_state["ascii"] = ascii
            ascii = st.session_state["ascii"]            
            
            # Display images
            img_plot = st.session_state['img'].copy()
            cv2.rectangle(img_plot, (dimension[0], dimension[1]), (dimension[2], dimension[3]), (255, 0, 0), 2)
            utils.display_images(img_plot, ascii, flag_small_art, flag_darkmode)