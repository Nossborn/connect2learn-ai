#	
#	This is script is ran as a subprocess from tts.py. It recieves the
#	message to be read as input (sys.argv[1]).
#
#	This script is terrible, mostly because the pyttsx3 library we are
#	using is quite broken. What should happen is that when it runs the
#	say() method, is that in runAndWait(), it should open a new thread and
#	read the string until completion and then close the thread and continue
#	with the program. This is not what happens always though on the
#	raspberry pi. On linux, it closes the thread prematurely, causing the
#	string to be cut off. One way to check if the engine is actually done
#	or not is to use the isBusy() method, but that for whatever reason
#	doesn't work for shorter strings. So here we are with a lot of akward
#	timers and spaghetti code.
#	Your mission, should you choose to accept it, would be to fix this
#	mess. Best of luck dear traveler.
#
#	Maybe this file could be sidestepped if you're on Linux by calling
#	$ espeak [message] directly in tts.py?
#

import sys
import pyttsx3
import time

def init_engine():
	engine = pyttsx3.init()
	return engine

def say(s):
	start_time = time.time()
	engine.say(s)
	engine.runAndWait()
	elapsed_time = time.time() - start_time
	if(elapsed_time > 1.5):
		return
	while engine.isBusy():
		elapsed_time = time.time() - start_time
		if(elapsed_time > 15):
			break 
		time.sleep(0.5)

engine = init_engine()
say(str(sys.argv[1]))