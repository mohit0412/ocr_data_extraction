import PyPDF2
import os
import io
import threading
import re
import sys
import json
#PDF TO IMAGE CONVERSION
#IMPORT LIBRARIES
from utility import read_hpi,extract_data_nsdl
import pdf2image
from PIL import Image
import time
import cv2
import pytesseract
import preprocess_image
from pytesseract import Output

#DECLARE CONSTANTS
PDF_PATH = sys.argv[1]
DPI = 300
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = 'ADGPJ5032L'
USE_CROPBOX = False
STRICT = False
result=''
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
custom_oem_psm_config = r'-c preserve_interword_spaces=0 --oem 3 --psm 6 -l eng'
output_file=sys.argv[1].split('.')[0]


def ocr(img,big_filename):
    global result
    data=pytesseract.image_to_string(img,config=custom_oem_psm_config)
    #file_obj.write(str(data)+'\n\n')
    result=result+str(data)+'\n\n'
    os.remove(big_filename)


def pdftopil():
    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    return pil_images
    
    
def save_images(pil_images):
    #This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    for image in pil_images:
        image.save("page_" + str(index) + ".jpg")
        img=preprocess_image.get_grayscale(cv2.imread("page_" + str(index) + ".jpg"))
        img=preprocess_image.thresholding(img)
        t=threading.Thread(target=ocr, args=(img,"page_" + str(index) + ".jpg",))
        t.start()
        t.join()
        index += 1


if __name__ == "__main__":
    start_time = time.time()
    pil_images = pdftopil()
    save_images(pil_images)
    text=re.sub(r'\s\s+','\n',result)
    preprocess_text=read_hpi(text.split('\n'))
    final_data=extract_data_nsdl(preprocess_text)
    with open('intermediate_text_chandrika.txt','w+') as op:
       for data in final_data:
          op.write(str(data)+'\n\n')
    print("----------------------------------- %s seconds -------------------------" % (time.time() - start_time))









