from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import cv2
import random

ImgPath = './VOC2012/JPEGImages/'
AnnoPath = './VOC2012/Annotations/'
ProcessedPath = './VOC2012/test/'
if not os.path.exists(ProcessedPath):
    os.makedirs(ProcessedPath)
imagelist = os.listdir(ImgPath)
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
for image in imagelist:

    print('a new image:', image)
    image_pre, ext = os.path.splitext(image)
    imgfile = ImgPath + image
    xmlfile = AnnoPath + image_pre + '.xml'
    raw_img = cv2.imread(imgfile)

    DomTree = xml.dom.minidom.parse(xmlfile)
    annotation = DomTree.documentElement

    filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]
    filename = filenamelist[0].childNodes[0].data
    objectlist = annotation.getElementsByTagName('object')
    for objects in objectlist:
        # print objects
        namelist = objects.getElementsByTagName('name')
        # print 'namelist:',namelist
        name_i = 0
        name_end = []
        for objectname in namelist:
            name_end.append(namelist[name_i].childNodes[0].data)
            name_i += 1
        bndbox = objects.getElementsByTagName('bndbox')
        box_i = 0
        box_end = []
        for box in bndbox:
            x1_list = box.getElementsByTagName('xmin')
            x1 = int(x1_list[0].childNodes[0].data)
            y1_list = box.getElementsByTagName('ymin')
            y1 = int(y1_list[0].childNodes[0].data)
            x2_list = box.getElementsByTagName('xmax')
            x2 = int(x2_list[0].childNodes[0].data)
            y2_list = box.getElementsByTagName('ymax')
            y2 = int(y2_list[0].childNodes[0].data)
            w = x2 - x1
            h = y2 - y1
            print(name_end[box_i])
            print([x1, y1, x2, y2])
            rgb_r = random.randint(0, 255)
            rgb_g = random.randint(0, 255)
            rgb_b = random.randint(0, 255)
            cv2.rectangle(raw_img, (x1, y1), (x2, y2), (rgb_b, rgb_g, rgb_r), 1)
            cv2.putText(raw_img, name_end[box_i], (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                        (rgb_b, rgb_g, rgb_r), 2)
            box_i += 1
            box_end.append([x1, y1, x2, y2])
    cv2.imshow('image', raw_img)
    cv2.waitKey(0)
    cv2.imwrite(ProcessedPath + image, raw_img)
