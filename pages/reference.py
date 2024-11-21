import streamlit as st

# Title
st.title("Reference")

# Section 1: Dithering Algorithms
st.header("Dithering Algorithms")

st.markdown("""
Dithering is a technique used in image processing to reduce the number of colors in an image while maintaining its visual appearance.
We use this to create images made of black and white pixels, which, combined with a numerical representation using Braille characters, form ASCII art.
Learn more about Braille **[here](https://en.wikipedia.org/wiki/Braille)**.

This tool implements **two popular [dithering algorithms](https://en.wikipedia.org/wiki/Dither)**:
""")

st.markdown("""
1. **[Floyd-Steinberg Dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering)**:
   - A widely used error-diffusion algorithm.
   - It works by distributing the quantization error of a pixel to its neighboring pixels.
   - This results in smoother gradients and less visible banding in images with reduced color palettes.
""")

st.markdown("""
2. **[Atkinson Dithering](https://en.wikipedia.org/wiki/Atkinson_dithering)**:
   - A simpler variation of error-diffusion dithering.
   - It spreads the error to fewer surrounding pixels, creating a more stylized, dotted appearance.
   - Atkinson dithering is often associated with early Macintosh graphics.
""")

st.markdown("""
These dithering techniques are useful for creating artistic effects, reducing image file sizes, or preparing images for low-color displays like e-ink screens or LED matrices.
Both implementation are extracted from [here](https://github.com/lukepolson/youtube_channel/blob/main/Python%20Metaphysics%20Series/vid39.ipynb).

For small-sized images, we use a simple threshold because dithering algorithms require a minimum number of pixels to work effectively.
""")

# Section 2: Face Detection and Segmentation
st.header("Face Detection and Segmentation")

st.markdown("""
This tool includes advanced **face detection** and **segmentation algorithms** to process images with human faces. Here's how these features work:
""")

st.markdown("""
1. **Face Detection**:
   - Uses **OpenCV's Haar Cascade classifier** for fast and efficient detection of faces in images. Official repo **[here](https://github.com/zllrunning/face-parsing.PyTorch)**.
   - OpenCV is an open-source computer vision library, and its Haar Cascade method is based on machine learning to detect objects in an image.
   - Learn more about OpenCV and its face detection capabilities **[here](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)**.

2. **Face Segmentation**:
   - Employs a **pre-trained face segmentation model** to precisely isolate facial features (like eyes, nose, and mouth) and background regions.
   - This is useful for applications like applying artistic filters, virtual try-on for glasses or makeup, and more.
   - Learn about the basics of image segmentation **[here](https://en.wikipedia.org/wiki/Image_segmentation)**.
""")