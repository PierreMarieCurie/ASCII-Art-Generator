import streamlit as st
import utils
import cv2

# Welcome title
st.title("Multiportrait mode 🎨")
        
# Upload image
st.session_state, is_file, is_new_image = utils.get_image(st.session_state)
if is_file:
    
    # User settings
    setting, is_small_art, flag_darkmode = utils.create_user_settings()
           
    # Check if the settings changed
    is_new_setting = utils.is_it_new_session_state_value(st.session_state, "setting", setting)
    st.session_state["setting"] = setting

    # Face detection
    with st.spinner('Face detection...'):
        
        # Perform object detection if new image is provided by the user
        if is_new_image:
            
            # Instance face detector
            face_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            # Pre-process
            gray_image = cv2.cvtColor(st.session_state['img'], cv2.COLOR_RGB2GRAY)            
            
            # Inference on face detection
            st.session_state["faces"] = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))        
        faces = st.session_state["faces"]
        
    # Face segmentation model initializing
    st.session_state = utils.load_face_segmentation_model(st.session_state)
    
    # Face segmentation
    with st.spinner('Segmentation of the faces...'):  

        if is_new_image:
            img_faces = []
            bboxes_faces = []
            dimensions = []
            for i_face, (x, y, w, h) in enumerate(faces):
                
                # Extract face from the original image
                img_face = st.session_state['img'][y:y+h+1, x:x+w+1]
                
                # Extract face parts using segmentation model
                _, _, bboxes, _ = st.session_state['model'].predict(img_face)
                
                # Set the minimal area : from eyebrows to the mouth
                dimension = None
                for i_face_part in [2, 3, 4, 5, 10, 11, 12, 13]:
                    dimension = utils.get_largest_box(dimension, bboxes[i_face_part]) 
            
                # Ignore faces without face part
                if dimension is not None:
                    img_faces.append(img_face)
                    bboxes_faces.append(bboxes)
                    dimensions.append(dimension)
            
            st.session_state["img_faces"] = img_faces
            st.session_state["bboxes_faces"] = bboxes_faces
            st.session_state["dimensions"] = dimensions
            
        img_faces = st.session_state["img_faces"]
        bboxes_faces = st.session_state["bboxes_faces"]
        dimensions = st.session_state["dimensions"]
        
        # No face detected
        N_face = len(dimensions)
        if N_face == 0:
            st.write("No face detected")
        
        else:
            # Get face part asked by the user
            indices_disable = [i_face_part for i_face_part in range(len(bboxes_faces[0])) if all(el[i_face_part] is None for el in bboxes_faces)]
            indices_face_parts = utils.get_face_part_indices(indices_disable)

            # ASCII generation
            with st.spinner('ASCII in progress...'):

                # Get dimensions of the box
                dimensions_after_selection = dimensions.copy()
                for i_face in range(N_face):
                    for indices_face_part in indices_face_parts:
                        dimensions_after_selection[i_face] = utils.get_largest_box(dimensions[i_face], bboxes_faces[i_face][indices_face_part])
                        
                # Reset ASCII if needed
                if (is_new_image | is_new_setting):
                    st.session_state["ascii"] = [None] * N_face

                # Perform ASCII transformation for each face in the image
                for i_face in range(N_face):
                    
                    # Determine if we compute the ASCII again based on current and previous box dimensions and settings
                    if (is_new_image | is_new_setting):
                        flag_ascii = True
                    elif "dimensions_after_selection" not in st.session_state:
                        flag_ascii = True
                    elif dimensions_after_selection[i_face] != st.session_state["dimensions_after_selection"][i_face]:
                        flag_ascii = True
                    else:
                        flag_ascii = False

                    if flag_ascii:
                        # Crop the image
                        im_cut = img_faces[i_face][dimensions_after_selection[i_face][1]:dimensions_after_selection[i_face][3]+1, dimensions_after_selection[i_face][0]:dimensions_after_selection[i_face][2]+1]

                        # ASCII
                        ascii = utils.transform_image(im_cut, setting, is_small_art)
                        st.session_state["ascii"][i_face] = ascii
                
                st.session_state["dimensions_after_selection"] = dimensions_after_selection                

                # Display images
                for i_face in range(N_face):    
                    
                    img_plot = st.session_state["img_faces"][i_face].copy()
                    cv2.rectangle(img_plot,
                                  (dimensions_after_selection[i_face][0], dimensions_after_selection[i_face][1]),
                                  (dimensions_after_selection[i_face][2], dimensions_after_selection[i_face][3]),
                                  (255, 0, 0), 2)
                    if flag_darkmode:
                        ascii_to_display = st.session_state["ascii"][i_face][0]
                    else:
                        ascii_to_display = st.session_state["ascii"][i_face][1]    
                    left, right = st.columns(2, vertical_alignment="center")
                    left.image(img_plot, use_column_width=True)
                    right.code(ascii_to_display)