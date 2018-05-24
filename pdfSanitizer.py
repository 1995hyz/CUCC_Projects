from wand.image import Image
from PIL import Image as Image2
import io
import PyPDF2
import sys

if __name__=="__main__":
	line=raw_input('Please Type in the Input File Name: ')
	targetPDF=PyPDF2.PdfFileReader(line)
	merger=PyPDF2.PdfFileMerger()
	for i in xrange(targetPDF.getNumPages()):
		splitPDF=PyPDF2.PdfFileWriter()
		splitPDF.addPage(targetPDF.getPage(i))
		splitPdfBuffer=io.BytesIO()
		imgBuffer=io.BytesIO()
		outPdfBuffer2=io.BytesIO()
		splitPDF.write(splitPdfBuffer)
		splitPdfBuffer.seek(0)
		img=Image(file=splitPdfBuffer,resolution=500)
		img.format='jpeg'
		img.save(imgBuffer)
		imgBuffer.seek(0)
		im=Image2.open(imgBuffer)
		im.save(outPdfBuffer2,"PDF",resolution=500)
		outPdfBuffer2.seek(0)
		merger.append(outPdfBuffer2)
	merger.write(line)
