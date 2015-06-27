__author__ = 'Dudentag'
import stat, sys, os, string, commands
from PIL import Image
from PIL import ImageDraw
from MainFunctions import MainFunctions

mainFunctions = MainFunctions()

def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

mainFunctions

if __name__ == '__main__':

    fontname = "Arial.ttf"
    fontsize = 11

    pattern = raw_input("file to print:\n")
    commandString = "cat " + pattern

    text = commands.getoutput(commandString)

    print text
    """
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"

    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, height/2), text, fill=colorText, font=font)
    d.rectangle((0, 0, width+3, height+3), outline=colorOutline)

    img.save("image.jpeg")
    """