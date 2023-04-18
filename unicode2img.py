import sys 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
from PIL import Image, ImageFont, ImageDraw 
from numpy.core.arrayprint import TimedeltaFormat 
from tqdm import tqdm

font_path = 'fonts' # *.ttf path
file_list = os.listdir(font_path)
fonts = [file for file in file_list if file.endswith(".ttf")] 

co = "0 1 2 3 4 5 6 7 8 9 A B C D E F"
start = "AC00"
end = "D7A3"

co = co.split(" ")

Hangul_Syllables = [a+b+c+d
                    for a in co
                    for b in co
                    for c in co
                    for d in co]

Hangul_Syllables = np.array(Hangul_Syllables)

s = np.where(start == Hangul_Syllables)[0][0]
e = np.where(end == Hangul_Syllables)[0][0]

Hangul_Syllables = Hangul_Syllables[s : e + 1]

w, h = (256,256)

for uni in tqdm(Hangul_Syllables):
    unicodeChars = chr(int(uni, 16))
    path = "output/" + unicodeChars
    os.makedirs(path, exist_ok=True)

    for ttf in fonts:
        font = ImageFont.truetype(font = font_path + "/" + ttf, size=256)
        x, y = font.getsize(unicodeChars)
        theImage = Image.new('RGB', size=(256,256), color='white', )
        theDrawPad = ImageDraw.Draw(theImage)
        theDrawPad.text(((w-x)/2, (h-y)/2), unicodeChars[0], font=font, fill='black')
        msg = path + "/" + ttf[:-4] + "-" + unicodeChars
        
        theImage.save('{}.png'.format(msg))