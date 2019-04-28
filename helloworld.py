#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in9b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in9b.EPD()
    epd.init()
    print("clear")
    epd.Clear(0xFF)
    
    # Drawing on the Horizontal image
    HBlackimage = Image.new('1', (epd2in9b.EPD_HEIGHT, epd2in9b.EPD_WIDTH), 255)  # 298*126
    HRedimage = Image.new('1', (epd2in9b.EPD_HEIGHT, epd2in9b.EPD_WIDTH), 255)  # 298*126
    
    # Horizontal
    print("Drawing")
    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
    font32 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 32)
    drawblack.line((0,100,298,100), fill = 0)
    drawblack.line((266,0,266,198), fill = 0)
    drawblack.text((128, 8), '世界和平', font = font32, fill = 0)
    drawred.text((110, 50), u'薛之谦', font = font24, fill = 0)    
    #heart = Image.open('heart.bmp')
    #HRedimage.paste(heart,(120,80))
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    time.sleep(2)
    
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()