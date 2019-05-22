import pygame, sys, time, random, os, pyautogui, threading
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
	
pygame.init()
pygame.font.init()

pygame.display.set_caption('SnakeGame')
white = (255, 255, 255)
position = [ [ 80, 80 ] ]
past_position = [ [ 80, 80 ] ]
randx = random.randrange(70, 780)
randy = random.randrange(70, 580)
randx -= randx % 20
randy -= randy % 20
rng = n = the_score = past_time = don = tmp = tt = dt = line_num = mtf = delay_time = TIME = 0
temp = 1
level = ''
hnd_direction = ''
past_dir = ''
img = []

for i in range(10):
	image = pygame.image.load('Images/' + str(i) + '.png')
	img.append(pygame.transform.scale(image, (30, 60)))
image = pygame.image.load('Images/' + 'colon.png')
img.append(pygame.transform.scale(image, (30, 60)))

you_died = pygame.image.load('Images/' + 'you_died.png')
you_died = pygame.transform.scale(you_died, (1160, 640))

FILE_DATA = list()

RECT = list()
RECT.append(pygame.rect.Rect(position[n][0], position[n][1], 20, 20))

EDGE = list()
EDGE.append(pygame.rect.Rect(0, 0, 1160, 20))
EDGE.append(pygame.rect.Rect(0, 0, 20, 640))
EDGE.append(pygame.rect.Rect(0, 620, 1160, 20))
EDGE.append(pygame.rect.Rect(820, 0, 20, 640))
EDGE.append(pygame.rect.Rect(880, 0, 20, 640))
EDGE.append(pygame.rect.Rect(1140, 0, 20, 640))
EDGE.append(pygame.rect.Rect(900, 540, 240, 20))
EDGE.append(pygame.rect.Rect(900, 105, 240, 20))


STICK = list()
for i in range(1600):
	STICK.append(pygame.rect.Rect(840, 20 + (0.375 * i), 40, 0.375))

class Player(object):
	def draw(self):
		global n
		i = 0
		r = 0
		b = 1
		for i in range(n + 1):
			if i == 0:
				pygame.draw.rect(screen, (0, 128, 255), RECT[i])
			else:
				r = r + 1
				if r == 51:
					r = 1
					b = b * -1

				if b == 1:
					pygame.draw.rect(screen, (5 * r, 128, 255), RECT[i])
				elif b == -1:
					pygame.draw.rect(screen, (260 - (5 * r), 128, 255), RECT[i])

	def handle_keys(self):
		global hnd_direction
		global past_dir
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			if not past_dir == 'right':
				hnd_direction = 'left'
				past_dir = 'left'
		elif key[pygame.K_RIGHT]:
			if not past_dir == 'left':
				hnd_direction = 'right'
				past_dir = 'right'
		elif key[pygame.K_UP]:
			if not past_dir == 'down':
				hnd_direction = 'up'
				past_dir = 'up'
		elif key[pygame.K_DOWN]:
			if not past_dir == 'up':
				hnd_direction = 'down'
				past_dir = 'down'

	def move(self, hnd_direction):
		global position, temp
		for i in range(n + 1):
			if i != 0 and n == temp:
				past_position.append([position[i][0], position[i][1]])
				temp = temp + 1

			if i != n:
				past_position[i][0] = position[i][0]
				past_position[i][1] = position[i][1]

			if i == 0:
				if hnd_direction == 'left':
					position[i][0] = position[i][0] - 20
				elif hnd_direction == 'right':
					position[i][0] = position[i][0] + 20
				elif hnd_direction == 'up':
					position[i][1] = position[i][1] - 20
				elif hnd_direction == 'down':
					position[i][1] = position[i][1] + 20
			
			else:
				position[i][0] = past_position[i - 1][0]
				position[i][1] = past_position[i - 1][1]

	def append(self):
		global position, n
		n = n + 1
		RECT.append(pygame.rect.Rect(position[n][0], position[n][1], 20, 20))

	def crash(self):
		global RECT, n, position
		for i in range(n + 1):
			for r in range(i + 1, n + 1):
				if RECT[i][0] == RECT[r][0] and RECT[i][1] == RECT[r][1]:
					return 1

		if position[0][0] <= 0 or position[0][1] <= 0 or position[0][0] >= 820 or position[0][1] >= 620:
			return 1

		return 0
		
