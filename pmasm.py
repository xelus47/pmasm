import argparse,os
from msvcrt import getch

import colorama
from colorama import Fore, Back, Style
colorama.init()

from pmasmclass import Pmasm_window

MINY, MAXY = 1, 30
MINX, MAXX = 1, 64

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

parser = argparse.ArgumentParser(description='Converts binary code in a .asm file to an executable .com binary file')
parser.add_argument('file', help='Assembly file')
#parser.add_argument('-s','--step', help='Pauses between each step so you can follow the action',action='count')
#parser.add_argument('-d','--debug', help='Extra info while running for debugging purposes',action='count')
parser.add_argument('-r','--run',help='Run binary file after compiling',action='count')
#parser.add_argument('-m','--matrix',help='Enter the matrix',action='count')
parser.add_argument('-e','--edit',help='Edit file (super cool)',action='count')
args = parser.parse_args()


def hexcompile(data):
	data=data.replace(' ','').replace('\t','') # collapse
	# TODO
	# strip comments (';')
	#
	lines = data.split('\n')
	data=''
	for line in lines:
		line = line.split(';')[0]
		data+=line

	data=data.replace('\n','')
	try:
		hexcodes=[int(data[i:i+2],base=16) for i in xrange(0, len(data), 2)]
	except:
		print("Error in file format. Did you make sure ALL bytes were hex codes?")
		exit()
	return hexcodes

def save(codes,file):
	for c in codes:
		file.write(chr(c))

filePath = args.file
filename,fileext=os.path.splitext(filePath)
if fileext=='':
	fileext='.asm'
	filePath+='.asm'

if not os.path.isfile(filePath):
	print("Not a valid file")
	exit()
else:
	outputFile='%s.com' % filename


def command_save(self):
	code = '\n'.join(self.editorLines)
	#hexcodes=hexcompile(code)
	f2=open(filePath,'w')
	f2.write(code)
	f2.close()

def command_compile(self):
	code = '\n'.join(self.editorLines)
	hexcodes=hexcompile(code)
	f2=open(outputFile,'w')
	save(hexcodes,f2)
	f2.close()

def command_run(self):
	self.command_compile(self)
	self.os.system('cls')
	self.os.system(outputFile)
	a=raw_input('%s has been executed' % outputFile)

if True: # if bool(args.edit)
	f1=open(filePath,'r')
	dat=f1.read()
	f1.close()
	window = Pmasm_window(dat)
	window.command_save=command_save
	window.command_compile=command_compile
	window.command_run=command_run
	while True:
		window.show()
else:
	f1=open(filePath,'r')
	dat=f1.read()
	f1.close()
	hexcodes=hexcompile(dat)
	f2=open(outputFile,'w')
	save(hexcodes,f2)
	f2.close()

	if not bool(args.run):
		print('Saved as %s' % outputFile)
	else:
		os.system(outputFile)
	exit()