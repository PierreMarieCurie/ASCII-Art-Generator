import streamlit as st
from PIL import Image
from src import tools
from src import dither
import numpy as np
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pbm', 'tiff', 'tif', 'bmp'}  # Define allowed file extensions

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
        
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # User selection
        with st.container(border=True):
            
            option = st.selectbox(
                "Select ASCII mode",
                ("Little ASCII Art", "Multiple ASCII Art of human faces", "Big ASCII Art")
                )
            
            col1, col2 = st.columns([0.8, 0.2])

            # Slider to select the threshold
            col1.markdown('<div class="centered-text">Select a threshold</div>', unsafe_allow_html=True)
            col1.write("")
            if option == "Big ASCII Art":
                min_value=4
                max_value=30
                step=2
                default_value=16
            else:
                min_value=0.1
                max_value=0.9
                step=0.05
                default_value=0.6
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

        with st.spinner('Wait for it...'):
            
            img_array = tools.preprocess_image(img_array)
            
            
            # here to the face detection with an option
            
            if option == "Little ASCII Art":
                new_shape = tools.get_max_shape(img_array.shape)
                img_array = cv2.resize(img_array, (new_shape[::-1]))
            elif option == "Big ASCII Art":
                img_array = tools.resize_image_with_fixed_width(img_array, 120)
                
            data = img_array.astype(np.float32)/255
            
            if option == "Little ASCII Art":
                img_final = (data > threshold).astype(int)
                
                ascii_darkmode = tools.convert_array_to_braille_characters(img_final)
                ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final)
                left, right = st.columns(2)
                left.image(image, use_column_width=True)
                if flag_darkmode:
                    right.code(ascii_darkmode)  
                else:
                    right.code(ascii_whitmode)
                    
            elif option == "Big ASCII Art":
                img_final = dither.floyd_steinberg(data, threshold)
                ascii_darkmode = tools.convert_array_to_braille_characters(img_final)
                ascii_whitmode = tools.convert_array_to_braille_characters(1-img_final)
                st.image(image, use_column_width=True)
                st.code(ascii_darkmode)
            else:
                st.write("to do")

if __name__ == "__main__":
    main()