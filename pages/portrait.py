import streamlit as st
import utils
import cv2

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

    # Face segmentation model initializing
    st.session_state = utils.load_face_segmentation_model(st.session_state)

    with st.spinner('ASCII in progress...'):

        # Extract face parts from the images
        _, masks, bboxes, _ = st.session_state['model'].predict(st.session_state['img'])

        # Set the minimal area : from eyebrows to the mouth
        dimension = None
        for i_face_part in [2, 3, 4, 5, 10, 11, 12, 13]:
            dimension = utils.get_largest_box(dimension, bboxes[i_face_part])
        
        # No face detected
        if dimension is None:
            st.write("No face detected")
        
        else:
            # Face parts for the user to choose
            face_part_map = {
                'Face 🦲':[1],
                'Ears 👂':[7, 8],
                'Clothes 👔':[16],
                'Hair 🦱':[17],
                'Background :material/background_replace:':[0]}

            # Get face part asked by the user
            indices_disable = [i for i, box in enumerate(bboxes) if box is None]
            indices_face_parts = utils.get_face_part_indices(face_part_map, indices_disable)
            for i in indices_face_parts:
                dimension = utils.get_largest_box(dimension, bboxes[i])
            
            is_new_dimension = utils.is_it_new_session_state_value(st.session_state, "dimension", dimension)        
            st.session_state["dimension"] = dimension
            
            # Reshape the image
            im_cut = st.session_state["img"][dimension[1]:dimension[3]+1, dimension[0]:dimension[2]+1]

            # Perform ASCII transformation
            if (is_new_setting | is_new_image | is_new_dimension):
                ascii = utils.transform_image(im_cut, setting, is_small_art)
                st.session_state["ascii"] = ascii
            ascii = st.session_state["ascii"]            
            
            # Display images
            img_plot = st.session_state['img'].copy()
            cv2.rectangle(img_plot, (dimension[0], dimension[1]), (dimension[2], dimension[3]), (255, 0, 0), 2)
            if flag_darkmode:
                ascii_to_display = ascii[0]
            else:
                ascii_to_display = ascii[1]    
            left, right = st.columns(2)
            left.image(img_plot)
            right.code(ascii_to_display)

