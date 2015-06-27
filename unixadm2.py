import stat, sys, os, string, commands
from PIL import Image, ImageFont, ImageDraw

im = Image.open("cat.jpeg")

pattern = raw_input("file to print:\n")
commandString = "sudo cat " + pattern
print commandString
print (commands.getoutput(commandString))

draw = ImageDraw.Draw(im)

# use a bitmap font
#font = ImageFont.load("arial.pil")
#draw.text((10, 10), text, font=font)