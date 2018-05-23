from wand.image import Image
from PIL import Image as Image2
import sys

def converter(inputFile):
	with Image(filename=inputFile, resolution=300) as img:
		img.format='jpeg'
		img.save(filename='tempJPG')
		returner('tempJPG')

def returner(inputFile):
	im=Image2.open(inputFile)
	im.save('OutFile',"PDF",resolution=300)

if __name__=="__main__":
	line=raw_input('Please Type in the Input File Name: ')
	converter(line)
