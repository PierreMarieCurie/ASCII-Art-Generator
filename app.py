import streamlit as st
from PIL import Image
from src import tools
import numpy as np

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
    uploaded_file = st.file_uploader("Upload an Image", type=ALLOWED_EXTENSIONS)
    
    if uploaded_file is not None:
        
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # User selection
        with st.container(border=True):
            col1, col2 = st.columns([0.8, 0.2])

            # Slider to select the threshold
            col1.markdown('<div class="centered-text">Select a threshold</div>', unsafe_allow_html=True)
            col1.write("")
            threshold = col1.slider("Select a threshold",
                                    min_value=0.2,
                                    max_value=0.95,
                                    step=0.05,
                                    value=0.6,
                                    label_visibility="collapsed")

            # Toggle to select darkmode or not
            col2.markdown('<div class="centered-text">Darkmode</div>', unsafe_allow_html=True)
            col2.write("")
            _, center_col, _ = col2.columns(3)
            flag_darkmode = center_col.toggle("Darmode",
                                            value=True,
                                            label_visibility="collapsed")

        with st.spinner('Wait for it...'):
            text = tools.process_image(img_array, float(threshold)*100)
        
        left, right = st.columns(2)
        left.image(img_array, use_column_width=True)
        if flag_darkmode:
            right.code(text[0])  
        else:
            right.code(text[1])

if __name__ == "__main__":
    main()