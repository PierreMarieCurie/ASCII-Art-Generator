import streamlit as st
from PIL import Image
from src import tools
from src import dither
import numpy as np
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pbm', 'tiff', 'tif', 'bmp'}  # Define allowed file extensions
MAX_WIDTH = 1120

st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
        color: white; /* Optional: to match dark mode */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
def main():
    
    # Create title
    st.markdown("<h1 style='text-align: center; color: white;'>ASCII art creator</h1>", unsafe_allow_html=True)

    # Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=ALLOWED_EXTENSIONS, label_visibility='hidden')
    
    if uploaded_file is not None:
        
        im_pillow = Image.open(uploaded_file)
        im_array = np.array(im_pillow)
        
        # User selection
        with st.container(border=True):
            
            option = st.selectbox(
                "Select ASCII mode",
                ("Small Art", "Human faces", "Huge Art")
                )
            
            col1, col2 = st.columns([0.8, 0.2])

            # Slider to select the threshold
            col1.markdown('<div class="centered-text">Select a threshold</div>', unsafe_allow_html=True)
            col1.write("")
            if option == "Huge Art":
                min_value=4
                max_value=30
                step=2
                default_value=16
            else:
                min_value=0.1
                max_value=0.9
                step=0.05
                default_value=0.5
            threshold = col1.slider("Select a threshold",
                                    min_value=min_value,
                                    max_value=max_value,
                                    step=step,
                                    value=default_value,
                                    label_visibility="collapsed"
                                    )

            # Toggle to select darkmode or not
            col2.markdown('<div class="centered-text">Darkmode</div>', unsafe_allow_html=True)
            col2.write("")
            _, center_col, _ = col2.columns(3)
            flag_darkmode = center_col.toggle("Darmode",
                                            value=True,
                                            label_visibility="collapsed")

        with st.spinner('ASCII in progress...'):
            
            im_grey = tools.preprocess_image(im_array)        
                
            if option == "Small Art":
                new_shape = tools.get_max_shape(im_grey.shape)
                im_grey = cv2.resize(im_grey, (new_shape[::-1]))
                
            elif option == "Huge Art":
                im_grey = tools.resize_image_with_fixed_width(im_grey, MAX_WIDTH)
                
            elif option == 'Human faces':
                face_classifier = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )
                gray_image = tools.convert_to_gray(im_array)
                faces = face_classifier.detectMultiScale(gray_image, 1.1, 5)
                            
            data = im_grey.astype(np.float32)/255
            
            if option == "Small Art":
                img_final = (data > threshold).astype(int)
                
                ascii_darkmode = tools.convert_array_to_braille_characters(img_final)
                ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final)
                left, right = st.columns(2)
                left.image(im_pillow, use_column_width=True)
                if flag_darkmode:
                    right.code(ascii_darkmode)  
                else:
                    right.code(ascii_whitmode)
            elif option == 'Human faces':
                
                im_display = im_array.copy()
                for (x, y, w, h) in faces:
                    cv2.rectangle(im_display, (x, y), (x + w, y + h), (255, 0, 0), 4)
                st.image(im_display, use_column_width=True)
                
                left, right = st.columns(2)
                for i, (x, y, w, h) in enumerate(faces):
                    im_grey_face = tools.preprocess_image(im_array[y:y+h, x:x+w])   
                    new_shape = tools.get_max_shape(im_grey_face.shape)
                    im_grey_face = cv2.resize(im_grey_face, (new_shape[::-1]))
                    data_face = im_grey_face.astype(np.float32)/255
                    img_final_face = (data_face > threshold).astype(int)
                
                    ascii_darkmode = tools.convert_array_to_braille_characters(img_final_face)
                    ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final_face)
                    
                    if i%2:
                        if flag_darkmode:
                            left.code(ascii_darkmode)
                        else:
                            left.code(ascii_whitmode)
                    else:
                        if flag_darkmode:
                            right.code(ascii_darkmode)
                        else:
                            right.code(ascii_whitmode)                      
                    
            elif option == "Huge Art":
                img_final = dither.floyd_steinberg(data, threshold)
                ascii_darkmode = tools.convert_array_to_braille_characters(img_final)
                ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final)
                st.image(im_pillow, use_column_width=True)
                if flag_darkmode:
                    st.code(ascii_darkmode)
                else:
                    st.code(ascii_whitmode)
            else:
                st.write("to do")

if __name__ == "__main__":
    main()