class Food(object):
	def __init__(self):
		self.rect = (pygame.rect.Rect(randx, randy, 20, 20))

	def draw(self):
		pygame.draw.rect(screen, (128, 255, 0), self.rect)

	def move(self):
		global randx, randy, RECT

		length = len(RECT)

		while True:
			same = 0
			randx = random.randrange(120, 780)
			randx -= randx % 20
			randy = random.randrange(120, 580)
			randy -= randy % 20
			for i in range(length):
				if RECT[i][0] == randx and RECT[i][1] == randy:
					same = True
					break
			if same == True:
				continue
			break

class SelectLevel(object):
	def sizedButton(self, root, x, y, lvl):
		f = Frame(self.root, width = 100, height = 35)
		f.pack_propagate(0)
		f.place(x = x, y = y)

		if lvl == 'easy':
			self.btn_easy = Button(f, text = 'Easy', command = self.easy)
			self.btn_easy.pack(fill = BOTH, expand = 1)
			self.btn_easy.bind("<Button-1>", lambda e: self.easy())
			self.btn_easy.bind("<Return>", lambda e: self.easy())

		elif lvl == 'normal':
			self.btn_normal = Button(f, text = 'Normal', command = self.normal)
			self.btn_normal.pack(fill = BOTH, expand = 1)
			self.btn_normal.bind("<Button-1>", lambda e: self.normal())
			self.btn_normal.bind("<Return>", lambda e: self.normal())

		elif lvl == 'hard':
			self.btn_hard = Button(f, text = 'Hard', command = self.hard)
			self.btn_hard.pack(fill = BOTH, expand = 1)
			self.btn_hard.bind("<Button-1>", lambda e: self.hard())
			self.btn_hard.bind("<Return>", lambda e: self.hard())

	def background(self):
		def close_onclick():
			sys.exit()

		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", close_onclick)

		self.root.focus_force()

		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = (ws / 2) - (1160 / 2)
		y = (hs / 2) - (640 / 2)

		self.root.geometry('%dx%d+%d+%d' % (1160, 640, x, y))
		self.root.geometry('1160x640')

		self.bgimg = PhotoImage(file = 'Images/' + 'BackGround.png')
		self.bglbl = Label(image = self.bgimg)
		self.bglbl.place(x = 0, y = -2)

		self.sizedButton(self.root, 250, 450, 'easy')
		self.sizedButton(self.root, 530, 450, 'normal')
		self.sizedButton(self.root, 810, 450, 'hard')

		self.lbl = Label(self.root, text = 'Select the Level')
		self.lbl.config(font = ('Comic Sans MS', 20))
		self.lbl.place(x = 580, y = 380, anchor = 'center')

		self.root.mainloop()

	def easy(self):
		global level
		self.root.destroy()
		level = 'easy'

	def normal(self):
		global level
		self.root.destroy()
		level = 'normal'

	def hard(self):
		global level
		self.root.destroy()
		level = 'hard'

class BeforePlaying(object):
	def before_start(self):
		global FILE_DATA, line_num, level
		if level == 'easy':
			file = open('TextFiles/' + 'score_easy.txt', 'r', encoding = 'utf-8')
		elif level == 'normal':
			file = open('TextFiles/' + 'score_normal.txt', 'r', encoding = 'utf-8')
		elif level == 'hard':
			file = open('TextFiles/' + 'score_hard.txt', 'r', encoding = 'utf-8')

		while True:
			line = file.readline()
			FILE_DATA.append(line.split('/'))
			' '.join(line)
			if not line:
				break
			FILE_DATA[line_num][1] = int(FILE_DATA[line_num][1])
			line_num += 1
		file.close()
		for i in range(0, len(FILE_DATA) - 1):
			for j in range(0, len(FILE_DATA) - 2 - i):
				if FILE_DATA[j][1] < FILE_DATA[j + 1][1]:
					tmp = FILE_DATA[j]
					del FILE_DATA[j]
					FILE_DATA.insert(j + 1, tmp)

