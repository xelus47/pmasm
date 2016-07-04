class Pmasm_window():

	terminalHeight=28

	padding=2
	editorHeight=20
	editorWidth=16 # i.e. 16 bytes wide
	navText='(^S)ave;(^C)ompile;(^R)un;(^Q)uit'

	cursor=[0,0]
	scroll=0
	inputStr=''

	editorLines=[]

	commands = [
		3,  # ctrl+C
		8,  # backspace
		83, # del
		17, # ctrl+Q
		18, # ctrl+R
		19, # ctrl+S
		13, # ENTER
		32, # Spacebar
		#59, # semicolon (;) - adds command
		77, # right arrow
		75, # left arrow
		72, # up
		80, # down
	]

	def command_save(self):
		pass

	def command_compile(self):
		pass

	def command_run(self):
		pass

	def command_quit(self):
		self.os.system('cls')
		exit()


	def getChrScope(self,s):
		ls=s.split(',')
		res=[]
		for l in ls:
			start=l.split('-')[0]
			end=l.split('-')[1]
			res+= [chr(n) for n in xrange(ord(start),ord(end)+1)]
		return res

	def __init__(self,fileData=''):
		self.os=__import__('os')
		self.colorama=__import__('colorama')
		from colorama import Fore, Back, Style
		from msvcrt import getch
		self.getch=getch
		self.colorama.init()

		self.Fore=Fore
		self.Back=Back
		self.Style=Style

		self.MINY, self.MAXY = 1, 30
		self.MINX, self.MAXX = 1, 64

		self.scope=self.getChrScope('0-9,A-z')

		self.editorLines = fileData.split('\n')
	
	def cleanup(self):
		self.inputStr=''

		for x in xrange(len(self.editorLines)):
			self.editorLines[x]=self.editorLines[x].replace('.. ','')

	def formatLeading(self,n,length):
		while len(n)<length:
			n='0'+n

		return n

	def placeNav(self,controls,allowed=False):
		controls=controls.split(';')
		padding=self.padding
		#pad={y:2,x:4} # unused
		s=''
		for key in controls:  # padding = 4
			if len(s)+len(key)+3*padding<64:
				s+=key+' '*padding
			else:
				s+='\n'+key
		H=(s.count('\n')+1)*2-1 # amount of space the worded lines take in
		startY=self.MAXY-H-2*padding

		if allowed:
			#print startY
			#pos(startY-2,0)
			print('%s%s%s' % (self.Back.BLUE,self.Style.BRIGHT,self.Fore.WHITE))

			
			VERTICAL = chr(0xBA)
			HORIZONTAL = chr(0xCD)
			TOPLEFT = chr(0xC9)
			BOTLEFT = chr(0xC8)
			TOPRIGHT = chr(0xBB)
			BOTRIGHT = chr(0xBC)

			print('\x1b[1A%s%s%s' %         (TOPLEFT, HORIZONTAL*62,           TOPRIGHT))

			for i in range(padding-1):
				print('\x1b[1A%s%s%s' %     (VERTICAL, ' '*62,                 VERTICAL))

			lines = s.split('\n')
			for i in range(H):
				if bool(i%2):
					print('\x1b[1A%s%s%s' % (VERTICAL, ' '*62,                 VERTICAL))
				else:
					n=i/2
					txt = ' '*padding + lines[n] + ' '*padding
					print('\x1b[1A%s%s%s%s'%(VERTICAL, txt, ' '*(62-len(txt)), VERTICAL))

			for i in range(padding-1):
				print('\x1b[1A%s%s%s' %     (VERTICAL, ' '*62,                 VERTICAL))

			print('\x1b[1A%s%s%s%s' %         (BOTLEFT, HORIZONTAL*62,           BOTRIGHT,  self.Style.RESET_ALL))

			#pos(0,0)
		return H+2*padding

	def show(self):
		getch=self.getch
		Back=self.Back
		Fore=self.Fore
		Style=self.Style


		navHeight = self.placeNav(self.navText)
		displaySize=self.terminalHeight-1-navHeight
		self.os.system('cls')
		for a in range(displaySize):
			print ""
		self.placeNav(self.navText,allowed=True)
		print('\x1b[%sA' % self.terminalHeight)


		byteLocation=0x100
		for y2 in range(self.scroll): # makes sure the line number doens't forget about the strings above the display window
			line=self.editorLines[y2].split(';')[0]
			cleaned = line.replace('\t','').replace(' ','')
			lineByte = [cleaned[i:i+2] for i in xrange(0, len(cleaned), 2)]
			for x2 in range(len(lineByte)):
				byteLocation+=1

		for y in range(self.editorHeight):
			loc = y+self.scroll

			self.lineStr='  0x%s: ' % self.formatLeading(str(hex(byteLocation)).replace('0x',''),4)

			if loc<len(self.editorLines):
				line=self.editorLines[loc].split(';')[0] # we're doing away with comments for now
				cleaned = line.replace('\t','').replace(' ','')
				lineByte = [cleaned[i:i+2] for i in xrange(0, len(cleaned), 2)]

				if len(lineByte)>self.editorWidth:
					self.editorLines = self.editorLines[:y] + lineByte[self.editorWidth:] + self.editorLines[y:]
					lineByte=lineByte[:self.editorWidth]

				for x in range(self.editorWidth):
					if x<len(lineByte):
						if lineByte[x]!='..':
							byteLocation+=1
						if x==self.cursor[1] and y==self.cursor[0]:
							self.lineStr += '%s%s%s%s ' % (Back.BLUE+Fore.WHITE+Style.BRIGHT, Back.MAGENTA+self.inputStr+Back.BLUE, lineByte[x][len(self.inputStr):], Style.RESET_ALL)
						else:
							self.lineStr+=lineByte[x]+' '
					else:
						if x==self.cursor[1] and y==self.cursor[0]:
							self.lineStr += '%s%s%s%s ' % (Back.BLUE+Fore.WHITE+Style.BRIGHT, Back.MAGENTA+self.inputStr+Back.BLUE, '  '[len(self.inputStr):], Style.RESET_ALL)
						else:
							self.lineStr+=' '*3
			else:
				for x in range(self.editorWidth):
					if x==self.cursor[1] and y==self.cursor[0]:
						self.lineStr += '%s%s%s%s ' % (Back.BLUE+Fore.WHITE+Style.BRIGHT, Back.MAGENTA+self.inputStr+Back.BLUE, '  '[len(self.inputStr):], Style.RESET_ALL)
					else:
						self.lineStr+=' '*3

			print self.lineStr


		key = ord(getch())
		if key in self.commands:
			if key == 77 or key == 80 or key==75 or key==72: # arrows
				self.cleanup()


				if key == 77: # -----------------------------  right
					if self.cursor[1]<self.editorWidth:
						self.cursor[1]+=1
				elif key == 80: # down
					if self.cursor[0]<self.editorHeight-1:
						self.cursor[0]+=1
					else:
						self.scroll+=1
				elif key == 75: # left
					if self.cursor[1]>0:
						self.cursor[1]-=1
				elif key == 72: # up
					if self.cursor[0]>0:
						self.cursor[0]-=1
					elif self.cursor[0]==0 and self.scroll>0:
						self.scroll-=1


			elif key == 13 or key == 83 or key == 32 or key == 8: # ---------------- ENTER/DEL/SPACEBAR/BACKSPACE
				y=self.cursor[0]
				x=self.cursor[1]
				loc=y+self.scroll
				if loc<len(self.editorLines):
					line = self.editorLines[loc].split(';')[0]
					if len(self.editorLines[loc].split(';'))>1:
						comment=self.editorLines[loc].split(';')[1]
					else:
						comment=''
					cleaned = line.replace('\t','').replace(' ','')
					lineByte = [cleaned[i:i+2] for i in xrange(0, len(cleaned), 2)]
					if x<len(lineByte):												# cursor pointing at a byte
						if key==32: 													# if space place inputStr
							if len(self.inputStr)==0:										# format inputStr
								lineByte=lineByte[:x]+['..']+lineByte[x:]			# add an empty byte space
								self.editorLines[loc]=' '.join(lineByte)					# save
								return None
							if len(self.inputStr)==1:										# copy the hexadecimal place
								self.inputStr+=lineByte[x][1]
								return None
							lineByte[x]=self.inputStr									# do place inputStr
							self.editorLines[loc]=' '.join(lineByte) 						# save
							self.cursor[1]+=1												# move cursor to the right
							self.inputStr=''
						elif key==13:													# elif enter make new line
							self.cursor[0]+=1												# move cursor one line down
							self.cursor[1]=0													# move cursor to very left
							lineSplit=[' '.join(lineByte[:x]),' '.join(lineByte[x:])] # define the two new lines
							self.editorLines=self.editorLines[:loc] + lineSplit + self.editorLines[loc+1:] # save
						else:															# else del remove byte
							if key==8:
								if x>0:												# backspace
									x-=1
									self.cursor[1]-=1
								else:
									if self.cursor[0]>0:
										self.cursor[0]-=1
									return None
							lineByte=lineByte[:x] + lineByte[x+1:]					# delete
							self.editorLines[loc]=' '.join(lineByte)						# save
					else: # cursor is to the right of the byte line
						if key==32:
							if len(self.inputStr)==0:										# format inputStr
								lineByte=lineByte[:x]+['..']+lineByte[x:]			# add an empty byte space
								self.editorLines[loc]=' '.join(lineByte)					# save
								return None
							if len(self.inputStr)==1:										# add '0'
								self.inputStr+='0'
								return None
							lineByte.append(self.inputStr)									# stick inputStr behind the line
							self.editorLines[loc]=' '.join(lineByte) 						# save
							self.cursor[1]+=1												# move cursor to the right
							self.inputStr=''
						elif key==13:													# enter
							self.cursor[0]+=1												# new empty line
							self.cursor[1]=0
							self.editorLines=self.editorLines[:loc+1] + [''] + self.editorLines[loc+1:]
						else: 															# del
							if loc+1<len(self.editorLines):
								nextLine=self.editorLines[loc+1]								# combine this and the next line
								nextLine2=nextLine.split(';')[0]
								clean=nextLine2.replace('\t','').replace(' ','')
								nextByteLine=[clean[i:i+2] for i in xrange(0, len(clean), 2)]
								lineByte+=nextLine
								self.editorLines[loc]=' '.join(lineByte)
								self.editorLines=self.editorLines[:loc] + self.editorLines[loc+1:]		# remove the next line
							else:
								pass

				else: # y =< editorLines
					if key==32: # --------------------------------- SPACE
						if len(self.inputStr)==0:
							self.inputStr='..'
						if len(self.inputStr)==1:
							self.inputStr+='0'
						while not y<len(self.editorLines):
							self.editorLines.append('.. ')
						self.editorLines[y]=self.inputStr
						for x in range(len(self.editorLines)):
							self.editorLines[x]=self.editorLines[x].replace('.. ','')
					else:
						pass
			elif key == 19: # ---------------------------------- CTRL+S
				self.command_save(self)
			elif key == 3: # ----------------------------------- CTRL+C
				self.command_compile(self)
			elif key == 17: # ---------------------------------- CTRL+Q
				self.command_quit()
			elif key == 18:
				self.command_run(self)
			else:
				self.cleanup()
		else:
			if len(self.inputStr)<2 and chr(key) in self.scope:
				self.inputStr+=chr(key)
