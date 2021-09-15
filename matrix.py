
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
import string
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
	
	def drawText(surface, text, position, font, color, alpha=None):		# Dibuja texto en pantalla.
		text = font.render(text, True, color)							# Se pasa el texto con la fuente especificada.
		if alpha: text.set_alpha(alpha)
		surface.blit(text, position)									# Se dibuja en pantalla el texto en la posición indicada.
	
	# ~ def rect_opaco(screen, surface, color=(0,0,0), alpha=128): 			# Rectangulo Opaco, sirve para crear rectangulos transparentes.
		# ~ img = pygame.Surface(surface[2:])
		# ~ img.set_alpha(alpha)
		# ~ img.fill(color)
		# ~ screen.blit(img, surface[:2])



class Particle:
	
	def __init__(self, letter):
		self.letter = letter
		self.color = 255
		self.l_t = 0



class Raindrop:
	
	def __init__(self, katakana, qty_chars):
		
		self.qty_chars = qty_chars+1									# Cantidad total de caracteres.
		self.qty_actual = 0												# Cantidad actual de caracteres que serán mostrados
		
		self.digital_raindrop = [Particle(random.choice(katakana)) for _ in range(self.qty_chars)]	# Caracteres con caracteristicas.
		
		self.time_init = time.perf_counter()							# Inicia a contar el tiempo para saber cuanto ha pasado hasta el aumento de velocidad.
		self.time_lapsed = 0											# Determina cuanto tiempo ha pasado, para saber si se deberá mostrar el siguiente caracter. Esto es relacionado con la velocidad.
		self.vel = random.randint(3,18)/100								# Velocidad de desplazamiento. Entre .05 y .15 segundos por caracter
		
		self.time_init_wait = time.perf_counter()						# Inicia a contar el tiempo para saber cuanto ha pasado desde la creacion de la gota.
		self.time_lapsed_wait = 0										# Indicará el tiempo recorrido para saber cuando empieza a caer la gota.
		self.time_wait = random.randint(1, 30)/2						# Indica el tiempo que esperara la gota en caer. Entre .5 y 10 segundos, de .5 en .5 
		
		self.is_black = False											# Indica si la linea ya esta completamente desvanecida
		self.is_blocked = False											# Indica si ya se reinicio la gota.
		
		self.time_init_des = 0											# Tiempo inicial para desvanecer
		self.time_des = random.randint(5,15)/10							# Tiempo para empezar a desvanecerse. Entre .5 y 1.5 segundos.
		self.vel_des = random.randint(3,12)/10							# Velocidad al desvanecerse. Entre .3 y 1.2 segundos.
		


#=======================================================================



