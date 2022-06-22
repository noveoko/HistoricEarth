import cv2
import time
from pathlib import Path


def slice_image_up(image_path):
    string_path = image_path.as_posix()
    img = cv2.imread(string_path)
    img2 = img

    height, width, channels = img.shape
    # Number of pieces Horizontally
    CROP_W_SIZE = 25
    # Number of pieces Vertically to each Horizontal
    CROP_H_SIZE = 25

    for ih in range(CROP_H_SIZE):
        for iw in range(CROP_W_SIZE):

            x = width/CROP_W_SIZE * iw
            y = height/CROP_H_SIZE * ih
            h = (height / CROP_H_SIZE)
            w = (width / CROP_W_SIZE)
            print(x, y, h, w)
            img = img[y:y+h, x:x+w]

            NAME = str(time.time())
            cv2.imwrite("slices/CROP/" + str(time.time()) + ".png", img)
            img = img2


root = "."

files = Path(root).glob("cropped/**/*.*")

for file in files:
    file_path = file
    stem = file.stem
    slice_image_up(file_path)
    

# SOURCE: https://stackoverflow.com/questions/44759654/divide-image-into-two-equal-parts-python-opencv/44764659
