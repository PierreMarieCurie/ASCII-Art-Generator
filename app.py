import streamlit as st
from PIL import Image
from src import tools
from src import dither
import numpy as np
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pbm', 'tiff', 'tif', 'bmp'}  # Define allowed file extensions

st.markdown("""<style>.centered-text {text-align: center; color: white;}</style>""", unsafe_allow_html=True)

# Streamlit app
def main():
    
    # Create title
    st.markdown("<h1 class='centered-text'>ASCII art creator</h1>", unsafe_allow_html=True)

    # Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=ALLOWED_EXTENSIONS, label_visibility='hidden')
    
    if uploaded_file is not None:
        
        # Load image
        im_pillow = Image.open(uploaded_file)
        im_array = np.array(im_pillow)
        
        # User selection
        with st.container(border=True):
            
            option = st.selectbox("Select ASCII mode", ("Normal", "Human faces"), help="to do")
            
            # Size of the ASCII art
            if option == "Normal":                
                _, large_center, _, = st.columns([0.05, 0.9, 0.05])
                large_center.markdown('<div class="centered-text">Select a size</div>', unsafe_allow_html=True)
                size_user = large_center.select_slider("Size slider", ["Small", "Medium", "Large", "Insane"], value="Small", label_visibility="collapsed")

            # Select an algorithm            
            algorithm = "Thresholding"
            if option=="Normal":
                if size_user != "Small":
                    large_center.markdown('<div class="centered-text">Select an algorithm</div>', unsafe_allow_html=True)
                    algorithm = large_center.selectbox('Select an algorithm', ["Thresholding", 'Floyd-Steinberg', 'Atkinson'], index=1, help="to do", label_visibility="collapsed")             
               
            # Threshold values
            min_value, max_value, step, default_value = 0.3, 0.7, 0.02, 0.5
            if algorithm != "Thresholding":
                min_value, max_value, step, default_value = 8, 32, 2, 16

            # Slider to select the threshold
            st.write("")
            _, col2, col3 = st.columns([0.05, 0.75, 0.2])
            col2.markdown('<div class="centered-text">Select a threshold</div>', unsafe_allow_html=True)
            col2.write("")
            threshold = col2.slider("Select a threshold", min_value, max_value, default_value, step, label_visibility="collapsed")

            # Toggle to select darkmode or not
            col3.markdown('<div class="centered-text">Darkmode</div>', unsafe_allow_html=True)
            col3.write("")
            _, center_col, _ = col3.columns(3)
            flag_darkmode = center_col.toggle("Darmode", True, label_visibility="collapsed")

        with st.spinner('ASCII in progress...'):
            
            im_grey = tools.preprocess_image(im_array)        
            
            if option == "Normal":
                
                # Set shape of ASCII according to user parameter
                new_shape = tools.get_max_shape(im_grey.shape)
                if size_user != "Small":
                    if size_user == "Medium":
                        new_shape = tools.increase_shape(new_shape, 3)
                    elif size_user == "Large":
                        new_shape = tools.increase_shape(new_shape, 5)
                    elif size_user == "Insane":
                        new_shape = tools.increase_shape(new_shape, 15)
                    else:
                        st.write("Size not recognized")
                
                # Pre-process : resize and change data type
                im_grey = cv2.resize(im_grey, (new_shape[::-1]))    
                data = im_grey.astype(np.float32)/255
                
                # Algorithm (Thresholding or dithering)
                if algorithm == "Thresholding":
                    img_final = (data > threshold).astype(int)
                elif algorithm == 'Floyd-Steinberg':
                    img_final = dither.floyd_steinberg(data, threshold)
                elif algorithm == 'Atkinson':
                    img_final = dither.atkinson(data, threshold)
                else:
                    st.write("Unknow algorithm... see source code")
                
                # Convert binary image to ASCII made of braille characters
                ascii_darkmode = tools.convert_array_to_braille_characters(img_final)
                ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final)
                    
                if size_user == "Small":
                    left, right = st.columns(2)
                    left.image(im_pillow, use_column_width=True)
                    if flag_darkmode:
                        right.code(ascii_darkmode)  
                    else:
                        right.code(ascii_whitmode)
                else:
                    st.image(im_pillow, use_column_width=True)
                    if flag_darkmode:
                        st.code(ascii_darkmode)
                        st.download_button("Download ASCII as a text file", ascii_darkmode, "toto.txt")
                    else:
                        st.code(ascii_whitmode)
                        st.download_button("Download ASCII as a text file", ascii_whitmode, "ASCII.txt")
            
            elif option == 'Human faces':
                face_classifier = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )
                gray_image = tools.convert_to_gray(im_array)
                faces = face_classifier.detectMultiScale(gray_image, 1.1, 5)
                            
                data = im_grey.astype(np.float32)/255
                
                im_display = im_array.copy()
                for (x, y, w, h) in faces:
                    cv2.rectangle(im_display, (x, y), (x + w, y + h), (200, 0, 0), 2)
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
                            right.code(ascii_darkmode)
                        else:
                            right.code(ascii_whitmode)
                    else:
                        if flag_darkmode:
                            left.code(ascii_darkmode)
                        else:
                            left.code(ascii_whitmode)                      
                if len(faces) == 0:
                    st.write("No human faces detected in this image :confounded:...")
            
            else:
                st.write("Unrecognized option, see source code...")
            
if __name__ == "__main__":
    main()