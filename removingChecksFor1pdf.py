import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import img2pdf



# Set your file paths
INPUT_PDF = "PA1459-202003.pdf"
OUTPUT_PDF = "PA1459-202003-fixed.pdf"
TEMP_IMG_FOLDER = "temp_images"

pages = convert_from_path(INPUT_PDF, dpi=200, poppler_path=r"C:\Users\Ägare\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin")


# Create a temporary folder for images if it doesn't exist
if not os.path.exists(TEMP_IMG_FOLDER):
    os.makedirs(TEMP_IMG_FOLDER)

# 1. Convert PDF pages to images
pages = convert_from_path(INPUT_PDF, dpi=200)  # Adjust DPI as needed
image_paths = []

for i, page in enumerate(pages):
    img_path = os.path.join(TEMP_IMG_FOLDER, f"page_{i}.png")
    page.save(img_path, "PNG")
    image_paths.append(img_path)

# 2. Remove green check marks using OpenCV
def remove_green_checks(img_path):
    image = cv2.imread(img_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for green color (adjust values if necessary)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Replace green areas with white
    image[mask != 0] = [255, 255, 255]
    cv2.imwrite(img_path, image)

# Process each image
for img_path in image_paths:
    remove_green_checks(img_path)

# 3. Convert the cleaned images back into a single PDF
with open(OUTPUT_PDF, "wb") as f:
    f.write(img2pdf.convert(image_paths))

# Optionally, clean up temporary image files
# for img_path in image_paths:
#     os.remove(img_path)
# os.rmdir(TEMP_IMG_FOLDER)

print("Processing complete! Cleaned PDF saved as:", OUTPUT_PDF)
