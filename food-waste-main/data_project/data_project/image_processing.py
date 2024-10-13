# convert image into String
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from PIL import Image
import pytesseract
import re
import cv2
import numpy as np

# Optional: Set the path to tesseract.exe if not automatically found
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open image file
image_path = 'receipt.jpg'
image = Image.open(image_path)

# Convert image to grayscale
gray_image = image.convert('L')

# Convert the image to a numpy array for OpenCV processing
gray_image_cv = np.array(gray_image)

# reduce noise with Gaussian Blur
# blurred_image = cv2.GaussianBlur(gray_image_cv, (3, 3), 0)

# adaptive thresholding for contrast
binary_image = cv2.threshold(gray_image_cv, 150, 255, cv2.THRESH_BINARY)

# morphological operations to remove small noise
# kernel = np.ones((1, 1), np.uint8)  
# opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

# changes to binarizing the image
    # Apply thresholding to binarize the image
_, binary_image = cv2.threshold(gray_image_cv, 150, 255, cv2.THRESH_BINARY)

# Convert the binary image back to a PIL image for pytesseract
binarized_image = Image.fromarray(binary_image)



# Optional: Resize the image to enhance OCR accuracy (scale factor of 1.5 or 2 can be tested)
# resized_image = binarized_image.resize((int(binarized_image.width * 2), int(binarized_image.height * 2)))

# Extract text from the image using OCR with custom configurations
custom_config = r'--oem 3 --psm 6'
# Use the LSTM engine and assume a single uniform block of text
extracted_text = pytesseract.image_to_string(binarized_image, config=custom_config)



