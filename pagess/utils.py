import streamlit as st
from PIL import Image, ImageDraw
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


def create_user_settings():
    with st.container(border=True):        
        # Small art
        col1, col2 = st.columns([0.2, 0.75])
        col1.write("")
        flag_small_art = col1.toggle("Small art", False)
        
        # Size of the ASCII art
        new_width = col2.slider("Select a size", 80, 600, 100, disabled=flag_small_art)
        
        # Select an algorithm            
        algorithm = st.selectbox('Select an algorithm',
                                    ["Thresholding", 'Floyd-Steinberg', 'Atkinson'],
                                    index=1,
                                    help="Floyd-Steinberg and Atkinson algorithms refine local contrast better than Thresholding but take longer to compute",
                                    disabled=flag_small_art)
        if flag_small_art:
            algorithm = "Thresholding"
            
        # Threshold values
        min_value, max_value, step, default_value = 0.3, 0.7, 0.02, 0.5
        if algorithm != "Thresholding":
            min_value, max_value, step, default_value = 8, 32, 2, 16

        # Slider to select the threshold
        col1, _, col2 = st.columns([0.75, 0.05, 0.2])
        threshold = col1.slider("Select a threshold", min_value, max_value, default_value, step)

        # Toggle to select darkmode or not
        col2.write("")
        flag_darkmode = col2.toggle("Darkmode", True)
        
        return {'new_width':new_width, 'algorithm':algorithm, 'threshold':threshold}, flag_small_art, flag_darkmode

def is_it_new_session_state_value(session_state, key, value):
    is_new = False
    if key not in session_state:
        is_new = True
    elif session_state[key] != value:
        is_new = True
    return is_new

def transform_image(img, setting, flag_small_art):
    im_grey = ascii.preprocess_image(img)
        
    # Set shape of ASCII according to user parameter
    if flag_small_art:
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

def display_images(img, ascii, flag_small_art, flag_darkmode):
    if flag_small_art:
        left, right = st.columns(2)
        left.image(img, use_column_width=True)
        if flag_darkmode:
            right.code(ascii[0])  
        else:
            right.code(ascii[1])
    else:
        st.image(img, use_column_width=True)
        if flag_darkmode:
            st.code(ascii[0])
            st.download_button("Download ASCII as a text file", ascii[0], "ASCII.txt")
        else:
            st.code(ascii[1])
            st.download_button("Download ASCII as a text file", ascii[1], "ASCII.txt")
                    
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

def get_new_dimension_from_toggle(dimension, box, face_part):
    disabled = box is None
    toggle = st.toggle(face_part, value=False, disabled=disabled)
    if toggle:
        dimension = get_largest_box(dimension, box)
    return toggle, dimension