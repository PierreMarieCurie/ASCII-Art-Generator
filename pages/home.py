import streamlit as st
#RAJOUTER PAGE LINK
# Welcome title
st.title("Welcome to the Ultimate ASCII Art Generator! 🎨")

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
st.image("data/macron.PNG", caption="Example of Classic Mode")

# Portrait option section with AI-powered mention and image
st.subheader("2. Portrait Mode (AI-powered)")
st.write("""
**Portrait Mode**, powered by AI, is all about faces. It adds extra detail to your portraits, making them stand out as beautifully contoured ASCII art.
""")
st.image("data/macron.PNG", caption="Example of Portrait Mode")

# Multi-portrait option section with AI-powered mention and image
st.subheader("3. Multi-Portrait Mode (AI-powered)")
st.write("""
Want to convert multiple faces in one image? **Multi-Portrait Mode** uses AI to detect and enhance each face, turning them all into detailed ASCII art portraits.
""")
st.image("data/macron.PNG", caption="Example of Multi-Portrait Mode")

# Closing statement
st.write("""
Ready to start? Pick a mode, upload your image, and watch it transform into stunning ASCII art!
""")