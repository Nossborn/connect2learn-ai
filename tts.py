#	
#	This file handles the text to speech part of the program, as well as
#	the interaction with the raspberry pi button. run_tts() is what gets
#	called first from server.py with the param message, which is what it
#	is going to try to say. Right now it only checks whether or not it is
#	is running on a Rpi or not, however if we want to support other linux
#	versions, we really should check properly and set PYTH_EXE_NAME
#	seperatly.
#	

import time
from subprocess import Popen, PIPE

try:
	import RPi.GPIO as gpio
	isRpi = True 	#Code is running on raspberry pi
	PYTH_EXE_NAME = "python3"
except ImportError:
	isRpi = False 	#Code is running on windows
	PYTH_EXE_NAME = "python.exe"

engine = None
led = 25
button = 23
speak_proc = None


def initGPIO():
	gpio.setmode(gpio.BCM)
	gpio.setup(button, gpio.IN)
	gpio.setup(led, gpio.OUT)

def run_tts(message='Error'):
	response = None
	if(isRpi):
		initGPIO()
		gpio.output(led, 1)
		response = button_handler(message)
		gpio.output(led, 0)
		gpio.cleanup()
	else:
		speak(message)
		response = "True"

	if(response==None):
		response = "False"
	return response

def button_handler(message):
	print("Waiting for button push....")
	startTime = time.time()
	while True:
		if(gpio.input(button)==0): # If button pressed, exit loop
			print("Button pressed!")
			speak(message)
			return "True"
		elif(time.time() - startTime > 10): #Allow up to 10s to push button before exit loop
			response = "Took too long, no button press detected!"
			print(response)
			return "False"
		time.sleep(0.25)

def speak(message):
	print("Speaking...")
	global speak_proc
	speak_proc = Popen([PYTH_EXE_NAME, "speak.py", message]) #open subprocess with message to be said as arg
	#Could we maybe check here if on linux and if true then run open([espeak, message]) ?

def stop_speak():
	global speak_proc
	if(speak_proc is None):
		print("Request aborted, not speaking")
		return False
	print("Stopping speech...")
	speak_proc.terminate()
	speak_proc = None #Cleaning up varibles
	return True