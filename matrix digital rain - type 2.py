
# ~ symb = '''
# ~ Identifiable symbols (all are mirror versions unless noted)

# ~ Kanji: "日"
# ~ Katakana: "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
# ~ Missing Katakana: "ｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ" (at least I couldn't find them)
# ~ Numbers: "012345789", "3" is upside down, "4" has underscore, "7" is not mirrored
# ~ Roman: "Z" only, then "THEMATRIX" for the title.
# ~ Punctuation/Arithmetic: ":・."=*+-<>"
# ~ Other: "¦｜" and dashed underscore (╌ but lower down)
# ~ Unknown: Something like ç and something like ﾘ but with an overbar (might be ｸ).
# ~ In total that's around 67 characters.
# ~ '''

# ~ print(symb)


import os
import pygame as pg
from random import choice, randrange
import string
import ctypes


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)
	
    def draw(self, color):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 24)
        self.speed = randrange(2, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]

def screen_size():
	user32 = ctypes.windll.user32
	screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	return screenSize

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = screen_size()
# ~ RES = WIDTH, HEIGHT = 1280, 720
FONT_SIZE = 16
alpha_value = 0

pg.init()
screen = pg.display.set_mode(RES)
surface = pg.Surface(RES)
surface.set_alpha(alpha_value)
clock = pg.time.Clock()

katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
font = pg.font.Font('ms mincho.ttf', FONT_SIZE, bold=True)
green_katakana = [font.render(char, True, (40, randrange(160, 256), 40)) for char in katakana+list(string.digits)+list(':・."=*+-<>')]
lightgreen_katakana = [font.render(char, True, pg.Color('lightgreen')) for char in katakana+list(string.digits)+list(':・."=*+-<>')]

symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]
close = False
qty_tick = 0
mouse_vis = True

while not close:
	screen.blit(surface, (0, 0))
	surface.fill(pg.Color('black'))
	
	for i in pg.event.get():
		if i.type == pg.QUIT:
			close = True
		elif i.type == pg.KEYDOWN:
			if i.key == pg.K_ESCAPE:
				close = True
			if i.key == pg.K_RETURN:
				mouse_vis = not mouse_vis
				pg.mouse.set_visible(mouse_vis)
	
	[symbol_column.draw() for symbol_column in symbol_columns]
	
	if not pg.time.get_ticks() % 20 and alpha_value < 200 and not qty_tick > 5000:
		alpha_value += 5
		surface.set_alpha(alpha_value)
	
	if qty_tick > 5000:
		if alpha_value == 0:
			symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]
			qty_tick = 0
		elif not pg.time.get_ticks() % 10 and alpha_value > 0:
			alpha_value -= 5
			surface.set_alpha(alpha_value)
	else:
		qty_tick += 1
		
	pg.display.flip()
	clock.tick(60)






