import torchvision.transforms as transforms
import cv2
import torch
import numpy as np

#FACE_PARSING_PATHNAME = '.'
#sys.path.insert(0, FACE_PARSING_PATHNAME)
from .model import BiSeNet

FACE_PARSING_WEIGHTS_PATHNAME = 'weights/face_parsing.pth'
RESNET18_WEIGTHS_PATHNAME = 'weights/resnet18-5c106cde.pth'
FACE_PARTS = ['background', 'face', 'left eyebrow', 'right eyebrow',
    'left eye', 'right eye', 'glasses', 'left ear', 'right ear',
    'earrings', 'noise', 'inside the mouth', 'upper lips', 'lower lips',
    'neck', 'necklace', 'clothes', 'hair', 'hat']
        
BISENET_PREPROCESSING = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])


class FaceSegmentation:
    def __init__(self, device='cpu') -> None:
        self.device = device
        self.net = self.initialize_model()

    def initialize_model(self):
        net = BiSeNet(n_classes=len(FACE_PARTS), resnet18_url=RESNET18_WEIGTHS_PATHNAME)
        net.load_state_dict(torch.load(FACE_PARSING_WEIGHTS_PATHNAME), self.device)
        net.to(self.device)
        net.eval()
        return net

    def __preprocess(self, im):
        """ im must be a BGR image """
        
        # Resize the image to 512x512
        im = cv2.resize(im, (512, 512), interpolation=cv2.INTER_LINEAR)

        # Convert the image from BGR to RGB
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # Convert the image to a tensor and normalize it
        im = BISENET_PREPROCESSING(im).to(self.device)

        # Add a batch dimension
        im = torch.unsqueeze(im, 0)

        # Move the tensor to the GPU or stay on CPU
        im = im.to(self.device)
        
        return im

    def __get_masks_from_segments(self, segments, original_size):
        
        masks = [None]*len(FACE_PARTS)

        for i in range(len(FACE_PARTS)): # peut etre loop sur masks ?
            mask = (segments == i).astype(np.uint8)
            masks[i] = cv2.resize(mask, original_size[::-1], interpolation=cv2.INTER_LINEAR)
            
        return masks
    
    def __get_bbox_from_mask(self, mask):
        
        # Get the indices of True values
        y_indices, x_indices = np.where(mask)
        
        if len(y_indices) > 0:
            
            ## Find the minimum and maximum x and y coordinates
            left = np.min(x_indices)
            right = np.max(x_indices)
            top = np.min(y_indices)
            bottom = np.max(y_indices)

            return [left, top, right, bottom]
        else:
            return None

    def predict(self, im):
        """ im must be a BGR image """
        
        original_size = im.shape[:2] 
        im = self.__preprocess(im)
        
        with torch.no_grad():
            segments = self.net(im)[0].squeeze(0).cpu().numpy().argmax(0).astype(np.uint8)
        
        masks = self.__get_masks_from_segments(segments, original_size)
        
        bboxes = [self.__get_bbox_from_mask(mask) for mask in masks]
    
        return segments, masks, bboxes, FACE_PARTS
