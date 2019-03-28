import cv2
import numpy as np
from scipy import ndimage

#STEP0 :: Grayscaling :: Color-to-Grayscale-Conversion
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

# STEP1 :: Perprocessing :: Applying Gaussian Blur
def gaussian_kernel(size, sigma=1):
    size = int(size) // 2 # Floor Division to Determine the Dimension
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g = np.exp(-((x**2 + y**2) / (2.0 * sigma**2))) * normal
    return g

#STEP2 :: Calculating Gradients :: Sobel Edge Detector
def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)# Highlighting Pixel Intensity
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    Ix = ndimage.filters.convolve(img, Kx)# Derivate x
    Iy = ndimage.filters.convolve(img, Ky)
    G = np.hypot(Ix, Iy)# Gradient
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)# Slope
    return (G, theta)

#STEP3 :: Non-Maximum Suppression :: Reducing the Edges
def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.int32)
    angle = D * 180. / np.pi # Conversion to Degree
    angle[angle < 0] += 180
    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]
                if (img[i,j] >= q) and (img[i,j] >= r):
                    Z[i,j] = img[i,j]
                else:
                    Z[i,j] = 0
            except IndexError as e:
                pass
    return Z

#STEP4 :: Thresholding :: Identifying Strong, Weak, and Non-Relevant Pixels
def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.15):
    highThreshold = img.max() * highThresholdRatio;
    lowThreshold = highThreshold * lowThresholdRatio;
    M, N = img.shape
    res = np.zeros((M,N), dtype=np.int32)
    weak = np.int32(25)
    strong = np.int32(255)
    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    return (res, weak, strong)

#STEP5 :: Hysteresis :: Edge Tracking
def hysteresis(img, weak, strong=255):
    M, N = img.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img

#STEP6 :: Canny Edge Detection :: Going Through The Previous Steps
def detect(image_detect):
    image = cv2.imread(image_detect)
    gray_image = rgb2gray(image)
    blurred_image = ndimage.convolve(gray_image, gaussian_kernel(5, 1.4))
    gradient, angle = sobel_filters(blurred_image)
    nonMax_image = non_max_suppression(gradient, angle)
    threshold_image, weak, strong = threshold(nonMax_image)
    final_image = hysteresis(threshold_image, weak, strong)
    return final_image
