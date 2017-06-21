# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 12:28:58 2017

@author: ndoannguyen
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy import misc

probability = 0.1

def to_binary_image(image):
    """
        png to binary
    """
    binary_list = []
    for row in image:
        for pixel in row:
            binary_list.append(to_binary_pixel(pixel))
    return np.reshape(binary_list, (width, height))
            
def to_binary_pixel(pixel):
    """
        png pixel to binary
    """
    if (pixel[0] + pixel[1] + pixel[2]) > 128:
        return 1
    else:
        return 0

def generate_random_noise(width, height, probability):
    """
        Generate random noise
    """
    return np.random.binomial(1, probability, (width, height))
    
def predict_pixel(image, index):
    """
        Predict the value of a pixel based on the neighbors
    """
    width = len(image)
    height = len(image[0])
    neighbor_sum = image[index[0], index[1]]
    neighbor_count = 1
    if (index[0] > 0):
        neighbor_sum += image[index[0] - 1, index[1]]
        neighbor_count += 1
    if (index[0] < width - 1):
        neighbor_sum += image[index[0] + 1, index[1]]
        neighbor_count += 1
    if (index[1] > 0):
        neighbor_sum += image[index[0], index[1] - 1]
        neighbor_count += 1
    if (index[1] < height - 1):
        neighbor_sum += image[index[0], index[1] + 1]
        neighbor_count += 1
    if neighbor_sum > neighbor_count / 2.0:
        return 1
    else:
        return 0
        
def denoise_image(image):
    """
        Denoise
    """
    predicted_img = []
    width = len(image)
    height = len(image[0])
    for row_idx in range(width):
        for col_idx in range(height):
            predicted_img.append(predict_pixel(image, (row_idx, col_idx)))
    return np.reshape(predicted_img, (width, height))

#Read original picture
original_picture = misc.imread('binary-icon-30.png')
width = len(original_picture)
height = len(original_picture[0])

#Change to binary
binary_picture = to_binary_image(original_picture)
plt.imsave('BinaryPicture.png', np.reshape(binary_picture, (width, height)), cmap=cm.gray)

#Make noise to the picture
noised_picture = (binary_picture + generate_random_noise(width, height, probability))%2
plt.imsave('NoisedPicture.png', np.reshape(noised_picture, (width, height)), cmap=cm.gray)

#Denoise it
denoised_picture = denoise_image(noised_picture)
plt.imsave('DenoisedPicture.png', np.reshape(denoised_picture, (width, height)), cmap=cm.gray)

#Denoise it one more time
denoised_picture_2 = denoise_image(denoised_picture)
plt.imsave('DenoisedPicture2.png', np.reshape(denoised_picture_2, (width, height)), cmap=cm.gray)