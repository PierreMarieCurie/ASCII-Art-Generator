import streamlit as st
import os

# Set the folder path where the .txt files are located
GALLERY_PATH = "gallery"

# Welcome title
st.markdown("<h1 style='text-align: center;'>Gallery 🎨</h1>", unsafe_allow_html=True)

# Loop through all files in the folder
for file_name in os.listdir(GALLERY_PATH):
    # Check if the file is a .txt file
    if file_name.endswith(".txt"):
        # Create the full file path
        file_path = os.path.join(GALLERY_PATH, file_name)
        
        # Open and read the file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Display the file name as title
        st.title(file_name.split(".")[0].replace('_', ' ').title())
        
        # Display the file content as code
        st.code(content, language='text')
