from unicodedata import lookup
import numpy as np
import cv2
from .dither import floyd_steinberg

def convert_array_to_Braille_character(arr:np.ndarray) -> str:
    """
    Convert a numpy array to a braille character (ex : array([[1, 1], -> '⡝')
                                                              [0, 1],
                                                              [1, 0],
                                                              [1, 0]]) 
    Args:
        array (np.ndarray): 1D or 2D numpy array of 8 digits

    Returns:
        str: braille character
    """
    
    # Check input data
    if not isinstance(arr, np.ndarray):
        raise TypeError("Input data must be a NumPy array")
    elif arr.shape != (4,2):
        raise ValueError('Input data must have a shape of (4,2), not {}.'.format(arr.shape))
    elif ~np.all(np.logical_or(arr == 0, arr == 1)):
        raise ValueError('Input data must only contain binary values.')
    
    # Convert numpy array to flat str and rearrange the order of numbers to follow a left-right and top-bottom sequence
    arr = ''.join(map(str,np.array(arr.astype(int)).ravel()[[7, 6, 5, 3, 1, 4, 2, 0]]))
        
    # Mostly extracted from https://stackoverflow.com/a/66085578/23149314)
    return chr(ord(lookup('BRAILLE PATTERN BLANK')) + int(str(arr), 2))
    
def convert_array_to_braille_characters(im:np.ndarray) -> str:
    """ Convert an image of 0 and 1 to a string in Braille

    Args:
        im (np.ndarray): Image that only contains 0 and 1 values

    Returns:
        str: Image with braille characters and returns
    """
    
    # Initialization
    ascii_art_str = '\n'
    
    # Loop through groups of 8 pixels
    for row in range(0, im.shape[0]//4*4, 4):
        for col in range(0, im.shape[1]//2*2, 2):
            
            # Convert a group of 8 pixel to a braille cha
            ascii_art_str += convert_array_to_Braille_character(im[row:row+4,col:col+2])
        
        # New line
        ascii_art_str += '\n'
        
    return ascii_art_str

def get_max_shape(shape:tuple, max_length:int=500) -> tuple:
    """Given an image shape, returns the maximum shape TO DO

    Args:
        shape (tuple): 

    Returns:
        tuple: Maximum shape 
    """
    
    # 8 : number of pixels in a single braille character
    # 500 : max number of characters allowed by Twitch
    # - size[0] : newline for every image row of the image
    max_pixels = 8 * 500 - shape[0]
    
    # Ratio between the old size and the new
    ratio = (shape[0]*shape[1]/max_pixels)**.5
    
    return tuple(int(i/ratio) for i in shape[:2])
    
def enhance_image(im:np.ndarray) -> np.ndarray:
    """ Enhance image quality using adaptive histogram equalization (Source: https://stackoverflow.com/a/41075028/23149314).

    Args:
        im (np.ndarray): Input image

    Returns:
        np.ndarray: Enhanced image
    """
    # Converting to LAB color space
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # Merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
def convert_to_gray(image):
    # Check the number of channels in the image
    if len(image.shape) == 3:
        if image.shape[2] == 4:
            # Convert 4-channel (RGBA/BGRA) to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        elif image.shape[2] == 3:
            # Convert 3-channel (RGB/BGR) to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError("Unexpected number of channels in image: {}".format(image.shape[2]))
    else:
        raise ValueError("Input image does not have 3 dimensions")

    return gray_image

def preprocess_image(img):
    
    img = enhance_image(img)
    
    img = cv2.resize(img, None, fx=.85, fy=1, interpolation=cv2.INTER_AREA)
    
    img = convert_to_gray(img)
    
    return img

def resize_image_with_fixed_width(image, fixed_width):
    """
    Resize an image to a fixed width while maintaining the aspect ratio.

    Parameters:
    image_path (numpy.ndarray): The input image.
    fixed_width (int): Desired width of the resized image.

    Returns:
    resized_image (numpy.ndarray): The resized image.
    """

    # Get the original dimensions of the image
    height, width = image.shape[:2]

    # Calculate the ratio of the new width to the old width
    ratio = fixed_width / float(width)

    # Calculate the new height to maintain the aspect ratio
    new_height = int(height * ratio)

    # Resize the image with the new dimensions
    return cv2.resize(image, (fixed_width, new_height), interpolation=cv2.INTER_AREA)