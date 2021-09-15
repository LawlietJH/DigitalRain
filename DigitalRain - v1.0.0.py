
# By: LawlietJH
# Digital Rain

from datetime      import datetime
# ~ import threading
# ~ import binascii						# hexlify y unhexlify
# ~ import psutil
import pygame						# python -m pip install pygame
import ctypes						# windll Manipulacion de DLLs de Windows
import random						# choice, randint
# ~ import base64
import time							# sleep
# ~ import math
# ~ import bz2
import copy
import os							# path, mkdir, environ, system

#=======================================================================

# pip install pywin32 ==================================================
# ~ from win32com.shell import shell
import win32api			as WA
import win32con			as WC
import win32gui			as WG
# ~ import win32ui			as WU
# ~ import win32net			as WN
# ~ import win32com			as WCM
# ~ import win32process		as WP
# ~ import win32security	as WS
# ~ import win32clipboard	as WCB
import win32console		as WCS
#=======================================================================

TITULO      = 'Digital Rain'		# Nombre
__version__ = 'v1.0.0'				# Version
__author__  = 'LawlietJH'			# Desarrollador

#=======================================================================
#=======================================================================
#=======================================================================



run_command = lambda Comando: os.popen(Comando).read()



class Scripts:
	
	min_vbs = """
		\r	' VBS Script para Minimizar todas las ventanas.
		\r	Set var = CreateObject("Shell.Application")
		\r	var.MinimizeAll
	"""



class Utils:
	
	def screenSize():
		user32 = ctypes.windll.user32
		screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		return screenSize
	
	def minimizeWindowCMD(): WG.ShowWindow(WG.GetForegroundWindow(), WC.SW_MINIMIZE)
	
	def minimizeAll():
		temp_path = os.getenv('TEMP') + '\\_odin_\\'					# Obtiene la ruta de la carpeta de archivos temporales en windows
		name = temp_path + 'min.vbs'									# Indica la ruta y nombre del archivo
		if not os.path.isdir(temp_path): os.mkdir(temp_path)			# Crea la carpeta _odin_ en los archivos temporales si no existe
		if not os.path.isfile(name):									# Crea el archivo si no existe en la carpeta %temp%\_odin_
			with open(name,'w') as File:
				File.write(Scripts.min_vbs)								# Añade el código dentro del archivo
				File.close()
		key = run_command('cscript ' + name).split('\n')				# Ejecuta el código del script
	
	# ~ def closeCMD(): WCS.FreeConsole()
	
	def hideConsole(xD=True): WG.ShowWindow(WCS.GetConsoleWindow(), not xD)
	
	# Saber si esta activo el Bloq. Mayus o las teclas Shift de izquierda o derecha.
	def is_shift_pressed():
		return False if WA.GetKeyState(WC.VK_CAPITAL) == 0 else True
	


class PyGameFuncs:
	
	def drawText(screen, text, position, font, color):					# Dibuja texto en pantalla.
		text = font.render(text, 1, color)								# Se pasa el texto con la fuente especificada.
		screen.blit(text, position)										# Se dibuja en pantalla el texto en la posición indicada.
	
	def rect_opaco(screen, surface, color=(0,0,0), alpha=128): 					# Rectangulo Opaco, sirve para crear rectangulos transparentes.
		img = pygame.Surface(surface[2:])
		img.set_alpha(alpha)
		img.fill(color)
		screen.blit(img, surface[:2])



class Particle:
	
	def __init__(self, letter):
		self.letter = letter
		self.color = 255
		self.l_t = 0



class Raindrop:
	
	def __init__(self, katakana, qty_chars):
		
		self.qty_chars = qty_chars
		self.qty_actual = 0
		
		self.rand = random.randint(150,250)/100
		
		self.digital_raindrop = [Particle(random.choice(katakana)) for _ in range(self.qty_chars)]
		
		self.time_init = time.perf_counter()
		self.time_lapsed = 0
		
		self.time_init_wait = time.perf_counter()
		self.time_lapsed_wait = 0
		self.time_wait = random.randint(0, 20)/5
		
		self.is_black = False

	

#=======================================================================



