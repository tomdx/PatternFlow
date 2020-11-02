#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import all the Libraries
import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
get_ipython().run_line_magic('matplotlib', 'inline')

from tqdm import tqdm_notebook, tnrange
from itertools import chain
from skimage.io import imread, imshow, concatenate_images
from skimage.transform import resize
from skimage.morphology import label
from sklearn.model_selection import train_test_split

import tensorflow as tf

from keras.models import Model, load_model
from keras.layers import Input, BatchNormalization, Activation, Dense, Dropout
from keras.layers.core import Lambda, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D, GlobalMaxPool2D
from keras.layers.merge import concatenate, add
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.utils import to_categorical


# In[2]:


# check the version
print(tf.keras.__version__)


# In[13]:


# Initialising the compression dimensions
img_width = 256
img_height =256
border = 5


# In[14]:


# Loading the dataset 
isic_features = next(os.walk("D:/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1-2_Training_Input_x2"))[2] # returns all the files "DIR."
isic_labels = next(os.walk("D:/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1_Training_GroundTruth_x2"))[2] # returns all the files "DIR."

print("Number of images in features folder = ", len(isic_labels))
print("Number of images in labels folder = ", len(isic_labels))


# In[15]:


isic_features_sort = sorted(isic_features) # Sorting of data wit respect to labels
isic_labels_sort = sorted(isic_labels) # Sorting of data wit respect to labels


# In[16]:


def load_features(inp_path,ids):
    X= np.zeros((len(ids),img_height,img_width,1),dtype=np.float32)
    for n, id_ in tqdm_notebook(enumerate(ids), total=len(ids)): # capture all the images ids using tqdm       
        img = load_img(inp_path+id_, color_mode = 'grayscale')  
        x_img = img_to_array(img) # Convert images to array
        x_img = resize(x_img,(256,256,1),mode = 'constant',preserve_range = True)
        X[n] = x_img/255 # Normalize the images
    return X    


# In[17]:


def load_labels(inp_path,ids):
    X= np.zeros((len(ids),img_height,img_width,1),dtype=np.uint8)
    for n, id_ in tqdm_notebook(enumerate(ids), total=len(ids)):
        img = load_img(inp_path+id_,color_mode = 'grayscale') # Load images here
        x_img = img_to_array(img) # Convert images to array
        x_img = resize(x_img,(256,256,1),mode = 'constant', preserve_range = True)
        X[n] = x_img
    return X


# In[18]:


# Loading the images for the training input data set
X_isic_train = load_features("D:/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1-2_Training_Input_x2/",isic_features_sort)


# In[19]:


# Loading the images for the training groundtruth data set
y_isic_train=load_labels("D:/ISIC2018_Task1-2_Training_Data/ISIC2018_Task1_Training_GroundTruth_x2/",isic_labels_sort)