class Option(object):
	def draw_edge(self):
		global EDGE
		for i in range(len(EDGE)):
			pygame.draw.rect(screen, (0, 0, 0), EDGE[i])

		pygame.draw.rect(screen, (20, 20, 20), pygame.rect.Rect(900, 560, 240, 60))

	def draw_stick(self):
		for i in range(0, 1600):
			if i < 0:
				i = 0
			pygame.draw.rect(screen, (250, (0.0390625 * i), (0.0390625 * i)), STICK[i])

	def draw_white(self, time):
		if time * 75 >= 600000:
			return 1
		pygame.draw.rect(screen, white, pygame.rect.Rect(840, 20, 40, time / 1000 * 75 ))

	def draw_rank(self):
		global line_num
		pygame.draw.rect(screen, (216, 226, 220), pygame.rect.Rect(900, 125, 240, 83))
		pygame.draw.rect(screen, (255, 229, 217), pygame.rect.Rect(900, 208, 240, 83))
		pygame.draw.rect(screen, (255, 202, 212), pygame.rect.Rect(900, 291, 240, 83))
		pygame.draw.rect(screen, (244, 172, 183), pygame.rect.Rect(900, 374, 240, 83))
		pygame.draw.rect(screen, (157, 129, 137), pygame.rect.Rect(900, 457, 240, 83))
		text = pygame.font.Font('C:\\Windows\\Fonts\\HANSaleB.ttf', 40)
		for i in range(5):
			textSurface = text.render(str(i + 1), True, (0, 0, 0))
			textRect = textSurface.get_rect()
			textRect.center = (915, 166.5 + (83 * i))
			screen.blit(textSurface, textRect)
			
		if line_num > 5:
			line_num = 5

		text = pygame.font.Font('C:\\Windows\\Fonts\\HANSaleB.ttf', 35)
		for i in range(line_num):
			rank_str = ('{}'.format(FILE_DATA[i][0]))
			textSurface = text.render(rank_str, True, (0, 0, 0))
			textRect = textSurface.get_rect()
			textRect.center = (1030, 150 + (83 * i))
			screen.blit(textSurface, textRect)

		text = pygame.font.Font('C:\\Windows\\Fonts\\HANSaleB.ttf', 35)
		for i in range(line_num):
			rank_str = ('{}{}'.format(FILE_DATA[i][1], '점'))	
			textSurface = text.render(rank_str, True, (0, 0, 0))
			textRect = textSurface.get_rect()
			textRect.center = (1030, 180 + (83 * i))
			screen.blit(textSurface, textRect)

	def time_score(self, time):
		global past_time, the_score
		per_time = time - time % 100

		if level == 'easy':
			if per_time <= 30000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 3)
					past_time = per_time
			elif per_time > 30000 and per_time <= 90000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 5)
					past_time = per_time
			else:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 7)
					past_time = per_time

		elif level == 'normal':
			if per_time <= 30000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 7)
					past_time = per_time
			elif per_time > 30000 and per_time <= 90000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 10)
					past_time = per_time
			else:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 13)
					past_time = per_time

		elif level == 'hard':
			if per_time <= 30000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 13)
					past_time = per_time
			elif per_time > 30000 and per_time <= 90000:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 16)
					past_time = per_time
			else:
				if per_time - past_time >= 100:
					the_score += round((per_time - past_time) / 100 * 20)
					past_time = per_time

	def eat_score(self, time):
		global the_score
		per_time = time - time % 100

		if level == 'easy':
			if per_time <= 30000:
				the_score += 150
			elif per_time > 30000 and per_time <= 90000:
				the_score += 300
			else:
				the_score += 500

		elif level == 'normal':
			if per_time <= 30000:
				the_score += 500
			elif per_time > 30000 and per_time <= 90000:
				the_score += 700
			else:
				the_score += 1000

		elif level == 'hard':
			if per_time <= 30000:
				the_score += 100
			elif per_time > 30000 and per_time <= 90000:
				the_score += 1400
			else:
				the_score += 2000

	def print_time(self, time):
		time = round(time / 10)
		MTime = time // 100 // 60
		STime = time // 100 % 60

		Min_1 = MTime // 10
		Min_2 = MTime %  10
		Sec_1 = STime // 10
		Sec_2 = STime %  10
		Msec_1 = time % 100 // 10
		Msec_2 = time % 10
		
		screen.blit(img[Min_1], (900, 560))
		screen.blit(img[Min_2], (930, 560))
		screen.blit(img[10], (960, 560))
		screen.blit(img[Sec_1], (990, 560))
		screen.blit(img[Sec_2], (1020, 560))
		screen.blit(img[10], (1050, 560))
		screen.blit(img[Msec_1], (1080, 560))
		screen.blit(img[Msec_2], (1110, 560))

	def print_score(self):  
		global the_score
		image = pygame.image.load('Images/' + 'your_score_is.png')
		image = pygame.transform.scale(image, (240, 35))
		screen.blit(image, (900, 20))

		text = pygame.font.Font('C:\\Windows\\Fonts\\comici.ttf', 50)
		textSurface = text.render(str(the_score), True, (0, 0, 0))
		textRect = textSurface.get_rect()
		textRect.center  = (1020, 77.5)
		screen.blit(textSurface, textRect)

