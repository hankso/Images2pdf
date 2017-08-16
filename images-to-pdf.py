#!/usr/bin/python
'''
A small script that convert image(s) to pdf losslessly using only \33[1m\33[4mos\33[0m, \33[1m\33[4msys\33[0m and \33[1m\33[4mimg2pdf\33[0m (https://github.com/josch/img2pdf)

Simply input source image(s) (in order) and output pdf name, then the pdf will quickly be generated. Notice that '-o' is not neccessary but recommanded:

>>> python images-to-pdf.py 1.png 2.png -o bar123.pdf

or :

>>> python images-to-pdf.py imgs/*.jpg result.pdf
'''

import img2pdf
import sys
import os

#>>> print(sys.argv)
#    ['images-to-pdf.py', '****.jpg', '****.pdf']

paras = sys.argv[1:]


if 'help' in paras or not paras:
    print(__doc__)
    sys.exit()


fromFile = []
for para in paras:
    if para[-4:] in ('.jpg', '.png', '.svg',):
        fromFile.append(paras.pop(paras.index(para)))
if not len(fromFile):
    print('img2pdf:\n    Error: no input images.\n    Conversion terminated.')
    sys.exit()


toFile = None
if '-o' in paras:
    try:
        toFile = paras.pop(paras.index('-o')+1)
    except IndexError, e:
        print('img2pdf:\n    Error: no output names.\n    Conversion terminated.')
        sys.exit()
for para in paras:
    if para.endswith('.pdf'):
        toFile = para
if not toFile:
    print('Congratulations! You just triggered all of my "if" sentences and travelled through my code and did nothing!\nRTFM pls......')
    print(__doc__)
    sys.exit()


images = []
for img in fromFile:
    if '*' in img:
        i, j = img.split('*')[0], img.split('*')[-1]
        i = os.path.dirname(i)
        for star_img in os.listdir(i):
            if star_img.endswith(j):
                images.append(i+star_img)
    else:
        images.append(img)

with open(toFile, 'wb') as f:
    f.write(img2pdf.convert(images))

print('Succesfully convert')
for img in images:
    print('    '+os.path.abspath(img))
print('To:')
print('    '+os.path.abspath(toFile))

