import cv2
import numpy as np
import math

def histogram_equalize(img):
    image = np.asarray(img)

    ints_array = np.zeros(256)
    x_axis, y_axis = image.shape[:2]
    for i in range(0, x_axis):
        for j in range(0, y_axis):
            ints = image[i, j]
            ints_array[ints] = ints_array[ints] + 1

    MN = 0
    for i in range(1, 256):
        MN = MN + ints_array[i]

    array_pdf = ints_array / MN

    CDF = 0
    CDF_matrix = np.zeros(256)
    for i in range(1, 256):
        CDF = CDF + array_pdf[i]
        CDF_matrix[i] = CDF

    final_array = np.zeros(256)
    final_array = (CDF_matrix * 255)
    for i in range(1, 256):
        final_array[i] = math.ceil(final_array[i])
        if (final_array[i] > 255):
            final_array[i] = 255

    new_img = np.zeros(img.shape)
    for i in range(0, x_axis):
        for j in range(0, y_axis):
            for value in range(0, 255):
                if (image[i, j] == value):
                    new_img[i, j] = final_array[value]
                    break
    return new_img


input_image = cv2.imread('mandrill.png', 1)
r = input_image[:, :, 2]
g = input_image[:, :, 1]
b = input_image[:, :, 0]
r2 = histogram_equalize(r)
g2 = histogram_equalize(g)
b2 = histogram_equalize(b)
out_image = np.zeros((input_image.shape[0], input_image.shape[1], 3), float)
out_image[..., 0] = b2
out_image[..., 1] = g2
out_image[..., 2] = r2

cv2.imwrite('HEQ_mandrill.png', out_image)