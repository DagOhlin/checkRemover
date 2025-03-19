import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import img2pdf

# ----- User Configuration -----
INPUT_FOLDER = r"pdfsToBeFixed"     # Folder containing the original PDFs
OUTPUT_FOLDER = r"fixedPdfs"     # Folder where the fixed PDFs will be saved
POPPLER_PATH = r"C:\Users\Ägare\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
DPI = 200  # Adjust DPI as needed

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Create a base temporary folder for image files
BASE_TEMP_FOLDER = "temp_images"
if not os.path.exists(BASE_TEMP_FOLDER):
    os.makedirs(BASE_TEMP_FOLDER)

# ----- Processing Each PDF in the Input Folder -----
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(INPUT_FOLDER, filename)
        output_pdf_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", "-fixed.pdf"))
        # Create a temporary folder for this PDF's images
        temp_img_folder = os.path.join(BASE_TEMP_FOLDER, filename[:-4])
        if not os.path.exists(temp_img_folder):
            os.makedirs(temp_img_folder)

        print(f"Processing {filename}...")

        # 1. Convert PDF pages to images using poppler_path
        pages = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)
        image_paths = []
        for i, page in enumerate(pages):
            img_path = os.path.join(temp_img_folder, f"page_{i}.png")
            page.save(img_path, "PNG")
            image_paths.append(img_path)

        # 2. Remove green check marks using OpenCV
        for img_path in image_paths:
            image = cv2.imread(img_path)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Define the HSV range for green check marks (adjust values if needed)
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # Replace green areas with white
            image[mask != 0] = [255, 255, 255]
            cv2.imwrite(img_path, image)

        # 3. Convert the cleaned images back into a single PDF
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))

        print(f"Processing complete for {filename}. Cleaned PDF saved as: {output_pdf_path}")

        # Optionally, remove temporary images for this PDF:
        # for img_path in image_paths:
        #     os.remove(img_path)
        # os.rmdir(temp_img_folder)

print("All PDFs processed!")
