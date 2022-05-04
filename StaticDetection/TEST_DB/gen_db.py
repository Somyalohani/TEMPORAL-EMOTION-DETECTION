import numpy as np
from PIL import Image
from scipy.ndimage import zoom
import cv2
import os

for files in os.listdir("."):
    if (files[-4:] == ".jpg"):
        img = cv2.imread(files)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        faces = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]  
        dim = (48, 48)
        resized = cv2.resize(faces, dim, interpolation = cv2.INTER_AREA)
        name = "edit_" + files[:-4] + ".png"
        cv2.imwrite(name, resized)

f = open("fer2013.csv", "a")
for files in os.listdir("."):
    if (files[-4:] == ".png"):
        srcImage = Image.open(files)
        grayImage = srcImage.convert('L')
        a = np.array(grayImage).astype(int)
        array = a.flatten()
        strs = ""
        if (files[15]=='A'):
            strs+='0'
            strs+=','
        if (files[15]=='D'):
            strs+='1'
            strs+=','
        if (files[15]=='F'):
            strs+='2'
            strs+=','
        if (files[15]=='H'):
            strs+='3'
            strs+=','
        if (files[15]=='S' and files[16]=='A'):
            strs+='4'
            strs+=','
        if (files[15]=='S'and files[16]=='U'):
            strs+='5'
            strs+=','
        if (files[15]=='N'):
            strs+='6'
            strs+=','
        for i in range(len(array)):
            strs+=f'{array[i]}'
            if ( i != (len(array) - 1)):
                strs+=' '
        strs+=','
        strs+="PrivateTest"
        strs+='\n'
        print(strs)
        f.write(strs)
f.close()