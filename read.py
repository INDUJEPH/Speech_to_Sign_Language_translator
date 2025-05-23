from PIL import Image
import cv2
import pytesseract
from textblob import TextBlob
import webp
import os
import shutil

# Destination paths
dest = r"E:\Python_projects\New folder\gif_extract\gif_data\"r" # Source directory
op_dest = r"E:\Python_projects\New folder\filtered_data"

# Ensure output directory exists
os.makedirs(op_dest, exist_ok=True)

# Process files
for i in range(107):
    ip = os.path.join(dest, f"{i}.webp")  # Source file path
    op = os.path.join(dest, "tmp.gif")  # Temporary gif file path

    try:
        # Load WebP images and save as GIF
        anim = webp.load_images(ip)
        anim[0].save(op, save_all=True, append_images=anim[0:1], duration=1, loop=0)

        # Open the first frame as PNG
        im = Image.open(op)
        im.seek(0)
        im.save("tmp.png")

        # Read image using OpenCV
        img = cv2.imread("tmp.png")
        crop_img = img[0:170, 200:470]  # Crop to relevant region

        # Perform OCR to extract text
        txt = pytesseract.image_to_string(crop_img)

        # Clean and correct text
        word = txt.replace("\n", "").replace(" ", "")
        word = ''.join(filter(str.isalnum, word)).lower()
        b = TextBlob(word)
        ans = str(b.correct())

        print(f"Corrected text: {ans}")

        # If valid text, rename the file, else store as unknown
        if len(ans) > 0:
            fname = os.path.join(op_dest, f"{ans}.webp")
        else:
            fname = os.path.join(op_dest, f"unknown{i}.webp")

        shutil.copyfile(ip, fname)

    except Exception as e:
        print(f"Error processing file {ip}: {e}")
