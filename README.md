# ASCII-Art-Generator

Welcome to the ASCII Art Creator! This tool allows you to transform images into stunning ASCII art. This repo is the code source for https://ascii-art-generator.streamlit.app/.

<p style="font-size: 5px;">

⠀⠀⠹⣧⠄⠈⠉⢶⢮⣝⣻⣶⣿⣿⣶⣶⣿⣿⣿⣣⣶⣿⣿⣿⠸⣿⣿⡿⡀
⣄⡈⠃⠙⠛⠻⠒⠀⠉⠐⠒⠿⠿⠿⠿⠟⠛⣩⣾⣿⣿⣿⣿⣿⠀⣿⣿⡇⠀
⠈⠳⢶⣿⠗⠪⡀⠀⡀⠀⠀⣀⣠⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⢹⡿⡄⠀
⠤⠀⠀⠀⠀⠉⠩⢍⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⠀⡇⠨⡒
⡏⠀⠀⠀⢀⣀⣀⡈⠉⠛⠿⠿⣿⣿⣿⣿⣿⣿⠟⠛⠋⢙⣻⣿⣇⠀⠀⢶⡻
⡿⠀⠀⢠⣿⠟⠛⠋⠉⠁⠄⡀⠙⢿⣿⣿⣿⢋⠀⡀⠀⠈⠉⠛⢿⡆⠀⢱⣷
⠀⠀⠀⣿⣿⣆⢀⣐⡤⣴⣿⣬⣦⢸⣿⣿⣿⣿⣮⣷⣶⣾⣤⣴⣾⣧⠀⠀⠞
⠀⠀⢀⣿⣿⣿⣿⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⠀⠀⠘
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠚
⠉⠀⢷⠻⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣏⠀⠀⢀
⠈⠀⢸⠆⠈⠉⠛⢿⢟⣿⣧⠘⠋⠿⣿⣿⡿⢛⣿⣿⣆⠹⣿⣿⣿⡷⠀⠀⢁
⠀⠀⠀⠘⠀⢤⣾⣿⣿⠿⣿⣷⣤⡀⢈⣽⣾⣿⣿⠿⢻⣦⣿⣿⣿⠃⠀⢀⣿
⠀⢀⠀⠀⠀⠘⢿⣿⣿⣆⠀⢠⣴⣴⣦⣴⣦⣶⠆⣠⣿⣿⣿⣿⡟⠀⢀⣼⣿
⠿⣿⣿⣿⣷⣶⣾⣿⣿⣿⡅⠀⠈⣉⣋⣭⣭⡴⣢⣿⣿⣿⣿⡟⠀⠀⣾⣿⣿
⡆⢿⣿⠈⣿⣟⠉⠈⣿⣿⣿⣷⣦⣤⣤⣥⣴⣾⣿⣿⣿⣿⠋⠀⠀⢀⣿⣿⣿
⣿⠸⣿⢈⣾⣿⣷⡄⠙⠘⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣶⣾⣿⣿⣿

</p>

## Features

- **Image to ASCII Art**: Transform images into intricate ASCII representations.
- **Supports Various Sizes**: Create both small and large ASCII art images.
- **Customizable Settings**: Adjust threshold value, algorithms, darkmode and more to fine-tune your art.
- **Human Faces Mode**: Includes a mode specifically for generating ASCII art from human faces in images.
- **Save and Share**: Save your creations by coping or as text files then share them as you like.

## Installation

To get started with the ASCII Art Generator, choose the option you like :

### Online

 Just go to https://ascii-art-generator.streamlit.app/

### On host

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ascii-art-creator.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ASCII-Art-Generator
    ```

3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run time :
    ```bash
    streamlit run app.py 
    ```
    Note that you can set different port number (Note that Streamlit will increment the port number if it is used):
    ```bash
    streamlit run app.py --server.port 8080
    ```

### Using docker

to do

# License

This project is licensed under the [MIT License](LICENSE). You can find the full text of the license in the `LICENSE` file.

## To do

1. work on code cleaning
2. darkmode doesn't restart the ascii creation
3. improve README (how to use the two options with illustration, installation on host...)
4. add Dockerfile
5. add a gallery ? (st.navigation ?)