class Gameover(object):
	def start(self):
		def close_onclick():
			sys.exit()

		self.root = Tk()
		self.root.title('Gameover')

		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = (ws/2) - (215/2)
		y = (hs/2) - (65/2)

		self.root.geometry('%dx%d+%d+%d' % (215, 65, x, y))
		self.root.geometry('215x65')

		self.root.protocol("WM_DELETE_WINDOW", close_onclick)

		self.lbl = Label(self.root, text = 'Enter your name')
		self.lbl.grid(row = 0)

		self.usertext = StringVar()
		self.entry = Entry(self.root, textvariable = self.usertext)
		self.entry.grid(row = 1, column = 0)
		self.entry.focus()

		self.root.focus_force()

		self.root.bind('<Return>', self.check_length)

		self.btn = Button(self.root, text = 'OK')
		self.btn.bind('<Button-1>', self.check_length)
		self.btn.grid(row = 1, column = 1)

		self.lbl = Label(self.root, text = '이름 길이는 1~9자 내로 하십시오')
		self.lbl.grid(row = 2)

		self.counter = 0

		self.root.mainloop()

	def check_length(self, event):
		if len(self.usertext.get().strip()) < 10:
			if len(self.usertext.get().strip()) == 0:
				self.errorbox()
			else:
				self.save()
		else:
			self.errorbox()

	def errorbox(self):
		messagebox.showinfo('Error', '이름 길이는 1~9자 내로 하십시오')

	def save(self):
		global the_score, FILE_DATA, level

		data = [self.usertext.get().strip(), str(the_score)]

		FILE_DATA.insert(len(FILE_DATA) - 1, data)
		FILE_DATA[len(FILE_DATA) - 2][1] = int(FILE_DATA[len(FILE_DATA) - 2][1])

		for i in range(0, len(FILE_DATA) - 1):
			for j in range(0, len(FILE_DATA) - 2 - i):
				if FILE_DATA[j][1] < FILE_DATA[j + 1][1]:
					poped_data = FILE_DATA[j]
					del FILE_DATA[j]
					FILE_DATA.insert(j + 1, poped_data)

		if level == 'easy':
			file = open('TextFiles/' + 'score_easy.txt', 'w', encoding = 'utf-8')
		elif level == 'normal':
			file = open('TextFiles/' + 'score_normal.txt', 'w', encoding = 'utf-8')
		elif level == 'hard':
			file = open('TextFiles/' + 'score_hard.txt', 'w', encoding = 'utf-8')

		for i in range(len(FILE_DATA) - 1):
			file.write('{}{}{}\n'.format(FILE_DATA[i][0], '/', FILE_DATA[i][1]))
		file.close()
		self.root.destroy()

