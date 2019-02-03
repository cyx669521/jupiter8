# Standard imports

# External dependencies
import numpy as np
import cv2
from keras.preprocessing import image
from sklearn.model_selection import train_test_split

# Local imports
from jup8.imgproc.filters import center_crop

IMG_HEIGHT = 128
IMG_WIDTH = 128

def load_images(filenames, resize_dim=(128,128), crop_dim=None):
    """Returns an array of loaded images

    Args:
        filenames:  list of image files
        resize_dim: (rows, cols) image should be resized tp
        crop_dim:   (rows, cols) to crop to (if provided)
    """
    rows, cols = resize_dim
    images = []
    for f in filenames:
        # Read image
        img = cv2.imread(f, 0)
        # Resize
        in_rows, in_cols = img.shape
        if (in_rows != rows) or (in_cols != cols):
            img = cv2.resize(img, (rows, cols))
        if crop_dim:
            out_rows, out_cols = crop_dim
            img = center_crop(img, out_rows, out_cols)
        # Add channel dimension
        img = np.expand_dims(img, axis=2)
        images.append(img)
    return np.array(images)

def get_training_generator(images, labels, batch_size=32):
    """Returns training and validator generators

    Args:
        images: array of image data
        labels: list of encoded (int) labels for images
    """
    gen_train = image.ImageDataGenerator(rescale=1./255,
                                         rotation_range=20,
                                         width_shift_range=0.2,
                                         height_shift_range=0.2,
                                         horizontal_flip=True,
                                         data_format='channels_last')
    
    gen_val = image.ImageDataGenerator(rescale=1./255,
                                       data_format='channels_last')

    # Partition training and validation data
    x_train, x_val, y_train, y_val = train_test_split(images, labels, test_size=0.1)

    # Get data generators
    train = gen_train.flow(x_train, y_train, batch_size=batch_size)
    val = gen_val.flow(x_val, y_val, batch_size=batch_size)

    return (train, val)