def main():
	
	# ~ Utils.hideConsole(True)
	
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	
	#===================================================================
	#Constants:
	# ~ SCR_SIZE = Utils.screenSize()
	SCR_SIZE = (720, 480)
	FONT_SIZE = 30
	FPS = 60
	#===================================================================
	#Variables:
	close_digital_rain = False											# Control de ventana, si es True el programa termina su ejecución.
	alpha_value = 0														# Cantidad de difuminado.
	mouse_vis = True
	qty_tick = 0
	
	katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
	# ~ katakana = list(string.ascii_letters)+list(string.digits)
	
	rain = [Raindrop(katakana, SCR_SIZE[1]//FONT_SIZE) for _ in range(SCR_SIZE[0]//FONT_SIZE)]
	
	tmp_rain = copy.deepcopy(rain)
	
	#===================================================================
	#Objects:
	pygame.init()
	screen  = pygame.display.set_mode(SCR_SIZE, pygame.NOFRAME)			# Objeto que crea la ventana.
	clock   = pygame.time.Clock()										# Obtiener el tiempo para pasar la cantidad de FPS más adelante.
	surface = pygame.Surface(SCR_SIZE)
	surface.set_alpha(alpha_value)
	katakana_font = pygame.font.Font('ms mincho.ttf', FONT_SIZE)
	#===================================================================
	
	while not close_digital_rain:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:								# Si se presiona el botón cerrar, cerrara el programa.
				close_digital_rain = True
			elif event.type == pygame.KEYDOWN:							# Entra al bloque cuando se presiona cualquier tecla.
				if event.key == pygame.K_ESCAPE:						# Si se presiona Escape, cerrara el programa.
					close_digital_rain = True
				if event.key == pygame.K_RETURN:						# Si se presiona la tecla Enter hace visible/invisible el puntero.
					mouse_vis = not mouse_vis
					pygame.mouse.set_visible(mouse_vis)
		
		screen.blit(surface, (0, 0))									# Dibuja el difuminado.
		screen.fill(pygame.Color('black'))								# Dibuja el fondo negro.
		
		if not pygame.time.get_ticks() % 20 and alpha_value < 200:		# Al empezar, cada 20 ticks disminuye el difuminado.
			alpha_value += 5
			surface.set_alpha(alpha_value)
		
		for j, raindrop in enumerate(tmp_rain):
			
			if raindrop.is_black:
				rain[j] = Raindrop(katakana, SCR_SIZE[1]//FONT_SIZE)
			
			if raindrop.time_wait > raindrop.time_lapsed_wait:
				raindrop.time_lapsed_wait = time.perf_counter() - raindrop.time_init_wait
				continue
			
			raindrop.time_lapsed = time.perf_counter() - raindrop.time_init
			
			if raindrop.time_lapsed > .1 and not raindrop.qty_actual == raindrop.qty_chars:
				raindrop.qty_actual += 1
				raindrop.time_init = time.perf_counter()
			
			# ~ if not raindrop.qty_actual_dism == 100:
			for i in range(raindrop.qty_actual):
				PyGameFuncs.drawText(
					screen,
					raindrop.digital_raindrop[i].letter,
					[j*FONT_SIZE, i*FONT_SIZE],
					katakana_font,
					pygame.Color(
						(0, raindrop.digital_raindrop[i].color, 0) if i == raindrop.qty_chars-1 else (
							'white' if i == raindrop.qty_actual-1 else (0, raindrop.digital_raindrop[i].color, 0)
						)
					)
				)
				if raindrop.digital_raindrop[i].l_t == 0:
					raindrop.digital_raindrop[i].l_t = time.perf_counter()
			
			if raindrop.qty_actual == raindrop.qty_chars:
				
				tmp = 0
				
				for i in range(raindrop.qty_actual):
					
					timer = (time.perf_counter() - raindrop.digital_raindrop[i].l_t)
					
					if timer > raindrop.rand:																# Espera unos segundos antes de desvanecerse
						raindrop.digital_raindrop[i].color = int(
							255 * ( 1 - ( (timer - raindrop.rand) / .5 ) )
						)
					
					if raindrop.digital_raindrop[i].color <= 0:
						raindrop.digital_raindrop[i].color = 0
						tmp += 1
				
				if raindrop.qty_chars == tmp and not raindrop.is_black:
					raindrop.is_black = True
		
		tmp_rain = copy.copy(rain)
		
		pygame.display.flip()											# Actualiza los datos en la interfaz.
		clock.tick(FPS)



if __name__ == '__main__':
	
	# ~ print(pygame.Color('green'))
	main()






