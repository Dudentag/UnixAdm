__author__ = 'Dudentag'
import stat, sys, os, string, commands, textwrap
from PIL import Image, ImageFont, ImageDraw

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

fontname = "Arial.ttf"
fontsize = 11   
j = 0

colorText = "black"
colorOutline = "red"
colorBackground = "white"

commandString = raw_input("file to print:\n")
text = commands.getoutput(commandString)
#text = "  ".join(text)


font = ImageFont.truetype(fontname, fontsize)
width, height = getSize(text, font)#d.textsize(text)

img = Image.new('RGB', (width, height))
d = ImageDraw.Draw(img)

y_text = height

lines = textwrap.wrap(text, width=40)

for line in lines:
    print line
"""
    width, height = font.getsize(line)
    d.text((width / 2, y_text), line, font=font, fill=colorBackground)
    y_text += height
"""
#d.text((width,height), text, fill=colorText)
#d.rectangle((0, 0, width+3, height+3), outline=colorOutline)

img.save("image.jpg")
#draw = ImageDraw.Draw(im)


# use a bitmap font
#font = ImageFont.load("arial.pil")
#draw.text((10, 10), text, font=font)
