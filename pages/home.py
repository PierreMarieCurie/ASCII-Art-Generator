import streamlit as st

# Welcome title
st.markdown("<h1 style='text-align: center;'>Welcome to the Ultimate ASCII Art Generator! 🎨</h1>", unsafe_allow_html=True)

# Introduction section
st.write("""
Create amazing ASCII art with our easy-to-use, open-source tool! Convert entire images or focus on detailed portraits — the choice is yours. 

Need something small? All modes let you create ASCII art perfectly sized for chat boxes, reducing the number of characters for clear visibility.

Check out the [GitHub repo](https://github.com) and join the fun!
""")

# Classic option section with image
st.subheader("1. Classic Mode")
st.write("""
In **Classic Mode**, you can quickly turn any image into ASCII art. It's perfect for landscapes, objects, or whatever you want to transform into a work of text-based art!
""")
#st.image("data/macron.PNG", caption="Example of Classic Mode")

# Portrait option section with AI-powered mention and image
st.subheader("2. Portrait Mode (AI-powered)")
st.write("""
**Portrait Mode**, powered by AI, is all about faces. The generation tool automatically detects the facial parts in the image, and you can then choose which ones you want to appear in the ASCII.
""")
#st.image("data/macron.PNG", caption="Example of Portrait Mode")

# Multi-portrait option section with AI-powered mention and image
st.subheader("3. Multi-Portrait Mode (AI-powered)")
st.write("""
Want to convert multiple faces in one image? **Multi-Portrait Mode** uses AI to detect and enhance each face, turning them all into detailed ASCII art portraits. Like portrait mode, the facial parts in the image.
""")
#st.image("data/macron.PNG", caption="Example of Multi-Portrait Mode")

# Closing statement
st.write("""
Ready to start? Pick a mode, upload your image, and watch it transform into stunning ASCII art!
""")