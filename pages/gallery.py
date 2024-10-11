import streamlit as st
import os

# Welcome title
st.title("Gallery 🎨")

# Set the folder path where the .txt files are located
folder_path = "gallery"

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is a .txt file
    if file_name.endswith(".txt"):
        # Create the full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Open and read the file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Display the file name as title
        st.title(file_name.split(".")[0].replace('_', ' ').title())
        
        # Display the file content as code
        st.code(content, language='text')