class Regame(object):
	def start(self):
		def close_onclick():
			sys.exit()

		self.root = Tk()
		self.root.title('SnakeGame')

		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = (ws/2) - (220/2)
		y = (hs/2) - (60/2)

		self.root.geometry('%dx%d+%d+%d' % (220, 60, x, y))
		self.root.geometry('220x60')

		self.root.focus_force()

		self.root.protocol("WM_DELETE_WINDOW", close_onclick)

		self.lbl = Label(self.root, text = 'Restart the game?')
		self.lbl.grid(row = 0, column = 1)

		self.btnY = Button(self.root, text = 'YES', width = 7, height = 2)
		self.btnY.grid(row = 1, column = 0)
		self.btnY.bind("<Button-1>", lambda e: self.yes())
		self.btnY.bind("<Return>", lambda e: self.yes())
		
		self.btnN = Button(self.root, text = 'NO', width = 7, height = 2)
		self.btnN.grid(row = 1, column = 2)
		self.btnN.bind("<Button-1>", lambda e: self.no())
		self.btnN.bind("<Return>", lambda e: self.no())

		self.counter = 0

		self.root.mainloop()

	def yes(self):
		self.root.destroy()

	def no(self):
		self.root.destroy()
		pygame.quit()
		sys.exit()

def Game():
	pygame.mixer.music.load('Musics/' + 'Snack Time.wav')
	pygame.mixer.music.play(-1)
	APPLE = pygame.mixer.Sound('Musics/' + 'Apple Bit Sound.wav')
	global don, rng, dt, tmp, tt, level, delay_time, TIME
	b = BeforePlaying()
	b.before_start()
	pyautogui.moveTo(1700, 540)

	clock = pygame.time.get_ticks()
	start = time.time()
	while True:
		s = time.time()
		EATEN = False
		p = Player()
		f = Food()
		o = Option()
		g = Gameover()
		r = Regame()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		screen.fill(white)
		p.handle_keys()
		p.move(hnd_direction)
		p.draw()
		f.draw()
		o.draw_edge()
		o.draw_rank()
		o.draw_stick()
		don = o.draw_white(TIME)

		if p.crash() == 1 or don == 1:
			pygame.mixer.music.stop()
			screen.fill(white)
			screen.blit(you_died, (0, 0))
			pygame.display.update()
			pygame.mixer.music.load('Musics/' + 'Crash Sound.wav')
			pygame.mixer.music.play(0)
			time.sleep(2)
			pygame.quit()
			g.start()
			r.start()
			return 0

		if position[0][0] == f.rect.x and position[0][1] == f.rect.y:
			APPLE.play()
			f.move()
			position.append([RECT[n].x, RECT[n].y])
			p.append()
			end = time.time()
			tmp = tmp + round(end - start, 2)
			tt = tt + 1
			start = time.time()
			if level == 'easy':
				rng = rng + 4000
			elif level == 'normal':
				rng = rng + 3200
			elif level == 'hard':
				rng = rng + 2500
			EATEN = True
	
		for i in range(n + 1):
			RECT[i] = pygame.rect.Rect(position[i][0], position[i][1], 20, 20)
		
		ticks_time = pygame.time.get_ticks() - clock

		o.time_score(ticks_time)
		o.print_time(ticks_time)
		o.print_score()

		if EATEN == True:
			o.eat_score(ticks_time)

		TIME = ticks_time - rng;
		if TIME < 0:
			rng = rng + TIME
			TIME = 0

		if dt == 0 and ticks_time >= 30000:
			delay_time = delay_time - 5
			dt = 1
		elif dt == 1 and ticks_time >= 90000:
			delay_time = delay_time - 5
			dt = 2

		print(FILE_DATA)
		pygame.display.flip()
		pygame.time.delay(delay_time)
		e = time.time()

while True:
	s = SelectLevel()
	s.background()
	if level == 'easy':
		delay_time = 50
	elif level == 'normal':
		delay_time = 40
	elif level == 'hard':
		delay_time = 30
	else:
		pygame.quit()
		sys.exit()

	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (380, 220)
	screen = pygame.display.set_mode((1160, 640), 0, 0)
	Game()
	os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)