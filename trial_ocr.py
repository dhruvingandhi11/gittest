import os
import pytesseract as tess
# tess.pytesseract.tesseract_cmd = "C:/Users/WOT-Dhruvin/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
from PIL import Image


img = Image.open(r"C:/Users/WOT-Dhruvin/Downloads/70e296da801318743.jpg")
text = tess.image_to_string(img,lang = "hin")
print(text)