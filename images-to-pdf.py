#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A small script that convert image(s) to pdf losslessly using only \33[1m\33[4mos\33[0m, \33[1m\33[4msys\33[0m and \33[1m\33[4mimg2pdf\33[0m (https://github.com/josch/img2pdf)

Simply input source image(s) (in order) and output pdf name, then the pdf will quickly be generated. Notice that '-o' is not neccessary but recommanded\n
'''

HELP = "try:\n\
>>> python images-to-pdf.py 1.png 2.png -o bar123.pdf --delete-source\n\
or :\n\
>>> python images-to-pdf.py imgs/*.jpg result.pdf -d
"

__doc__ += HELP

import img2pdf
import sys
import os

#>>> print(sys.argv)
#    ['images-to-pdf.py', '****.jpg', '****.pdf']
paras = sys.argv[1:]

if not paras:
    print(__doc__)

elif '-h' or 'help' in paras:
    print(HELP)

else:
    del_src = True if ('-d' in paras or '--delete-source' in paras) else False

    fromFile = []
    for para in paras:
        if para[-4:] in ('.jpg', '.png', '.svg',):
            fromFile.append(paras.pop(paras.index(para)))
    if len(fromFile) == 0:
        print('img2pdf:\n    Error: no input images.\n    Conversion terminated.')
        sys.exit()

    toFile = None
    if '-o' in paras:
        try:
            toFile = paras.pop(paras.index('-o')+1)
        except IndexError:
            print('img2pdf:\n    Error: no output names.\n    Default name used.')
    else:
        for para in paras:
            if para.endswith('.pdf'):
                toFile = para
    toFile = toFile if toFile else 'default_name.pdf'
    del para, paras

    path_list = []
    for img in fromFile:
        if '*' in img:
            i, j = img.split('*')[0], img.split('*')[-1]
            i = os.path.dirname(i)
            for star_img in os.listdir(i):
                if star_img.endswith(j):
                    path_list.append(i + star_img)
            del i, j, star_img
        else:
            path_list.append(img)
    del fromFile

    img_list = []
    del_list = []
    from PIL import Image
    for img in path_list:
        try:
            img = Image.open(img)
            if img.width > 14399:
                ratio = 14399.0/img.width
                img = img.resize((14399, int(ratio*img.height)))
                img.save(img.filename)
            if img.height/14399:
                for i in range(img.height/14399+1):
                    img.crop((0, i*14399, img.width, min((i+1)*14399, img.height))).save(img.filename[:-4]+str(i)+'.png')
                    img_list.append(img.filename[:-4]+str(i)+'.png')
                    del_list.append(img.filename[:-4]+str(i)+'.png')
            else:
                img_list.append(img.filename)
        except:
            pass
    del i


    with open(toFile, 'wb') as f:
        f.write(img2pdf.convert(img_list))
    for _ in del_list + path_list if del_src else []:
        os.remove(_)
    del img_list, del_list, del_src


    print('\33[1mSuccesfully convert\33[0m')
    for img in path_list:
        print('    '+os.path.abspath(img))
    print('\33[1mTo:\33[0m')
    print('    '+os.path.abspath(toFile))
