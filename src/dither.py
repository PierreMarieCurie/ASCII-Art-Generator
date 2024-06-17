import numpy as np

#https://github.com/lukepolson/youtube_channel/blob/main/Python%20Metaphysics%20Series/vid39.ipynb
def floyd_steinberg(image, frac=16, round_func=round):
    Lx, Ly = image.shape
    for j in range(Ly):
        for i in range(Lx):
            rounded = round_func(image[i,j])
            err = image[i,j] - rounded
            image[i,j] = rounded
            if i<Lx-1: image[i+1,j] += (7/frac)*err
            if j<Ly-1:
                image[i,j+1] += (5/frac)*err
                if i>0: image[i-1,j+1] += (3/frac)*err
                if i<Lx-1: image[i+1,j+1] += (1/frac)*err     
    return np.clip(image, a_min=0, a_max=1)