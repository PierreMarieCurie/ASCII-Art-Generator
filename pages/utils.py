import streamlit as st
from PIL import Image
import numpy as np
import cv2
from src import ascii, dither
from src.face_segmentation import FaceSegmentation
import torch

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pbm', 'tiff', 'tif', 'bmp'}  # Define allowed file extensions

def load_image(file, session_state):
    
    # Check is we need to load the image again
    is_new_image = is_it_new_session_state_value(session_state, "file_id", file.file_id)
    session_state["file_id"] = file.file_id

    # Load the image
    if is_new_image:
    
        # Load the image into a numpy array
        img_array = np.array(Image.open(file))

        # Check if the image has 4 channels (RGBA), if so, remove the alpha channel
        if img_array.shape[-1] == 4:
            img_array = img_array[:, :, :3]  # Keep only the first 3 channels (RGB)
        
        # Save image
        session_state['img'] = img_array
        
    return session_state, is_new_image

def get_image(session_state):
    with st.container(border=True):
        col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center")    
        is_file = col1.file_uploader("Upload an Image", type=ALLOWED_EXTENSIONS, label_visibility="collapsed")

    is_new_image = False
    if is_file is not None:
        st.session_state, is_new_image = load_image(is_file, session_state)
        col2.image(st.session_state["img"])

    return session_state, is_file, is_new_image

def create_user_settings():
    with st.container(border=True):        
        # Small art
        col1, col2, col3 = st.columns([0.02, 0.2, 0.76], vertical_alignment="center")
        is_small_art = col2.toggle("Small art", False)
        
        # Size of the ASCII art
        new_width = col3.slider("Select a size", 80, 400, 100, disabled=is_small_art)
        
        # Select an algorithm            
        algorithm = st.selectbox('Select an algorithm',
                                    ["Thresholding", 'Floyd-Steinberg', 'Atkinson'],
                                    index=1,
                                    help="Floyd-Steinberg and Atkinson algorithms refine local contrast better than Thresholding but take longer to compute and need large images",
                                    disabled=is_small_art)
        if is_small_art:
            algorithm = "Thresholding"
            
        # Threshold values
        min_value, max_value, step, default_value = 0.3, 0.7, 0.02, 0.5
        if algorithm != "Thresholding":
            min_value, max_value, step, default_value = 8, 32, 2, 16

        # Slider to select the threshold
        col1, col2, col3 = st.columns([0.75, 0.02, 0.23], vertical_alignment="center")
        threshold = col1.slider("Select a threshold", min_value, max_value, default_value, step)

        # Toggle to select darkmode or not
        flag_darkmode = col3.toggle("Darkmode", True)
        
        return {'new_width':new_width, 'algorithm':algorithm, 'threshold':threshold}, is_small_art, flag_darkmode

def is_it_new_session_state_value(session_state, key, value):
    is_new = False
    if key not in session_state:
        is_new = True
    elif session_state[key] != value:
        is_new = True
    return is_new

def transform_image(img, setting, is_small_art):
    im_grey = ascii.preprocess_image(img)
        
    # Set shape of ASCII according to user parameter
    if is_small_art:
        new_shape = ascii.get_max_shape(im_grey.shape)
    else:
        new_shape = ascii.get_new_shape_with_width(im_grey.shape, setting["new_width"])
    
    # Pre-process : resize and change data type
    im_grey = cv2.resize(im_grey, (new_shape[::-1]), interpolation=cv2.INTER_AREA)    
    data = im_grey.astype(np.float32)/255
    
    # ASCII process
    algorithm = setting["algorithm"]
    threshold = setting["threshold"]
    if algorithm == "Thresholding":
        img_final = (data > threshold).astype(int)
    elif algorithm == 'Floyd-Steinberg':
        img_final = dither.floyd_steinberg(data, threshold)
    elif algorithm == 'Atkinson':
        img_final = dither.atkinson(data, threshold)

    # Convert binary image to ASCII made of braille characters
    ascii_darkmode = ascii.convert_array_to_braille_characters(img_final)
    ascii_whitmode = ascii.convert_array_to_braille_characters(1-img_final)
    
    return ascii_darkmode, ascii_whitmode

def load_face_segmentation_model(session_state):
    if 'model' not in session_state:
        with st.spinner("Face segmentation model initializing..."):
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            session_state['model'] = FaceSegmentation(device)
            session_state["device"] = device
    
    return session_state    
                    
def get_largest_box(box1, box2):
    if box1 is None:
        return box2
    elif box2 is None:
        return box1
    else:
        return [min(box1[0], box2[0]),
                min(box1[1], box2[1]),
                max(box1[2], box2[2]),
                max(box1[3], box2[3])]

def get_face_part_indices(face_part_map, indices_disable):
    indices = []
    with st.container(border=True):
        cols = st.columns(len(face_part_map), vertical_alignment="top")
        for index_col, (name, indices_face_part) in enumerate(face_part_map.items()):
            cols[index_col].write(name)
            disable = all([index_face_part in indices_disable for index_face_part in indices_face_part])
            _, c = cols[index_col].columns([1, 500])
            if c.toggle(label=str(index_col), value=False, disabled=disable, label_visibility="hidden"):
                for index_face_part in indices_face_part:
                    indices.append(index_face_part)
    return indices