def main():
	
	# ~ Utils.hideConsole(True)
	
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	
	#===================================================================
	#Constants:
	SCR_SIZE = Utils.screenSize()
	# ~ SCR_SIZE = (720, 480)
	FONT_SIZE = 24
	FPS = 60
	#===================================================================
	#Variables:
	close_digital_rain = False											# Control de ventana, si es True el programa termina su ejecución.
	alpha_value = 0														# Cantidad de difuminado.
	mouse_vis = True
	qty_tick = 0
	full_scr = False
	
	katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
	all_str = list(string.digits)#+list(string.ascii_letters)
	
	rain = [Raindrop(katakana+all_str, SCR_SIZE[1]//FONT_SIZE) for _ in range(SCR_SIZE[0]//FONT_SIZE)]
	
	tmp_rain = copy.copy(rain)
	
	#===================================================================
	#Objects:
	pygame.init()
	# ~ screen  = pygame.display.set_mode(SCR_SIZE, pygame.NOFRAME)			# Objeto que crea la ventana.
	screen  = pygame.display.set_mode(SCR_SIZE, pygame.FULLSCREEN)#, vsync=1)			# Objeto que crea la ventana.
	surface = pygame.Surface(SCR_SIZE)
	surface.set_alpha(alpha_value)
	clock   = pygame.time.Clock()										# Obtiener el tiempo para pasar la cantidad de FPS más adelante.
	katakana_font = pygame.font.Font('ms mincho.ttf', FONT_SIZE)
	katakana_font.set_bold(False)
	#===================================================================
	
	while not close_digital_rain:
		
		screen.blit(surface, (0, 0))									# Dibuja el difuminado.
		surface.fill(pygame.Color('black'))								# Dibuja el fondo negro.
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:								# Si se presiona el botón cerrar, cerrara el programa.
				close_digital_rain = True
			elif event.type == pygame.KEYDOWN:							# Entra al bloque cuando se presiona cualquier tecla.
				if event.key == pygame.K_ESCAPE:						# Si se presiona Escape, cerrara el programa.
					close_digital_rain = True
				if event.key == pygame.K_RETURN:						# Si se presiona la tecla Enter hace visible/invisible el puntero.
					mouse_vis = not mouse_vis
					pygame.mouse.set_visible(mouse_vis)
				# ~ if event.key == pygame.K_f:								# Si se presiona la tecla Enter hace visible/invisible el puntero.
					# ~ if not full_scr:
						# ~ screen = pygame.display.set_mode(Utils.screenSize(), pygame.FULLSCREEN)
					# ~ else:
						# ~ screen = pygame.display.set_mode(SCR_SIZE, pygame.NOFRAME)
					# ~ full_scr = not full_scr
					# ~ pygame.display.update()
		
		for j, raindrop in enumerate(tmp_rain):
			
			if raindrop.is_blocked: continue
			
			if raindrop.is_black:
				rain[j] = Raindrop(katakana+all_str, SCR_SIZE[1]//FONT_SIZE)
				raindrop.is_blocked = True
			
			if raindrop.time_wait > raindrop.time_lapsed_wait:
				raindrop.time_lapsed_wait = time.perf_counter() - raindrop.time_init_wait
				continue
			
			raindrop.time_lapsed = time.perf_counter() - raindrop.time_init
			
			if raindrop.time_lapsed > raindrop.vel and not raindrop.qty_actual == raindrop.qty_chars:
				raindrop.qty_actual += 1
				raindrop.time_init = time.perf_counter()
			
			for i in range(raindrop.qty_actual):
				
				if random.random() > .995:
					raindrop.digital_raindrop[i].letter = random.choice(katakana)
				
				plus = FONT_SIZE/4 if raindrop.digital_raindrop[i].letter in all_str else 0
				PyGameFuncs.drawText(
					surface,
					raindrop.digital_raindrop[i].letter,
					[j*FONT_SIZE+plus, i*FONT_SIZE],
					katakana_font,
					pygame.Color(
						(0, raindrop.digital_raindrop[i].color, 0) if i == raindrop.qty_chars-1 else (
							'white' if i == raindrop.qty_actual-1 else (0, raindrop.digital_raindrop[i].color, 0)
						)
					)
				)
				if raindrop.digital_raindrop[i].l_t == 0:
					raindrop.digital_raindrop[i].l_t = time.perf_counter()
			
			tmp = 0
			
			for i in range(raindrop.qty_actual):
				
				timer = (time.perf_counter() - raindrop.digital_raindrop[i].l_t)
				
				if raindrop.time_init_des == 0:
					raindrop.time_init_des = timer
				
				if timer > raindrop.time_des+raindrop.time_init_des:																# Espera unos segundos antes de desvanecerse
					raindrop.digital_raindrop[i].color = int(
						255 * ( 1 - ( (timer - (raindrop.time_des+raindrop.time_init_des)) / raindrop.vel_des ) )
					)
				
				if raindrop.digital_raindrop[i].color <= 0:
					raindrop.digital_raindrop[i].color = 0
					tmp += 1
			
			if raindrop.qty_chars == tmp and not raindrop.is_black:
				raindrop.is_black = True
		
		qty_tick += 1
		
		if qty_tick == 30:
			tmp_rain = copy.copy(rain)
			qty_tick = 0
		
		if not pygame.time.get_ticks() % 20 and alpha_value < 170:		# Al empezar, cada 20 ticks disminuye el difuminado.
			alpha_value += 5
			surface.set_alpha(alpha_value)
		
		pygame.display.flip()											# Actualiza los datos en la interfaz.
		clock.tick(FPS)



if __name__ == '__main__':
	
	# ~ print(pygame.Color('green'))
	main()






