#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'me' #David-Salinas Cortés'
#Code in progress. Here only for checking. Use at your own risk (those indents)!

import socket
import tkinter
from tkinter import *
import time
import os
import sys, traceback

import urllib.request
import json

import threading
import random
import multiprocessing
from multiprocessing import Queue
import queue

import math
from datetime import datetime
import codecs
import re

import sqlite3

import tkinter.messagebox
import pyautogui

localtime = time.asctime( time.localtime(time.time()) )

TEST_CHARSET = u" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¡¢£¤¥¦§¨©ª«¬­ ®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĂăĄąĆćČčĎďĐđĘęĚěĹĺĽľŁłŃńŇňŐőŒœŔŕŘřŚśŞşŠšŢţŤťŮůŰűŸŹźŻżŽžƒˆˇ˘˙˛˜˝–—‘’‚“”„†‡•…‰‹›€™"

WEBPAGE_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
FBSITE_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com(\/.*)?$")
FBGROUP_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com\/groups\/[0-9]+\/permalink(\/.*)?$")
FBPAGE_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com\/(pg\/)?[a-zA-Z0-9\.]+(\/.*)?$")
FBPAGEPHOTOS_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com\/(pg\/)?[a-zA-Z0-9\.]+\/photos(\/.*)?$")
FBPAGEALBUMS_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com\/(pg\/)?[a-zA-Z0-9\.]+\/photos\/\?tab=albums(.*)?$")
FBPAGEALBUM_REGEX = re.compile(r"^[a-zA-Z0-9\-\.\/\\:].facebook\.com\/(pg\/)?[a-zA-Z0-9\.]+\/photos\/\?tab=album&album_id[=0-9]+?$")

FBSITE = 6
FBPAGE_PHOTOS = 5
FBPAGE_ALBUMS = 4
FBPAGE = 3
FBPAGE_ALBUM = 2
FB_GROUP = 1
WEBPAGE = -1
SOMETHING_ELSE = -2

EMPTY = "<Empty>"

#......config................................................................


CHECKNAMES = "CHECKNAMES"
CHECKNAMES_TIMEOUT = 1200
CHECKNAMES_MAXCOUNT = 100

NOTIFICATIONS = "NOTIFICA"
NOTIFICATIONS_TIMEOUT = 1800
NOTIFICATIONS_MAXCOUNT = 200

SPECIFIC_POST = "SPECPOST" 
SPECIFIC_POST_TIMEOUT = 3600
SPECIFIC_POST_MAXCOUNT = 70

SPECIFIC_ALBUM = "SPECALBM"
SPECIFIC_ALBUM_TIMEOUT = 3600
SPECIFIC_ALBUM_MAXCOUNT = 70

SPECIFIC_RAISER = "SPECRAIS"
SPECIFIC_RAISER_TIMEOUT = 3600
SPECIFIC_RAISER_MAXCOUNT = 144

ACTIVITYREG = "ACTIVITYREG"
ACTIVITYREG_TIMEOUT = 1200
ACTIVITYREG_MAXCOUNT = 100

RAISEPOST = "RAISEPOST"
RAISEPOST_TIMEOUT = 1200
RAISEPOST_MAXCOUNT = 100

TURNO_INDEFINIDO = -1
TURNO_CHECKNAMES = 1
TURNO_NOTIFICACIONES = 2
TURNO_POSTS = 3
TURNO_ALBUMS = 4
TURNO_REGISTRO_DE_ACTIVIDAD = 5
TURNO_SUBE_PUBLICACION = 6

MODO_INDEFINIDO = -1
MODO_MANUAL = 1
MODO_AUTOMATICO = 2

TURNO = TURNO_INDEFINIDO
MODO = MODO_INDEFINIDO


LIMIT_FOR_USERNAME_SHORTEST_LENGHT = 8
LIMIT_FOR_PASSWORD_LONGEST_LENGHT = 16


USER_HERE = "<Escriba aquí su Cuenta de Usuario>"
PASS_HERE = "<Escriba aquí su Contraseña>"

WUNDERGROUND_KEY='c4c7b1adc7c9b8c1'

gbLoggedIn = False

SYMBOLS = ['!', '"', '·', '$', '%', '&', '/', 
			'(', ')', '=', '?', '¿', 'º', 'ª', 
			'\\', '|', '@', '#', '~', '½', '¬', 
			'{', '[', ']', '}', '^', '*', '"', 
			'Ç', '`', '+', '\'', 'ç', ',', '.', 
			'-', ';', ':', '_', '·', '<', '>', 
			' ']

NOTIFICATIONS_PARAMS = {'FB_CONNECTION' : "notifications", 
	'FB_USERNAME' : "", 
	'FB_SERVER' : "www.facebook.com", 
	'FB_BEHAVIOR' : NOTIFICATIONS, 
	'DB_FILE' : "../../fbclient.db", 
	'FB_PORT' : 21, 
	'USR_NICKNAME' : "", 
	'USR_USERNAME': "", 
	'USR_ENCRYPTED_PASSWORD' : "",
	'PASSWORD_SALT':  ""} 
	

SPECIFIC_POST_PARAMS = {'FB_CONNECTION' : "posts", 
	'FB_USERNAME' : "", 
	'FB_SERVER' : "www.facebook.com", 
	'FB_BEHAVIOR' : SPECIFIC_POST, 
	'DB_FILE' : "../../fbclient.db", 
	'FB_PORT' : 21, 
	'USR_NICKNAME' : "", 
	'USR_USERNAME': "", 
	'USR_ENCRYPTED_PASSWORD' : "",
	'PASSWORD_SALT': ""}

SPECIFIC_ALBUM_PARAMS = {'FB_CONNECTION' : "albums", 
	'FB_USERNAME' : "", 
	'FB_SERVER' : "www.facebook.com", 
	'FB_BEHAVIOR' : SPECIFIC_ALBUM, 
	'DB_FILE' : "../../fbclient.db", 
	'FB_PORT' : 21, 
	'USR_NICKNAME' : "", 
	'USR_USERNAME': "", 
	'USR_ENCRYPTED_PASSWORD' : "",
	'PASSWORD_SALT': ""}

SPECIFIC_RAISER_PARAMS = {'FB_CONNECTION' : "raiser", 
	'FB_USERNAME' : "", 
	'FB_SERVER' : "www.facebook.com", 
	'FB_BEHAVIOR' : SPECIFIC_RAISER, 
	'DB_FILE' : "../../fbclient.db", 
	'FB_PORT' : 21, 
	'USR_NICKNAME' : "", 
	'USR_USERNAME': "", 
	'USR_ENCRYPTED_PASSWORD' : "",
	'PASSWORD_SALT': ""}


gbPARAMS = [NOTIFICATIONS_PARAMS, SPECIFIC_POST_PARAMS, SPECIFIC_ALBUM_PARAMS, SPECIFIC_RAISER_PARAMS]

goUI=None

gaNotifications = []
gaPosts = []
gaAlbums = []

STATUS_EXPIRED = -2
STATUS_CANCELED = -1
STATUS_POSTING = 0
STATUS_PARTIALLY_POSTED = 1
STATUS_POSTED = 2
STATUS_VALID = 3
STATUS_COMPLETED = 4
STATUS_DELIVERED = 5
STATUS_HANDED = 6
STATUS_FINISHED = 7

USER_STATUS_EXPIRED = -2
USER_STATUS_CANCELED = -1
USER_STATUS_CLIENT_OCATIONALLY = 0
USER_STATUS_CLIENT_PARTIALLY = 1
USER_STATUS_CLIENT_COMPLETELY = 2
USER_STATUS_VALID = 3
USER_STATUS_CLIENT_FRECUENTLY = 4
USER_STATUS_FINISHED = 7


TEXT_HERE = "<TEXTHERE>"



ntfWindow = None
spstWindow = None
albmWindow = None
raiserWindow = None



def randomSleep(piMaxSecondsToWait):
	lfFraction = random.random()
	liMaxSeconds = random.randint(2, piMaxSecondsToWait)
	fbClntprnt("Sleeping " + str(liMaxSeconds*lfFraction) + " seconds")
	time.sleep(liMaxSeconds*lfFraction)
	
def fbClntprnt(psTexto, psUtf8=""):
	print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " " + psTexto, psUtf8)	




#................................................................

"""
Method: ClosingFBClient
description: Its objective is to close an FBClient Window 

Parameter: theFBClientToClose
description: An FBClient instance (an instance object of the class FBClient (which is supposed to be running at the time when you call this method).
"""
def ClosingFBClient(theFBClientToClose=None):
	global ntfWindow
	global spstWindow
	global albmWindow
	global raiserWindow
	global client
	global gbLoggedIn
	
	if gbLoggedIn:
		LogOut()
	
	if theFBClientToClose == None :
		fbClntprnt(" To Close something you need to know WHAT to close.")
		return False
	else:
		ldicParams = theFBClientToClose.dicParams
		
	fbClntprnt("Closing: " + ldicParams['FB_CONNECTION'] + " !!!")

	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s thread1.stop()")
#	theFBClientToClose.thread1.stop()

	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s thread2.stop()")
#	theFBClientToClose.thread2.stop()

	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s thread3.stop()")
#	theFBClientToClose.thread3.stop()

	#Close here the DB Conection
	theFBClientToClose.ClosingDBConnection()

	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s master.destroy()")
	if ldicParams['FB_CONNECTION'] == "notifications":
		ntfWindow.destroy()
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "post":
		spstWindow.destroy()
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "album":
		albmWindow.destroy()
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "raiser":
		raiserWindow.destroy()
		theFBClientToClose.fbClntprntDbg("success!")
	

	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s master is being set to None")
	if ldicParams['FB_CONNECTION'] == "notifications":
		ntfWindow = None
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "post":
		spstWindow = None
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "album":
		albmWindow = None
		theFBClientToClose.fbClntprntDbg("success!")
	elif ldicParams['FB_CONNECTION'] == "raiser":
		raiserWindow = None
		theFBClientToClose.fbClntprntDbg("success!")


	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + "\'s .destroy()")
	for liInt in range(0,len(sys.argv)):
		if not client[liInt] == None:
			if client[liInt].dicParams['FB_CONNECTION'] == ldicParams['FB_CONNECTION']:
				client[liInt].destroy()
				theFBClientToClose.fbClntprntDbg("success!")
	
	theFBClientToClose.fbClntprntDbg(ldicParams['FB_CONNECTION'] + " is being set to None")
	for liInt in range(0,len(sys.argv)):
		if not client[liInt] == None:
			if client[liInt].dicParams['FB_CONNECTION'] == ldicParams['FB_CONNECTION']:
				client[liInt] = None
				theFBClientToClose.fbClntprntDbg("success!")
				
	theFBClientToClose = None


def LogOut():
	x=""


#......................................................................



def CheckNames(maxCount, psTurno=TURNO_CHECKNAMES, piModo=MODO_AUTOMATICO):
	global goUI
	global MODO
	global TURNO
	lsFile = ""

	if MODO == MODO_AUTOMATICO and TURNO == TURNO_CHECKNAMES:
		goUI.master.title("Check Names")
		goUI.EmptyTextBoxAndClipboard()
		lsFile = "\"http://www.facebook.com/group/" +  + "\" "
		if sys.platform == 'linux2':
			subprocess.call(["xdg-open", file])
		else:
			os.startfile(file)			
	else:
		return False		
	


		

def ActivityRegChecker(maxCount, psTurno=TURNO_REGISTRO_DE_ACTIVIDAD, piModo=MODO_AUTOMATICO):
	goUI.master.title("Activities Registry")
	goUI.EmptyTextBoxAndClipboard()


def CheckNotifications(maxCount, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO):
	global goUI
	#goUI.grid()
	print("Iniciando CheckNotificaciones")
	
	#if goUI.Turno != psTurno and goUI.Count <= 0:
	#	goUI.Turno = psTurno
	#	goUI.Modo = piModo
	#	goUI.Count = maxCount
	#	fbClntprnt("Corre el primero en la fila.")
	#elif goUI.Turno == psTurno and goUI.Count <= 0:
	#	goUI.Turno = psTurno
	#	goUI.Modo = piModo
	#	goUI.Count = maxCount
	#	fbClntprnt("Corre el primero en cola (Notificaciones).")
	#elif goUI.Turno == psTurno and goUI.Count > 0:
	#	fbClntprnt("Seguro ya está corriendo y aún no termina...")
	#	return False
	#else:
	#	fbClntprnt("No Corre Notificaciones por ahora ")
	#	return False
	
	goUI.Turno = psTurno
	goUI.Modo = piModo
	goUI.Count = maxCount

	#goUI.master.title("Notificaciones")
	print("Notificaciones")
	goUI.EmptyTextBoxAndClipboard()

	print("First \'Are We OK?\':")
	if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

	if not goUI.WeAreThere():
		fbClntprnt("We are not there! :0")
		goUI.GoThere()
	
	if goUI.WeAreThere(): # and goUI.Turno==TURNO_INDEFINIDO and goUI.Modo==MODO_INDEFINIDO:

		if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

		liRandomSleep = random.randint(1,7)

		fbClntprnt("We are going to AddressBar...")
		goUI.Go2AddressBar()
		time.sleep(liRandomSleep/10)

		if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

		fbClntprnt("We are going to FB SearchBox...")
		goUI.GoForward(2)
		goUI.PressEsc()

		if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

		fbClntprnt("We are going to Notif Icon Button...")
		goUI.GoForward(6)
		time.sleep(liRandomSleep/10)
		goUI.PressEnter()

		if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

		fbClntprnt("We are there, now: Notif Dropdown\'s items...")
		goUI.GoForward(4)
		time.sleep(liRandomSleep/10)
		goUIgoUI.RightClick()			
		
		for liCount in range(0, maxCount - 1):

			if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False


			liRandomSleep = random.randint(0,10)

			fbClntprnt("Inside the cicle.- Selecting Drop-menú option...")
			goUI.UpKey(2) #To get the Menú option called "Copy link location"

			fbClntprnt(""" Now wait to see if someone is watching to see if the drop-down menú is ok. """)
			time.sleep((liRandomSleep*4)/10)
		
			if goUI.WeAreThere and goUI.GB_PLAY and not goUI.GB_PAUSE and not goUI.GB_STOP:

				if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False
		
				fbClntprnt("Inside the cicle.- Pressing \<Enter\> there...")
				goUI.PressEnter()
		
				lsTheURL = goUI.GetClipBoardText()

				fbClntprnt("Notif URL.- " + lsTheURL)
				
				goUI.Count = maxCount - liCount

				if not goUI.AreWeOk(TURNO_NOTIFICACIONES, "Notificaciones"): return False

				fbClntprnt("Inside the cicle.- Next Notif...")
				goUI.GoForward(3)
				time.sleep(liRandomSleep/10)
				fbClntprnt("Inside the cicle.- Drop Menú...")
				goUI.RightClick()
	goUI.Stop()
	goUI.Count = 0
	goUI.Turno = TURNO_INDEFINIDO
	goUI.Modo = MODO_INDEFINIDO
	#goUI.grid_remove()
	return False
	
"""
	Post Raiser Class
"""
class PostRaiser(Frame):

	def fbClntprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	def ClosingDBConnection(self):
		global client
	
		#fbClntprnt(self.dicParams['FB_CONNECTION'] + "\'s saying good bye to the DB !")

		#fbClntprnt("Commiting  " + self.dicParams['FB_CONNECTION'] + "\'s DB Changes !!!")
		#self.Cnx.commit()

		#fbClntprnt("Closing  " + self.dicParams['FB_CONNECTION'] + "\'s DB Conection !!!")
		#self.Cnx.close()

		#fbClntprnt("Setting  " + self.dicParams['FB_CONNECTION'] + "\'s DB Conection to NONE !!!")
		#self.Cnx = None


	def __init__(self, master=None, pdicParams=None, psTitle="Post Raiser", *args, **kwargs):
		global gbLoggedIn
		global goUI
		#goUI.grid()
		print("Iniciando PostRaiser")

		self.dicParams = pdicParams

		fbClntprnt('Loading first Frame:')
		Frame.__init__(self, master)
		self.grid()


		if psTitle==SPECIFIC_RAISER:
			lsTitle = "@Post Raiser"

		self.master.title(lsTitle)

		
		rand = random.Random()

		self.running = 1
	
		fbClntprnt("Periodic Call about to start")
		self.periodicCall()
		fbClntprnt("Periodic Call STARTED!!!")


		ntfWindow = tkinter.Toplevel()

		if psTitle==SPECIFIC_RAISER:
			goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_SUBE_PUBLICACION, piModo=MODO_MANUAL, piCount=ACTIVITYREG_MAXCOUNT, psTitle=lsTitle)


		self.gaTextArray = [None]*11 

		# Set up the GUI
		fbClntprnt('Adding TextToScrable InputBox:')

		#InnerFrame = Frame(self, width=768, height=576, bg="", colormap="new")

								#tkinter.Entry(self, bg="white", fg="black", cursor="xterm", 
								#state=tkinter.NORMAL) # .master height=1, width=14,  undo=False, 
		self.playTextToScrabble = tkinter.Text(self, bg="white", fg="black", cursor="xterm", height=2,  
								undo=True, maxundo=-1, state=tkinter.NORMAL, width=47, wrap=tkinter.WORD)
		self.playTextToScrabble.bind("<Key>", self.textToScrableChanged)
		#self.playTextToScrabble.bind("<Return>", self.callUsernameChecker)#lambda e: "break")
		self.playTextToScrabble.grid()

		self.ScrabledText = [None]*10

		fbClntprnt('Adding ScrabledText1 Label:')
		self.ScrabledText[0] = Label(self, height=2, width=47, text="1")
		self.ScrabledText[0].grid()

		fbClntprnt('Adding ScrabledText2 Label:')
		self.ScrabledText[1] = Label(self, height=2, width=47, text="2")
		self.ScrabledText[1].grid()

		fbClntprnt('Adding ScrabledText3 Label:')
		self.ScrabledText[2] = Label(self, height=2, width=47, text="3")
		self.ScrabledText[2].grid()

		fbClntprnt('Adding ScrabledText4 Label:')
		self.ScrabledText[3] = Label(self, height=2, width=47, text="4")
		self.ScrabledText[3].grid()

		fbClntprnt('Adding ScrabledText5 Label:')
		self.ScrabledText[4] = Label(self, height=2, width=47, text="5")
		self.ScrabledText[4].grid()

		fbClntprnt('Adding ScrabledText6 Label:')
		self.ScrabledText[5] = Label(self, height=2, width=47, text="6")
		self.ScrabledText[5].grid()

		fbClntprnt('Adding ScrabledText7 Label:')
		self.ScrabledText[6] = Label(self, height=2, width=47, text="7")
		self.ScrabledText[6].grid()

		fbClntprnt('Adding ScrabledText8 Label:')
		self.ScrabledText[7] = Label(self, height=2, width=47, text="8")
		self.ScrabledText[7].grid()

		fbClntprnt('Adding ScrabledText9 Label:')
		self.ScrabledText[8] = Label(self, height=2, width=47, text="9")
		self.ScrabledText[8].grid()

		fbClntprnt('Adding ScrabledText10 Label:')
		self.ScrabledText[9] = Label(self, height=2, width=47, text="10")
		self.ScrabledText[9].grid()

		fbClntprnt('Adding PasteAndScrabbleText InputButton:')
		self.pasteAndScrabbleText = tkinter.Button(self, text='Paste Current Text', fg="green", command=self.PasteTextAndScrabble) #.master
		self.pasteAndScrabbleText.grid()

		fbClntprnt('Adding Close Button:')
		self.console = tkinter.Button(self, text='Close', command=self.endApplication) #.master
		self.console.grid() # console.pack()
		# Add more GUI stuff here

		#playButton.pack(side=TOP)
		#stopButton.pack(side=BOTTOM)

		self.master.protocol("WM_DELETE_WINDOW", self.quitCnx)

	"""
		method: textToScrableChanged
		description:
	"""
	def textToScrableChanged(self, event):
		global goUI
		global gbLoggedIn
		self.gaTextArray[0] = self.playTextToScrabble.get( 1.0, tkinter.END )
		fbClntprnt('texto: ' + self.gaTextArray[0])
		self.Scrabble()

	def Scrabble(self):
		NUMBER_OF_LABELS = 10
		lbFound = False
		lsArr = [None]*NUMBER_OF_LABELS
		laText = self.gaTextArray[0].split(" ")
		fbClntprnt('Scrabble: ' + self.gaTextArray[0])
		liNumbreOfWords = len(self.gaTextArray[0].split(" "))
		
		liQuantity = int((NUMBER_OF_LABELS*10)/(liNumbreOfWords*10))
		
		for liCount in range(0, NUMBER_OF_LABELS - 1):
			lsArr[liCount] = ""
			lbFound = False
			for ljCount in range(0, len(self.gaTextArray[0].split(" "))):
				if ljCount == liCount:
					lsArr[liCount] = lsArr[liCount] + " " + self.ScrabbleWordRandomly(laText[ljCount], piQuantity=liQuantity+1)
					fbClntprnt('word: ' + self.ScrabbleWordRandomly(laText[ljCount], piQuantity=1))
					lbFound = True
				elif ljCount > liCount and not lbFound:
					lsArr[liCount] = lsArr[liCount] + " " + self.ScrabbleWordRandomly(laText[ljCount], piQuantity=liQuantity+2)
					fbClntprnt('word: ' + self.ScrabbleWordRandomly(laText[ljCount], piQuantity=2))
					lbFound = True
				else:
					lsArr[liCount] = lsArr[liCount] + " " + laText[ljCount]
					fbClntprnt('word: ' + laText[ljCount])
				
			fbClntprnt('label: ' + lsArr[liCount])
			self.ScrabledText[liCount].config(text=lsArr[liCount])
					
	
	def ScrabbleWordRandomly(self, psWord, piQuantity):
		lbFoundRightNow = False
		liFound = 0
		lsWord = ""
		EQUIVALENCIAS = [["A","4"], ["a","4"], ["b","6"], ["E","3"], 
						["i","1"], ["I","1"], ["l","1"], ["o","0"], ["q","9"], 
						["O","0"], ["T","7"], ["t","7"], ["B","8"], ["S","5"], ["9","q"], ["c","k"], ["Z","2"], ["z","2"]]
		fbClntprnt('ScrabbleWord: ' + psWord + ", " + str(piQuantity))
		for letter in psWord:
			fbClntprnt('letter: ' + letter)
			lbFoundRightNow = False
			for liCount in range(0, len(EQUIVALENCIAS)):
				if letter == EQUIVALENCIAS[liCount][0] and liFound < piQuantity:
					lsWord = lsWord + EQUIVALENCIAS[liCount][1]
					liFound = liFound + 1
					lbFoundRightNow = True
					fbClntprnt('liCount, equiv: ' + str(liCount) + ", " + EQUIVALENCIAS[liCount][1])
					break
			if not lbFoundRightNow:
				lsWord = lsWord + letter
				fbClntprnt('liCount, equiv: ' + str(liCount) + ", " + letter)
		return lsWord
					
				


	"""
		method: PasteTextAndScrabble
		description:
	"""
	def PasteTextAndScrabble(self):
		global goUI
		global gbLoggedIn
		fbClntprnt('yendo allá')
		goUI.GoThere()
		fbClntprnt('Escribiendo:')
		goUI.Type(self.playTextToScrabble.get( 1.0, tkinter.END ))
		self.playTextToScrabble.text = self.ScrabledText[0].text
		for liCount in range(0,9):
			self.ScrabledText[liCount].config(text=self.ScrabledText[liCount + 1].text)
			

	"""
		method: quitCnx
		description: 
	"""
	def quitCnx(self):
		self.running = False
		self.periodicCall()


	"""
		method: endApplication
		description: 
	"""
	def endApplication(self):
		self.running = False


	"""
		method: periodicCall
		description: 	"""
	def periodicCall(self):
		"""
		Check every 100 ms if the program has to be still running.
		"""
		if not self.running:
			# This is the brutal stop of the system. You may want to do
			# some cleanup before actually shutting it down.
			
			ClosingFBClient(theFBClientToClose=self)
			
		self.master.after(100, self.periodicCall)

"""
	User Interaction Class
"""
class UserInteraction(Frame):

	def usrIntrfcprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	
	
	def Play(self):
		self.GB_PLAY = True
		self.GB_PAUSE = False
		self.GB_STOP = False
		self.lbl1.text = "Playing"
		self.PlayBtn.config(fg='gray') # grid_Remove()
		self.PauseBtn.config(fg='black') # grid()
		self.StopBtn.config(fg='black') # grid()

	def Pause(self):
		self.GB_PLAY = False
		self.GB_PAUSE = True
		self.GB_STOP = False
		self.lbl1.text = "Paused"
		self.PlayBtn.config(fg='black') # grid()
		self.PauseBtn.config(fg='gray') # grid_Remove()
		self.StopBtn.config(fg='black') # grid()

	def Stop(self):
		self.GB_PLAY = False
		self.GB_PAUSE = False
		self.GB_STOP = True
		self.lbl1.text = "Stopped"
		self.PlayBtn.config(fg='black') # grid()
		self.PauseBtn.config(fg='gray') # grid_Remove()
		self.StopBtn.config(fg='gray') # grid_Remove()

	def AreWeOk(self, EspectedTurn=None, EspectedTitle=None):

		while not self.GB_PLAY: 
			time.sleep(2)
			fbClntprnt(""" . """)

		if goUI.Turno!=None and goUI.Modo !=None:
			if goUI.Modo == MODO_INDEFINIDO or (goUI.Modo != MODO_AUTOMATICO and goUI.Modo != MODO_MANUAL):
				self.Stop()
				self.Count = 0
				self.Turno = TURNO_INDEFINIDO
				self.Modo = MODO_INDEFINIDO
				self.grid_remove()
				return False
			if goUI.Turno!=EspectedTurn:
			#	goUI.grid_remove()
				self.Stop()
				self.Count = 0
				self.Turno = TURNO_INDEFINIDO
				self.Modo = MODO_INDEFINIDO
				self.grid_remove()
				return False
			elif goUI.Turno==EspectedTurn:
				goUI.master.title(EspectedTitle)
			#	goUI.grid()
				fbClntprnt("We are OK! =D")
				return True
			#elif goUI.Turno==TURNO_INDEFINIDO:
			#	goUI.Turno = EspectedTurn
			#	goUI.Modo = EspectedMode
			#	goUI.master.title(EspectedTitle)
			##	goUI.grid()
			#	fbClntprnt("We are Ok Now! <:D")
			#	return True
		self.Stop()
		self.Count = 0
		self.Turno = TURNO_INDEFINIDO
		self.Modo = MODO_INDEFINIDO
		self.grid_remove()
		return False	

	def __init__(self, master=None, psTurno=TURNO_INDEFINIDO, piModo=MODO_INDEFINIDO, piCount=0, psTitle="", *args, **kwargs):
		self.gbEdited = False
		self.gbWeAreThere = False
		self.gbWeAreHere = True

		self.GB_PLAY = False
		self.GB_PAUSE = False
		self.GB_STOP = False
		
		self.Procedures = []
		
		self.Turno = psTurno
		self.Modo = piModo
		self.Count = piCount

		#self.master = master
		Frame.__init__(self, master)
		self.grid()
		
		self.running = 1

		self.lbl1 = Label(self, text=psTitle)
		self.lbl1.grid()

		self.playClipBoardChecker = tkinter.Entry(self, bg="grey", fg="black", cursor="xterm", 
								state=tkinter.NORMAL, width=10) # .master undo=False, height=1,  
		self.playClipBoardChecker.bind("<Key>", self.textChanged)
		self.playClipBoardChecker.grid()


		self.PlayBtn = tkinter.Button(self, text='⏵', command=self.Play, fg='black') #.master
		self.PlayBtn.grid() # console.pack()
		self.PauseBtn = tkinter.Button(self, text='⏸', command=self.Pause, fg='black') #.master
		self.PauseBtn.grid() # console.pack()
		self.StopBtn = tkinter.Button(self, text='⏹', command=self.Stop, fg='black') #.master
		self.StopBtn.grid() # console.pack()

		
		self.periodicCall()

		self.master.master.protocol("WM_DELETE_WINDOW", self.quitCnx)

		self.console = tkinter.Button(self, text='Close', command=self.endApplication) #.master
		self.console.grid() # console.pack()
		
	
	def Type(self, psText):
		for letter in psText:
			fbClntprnt('letra:' + letter)
			pyautogui.press(letter)

	def endApplication(self):
		self.running = False

	def quitCnx(self):
		self.running = False
		self.periodicCall()

	def periodicCall(self):
		if not self.running:
			self.destroy()
			self = None
			return False
		self.master.after(100, self.periodicCall)


	def textChanged(self, event):
		thetext = self.playClipBoardChecker.get()
		print(thetext)
		self.gbEdited = True

	def ComeBack(self):
		pyautogui.keyDown('alt')
		pyautogui.press('tab')
		pyautogui.keyUp('alt')
		self.gbWeAreThere = False
		self.gbWeAreHere = True

	def GoThere(self):
		self.gbWeAreThere = True
		self.gbWeAreHere = False
		pyautogui.keyDown('alt')
		pyautogui.press('tab')
		pyautogui.keyUp('alt')
		
	def GoBackward(self, piHowMuch=0):
		pyautogui.keDown('shift')
		for i in range(0, piHowMuch):
			pyautogui.press('tab')
			time.sleep(.7)
		pyautogui.keUp('shift')

	def GoForward(self, piHowMuch=0):
		liRandom = random.randint(1,6)
		for i in range(0, piHowMuch):
			pyautogui.press('tab')
			time.sleep(liRandom/10)

	def Type(self, psCadena=None):
		liRandom = random.randint(1,7)
		for c in psCadena:
			pyautogui.press(c)
			time.sleep(liRandom/10)
	
	def UpKey(self, piHowMuch=0):
		liRandom = random.randint(1,6)
		for i in range(0, piHowMuch):
			pyautogui.press('up')
			time.sleep(liRandom/10)
	
	def PressEnter(self):
		pyautogui.press('enter')

	def PressEsc(self):
		pyautogui.press('esc')

	def RightClick(self):
		pyautogui.keyDown('shift')
		time.sleep(.2)
		pyautogui.press('F10')
		time.sleep(.4)
		pyautogui.keyUp('shift')

	def Go2AddressBar(self):
		self.usrIntrfcprntDbg("""Intentar \'posicionarse\' en la barra de direcciones (URL Path)  """)
		pyautogui.keyDown('alt')
		pyautogui.press('d')
		pyautogui.keyUp('alt')
		time.sleep(.6)
		pyautogui.hotkey('esc')

	def TextBoxEmpty(self):
		lbWeWereThere = False
		lsCurrentValue = self.playClipBoardChecker.get()
		if len(lsCurrentValue) == 0 or lsCurrentValue == EMPTY:
			return True
		return False

	def EmptyTextBoxAndClipboard(self):
		lbWeWereThere = False
		if self.gbWeAreThere:
			self.ComeBack()
			lbWeWereThere = True
			
		self.usrIntrfcprntDbg(""" Let\'s enter to the TextBox  """)
		self.playClipBoardChecker.focus_set()
		
		self.usrIntrfcprntDbg(""" Let\'s clear it:  """)
		pyautogui.press('home')
		pyautogui.keyDown('shift')
		pyautogui.press('end')
		pyautogui.keyUp('shift')
		pyautogui.press('delete')

		self.usrIntrfcprntDbg(""" Let\'s use it as a clipboard for a second:  """)
		self.Type(psCadena=EMPTY)
		pyautogui.press('home')
		pyautogui.keyDown('shift')
		pyautogui.press('end')
		pyautogui.keyUp('shift')
		pyautogui.hotkey('shift', 'del') #Se copia la cadena (en caso de que haya) al clipboard
		self.usrIntrfcprntDbg(""" Ready! They're both \'empty\' now! """)

		if lbWeWereThere:
			self.GoThere()
	

	def GetClipBoardText(self):
		lbWeWereThere = False
		if self.gbWeAreThere:
			self.ComeBack()
			lbWeWereThere = True

		self.playClipBoardChecker.focus_set()

		self.usrIntrfcprntDbg(""" \'SUBRAYAR\'  """)
		pyautogui.press('home')
		pyautogui.keyDown('shift')
		pyautogui.press('end')
		pyautogui.keyUp('shift')

		self.usrIntrfcprntDbg(""" \'BORRAR\' el Contenido del Textbox  """)
		pyautogui.press('delete')

		self.usrIntrfcprntDbg(""" \'Obtener\' el contenido del Clipboard  """)
		pyautogui.hotkey('shift', 'insert')
		if self.gbEdited and not self.TextBoxEmpty():
			thetext = self.playClipBoardChecker.get()
			self.gbEdited = False
			self.usrIntrfcprntDbg(thetext)
			if lbWeWereThere:
				GoThere()
			return thetext
		else:
			if lbWeWereThere:
				GoThere()
			return EMPTY
		
	
	def WeAreThere(self):
		liResult = None
		if self.gbWeAreThere:

			self.Go2AddressBar()

			self.usrIntrfcprntDbg(""" Intentar \'SUBRAYAR\' el Path URL  """)
			pyautogui.press('home')
			pyautogui.keyDown('shift')
			pyautogui.press('end')
			pyautogui.keyUp('shift')

			self.usrIntrfcprntDbg(""" \'COPIAR\' el Path URL al Keyboard """)
			pyautogui.hotkey('shift', 'del') #Se copia la cadena (en caso de que haya) al clipboard
			pyautogui.hotkey('esc')
			pyautogui.hotkey('shift', 'insert')
			pyautogui.hotkey('esc')
			
			self.ComeBack()
			self.playClipBoardChecker.focus_set()

			self.usrIntrfcprntDbg(""" \'SUBRAYAR\'  """)
			pyautogui.press('home')
			pyautogui.keyDown('shift')
			pyautogui.press('end')
			pyautogui.keyUp('shift')

			self.usrIntrfcprntDbg(""" \'BORRAR\' el Contenido del Textbox  """)
			pyautogui.press('delete')

			self.usrIntrfcprntDbg(""" \'Obtener\' el contenido del Clipboard  """)
			pyautogui.hotkey('shift', 'insert')
			if self.gbEdited and not self.TextBoxEmpty():
				thetext = self.playClipBoardChecker.get()
				self.gbEdited = False
				self.usrIntrfcprntDbg(""" \'Evaluarlo\'  """)
				liResult = MatchesURLSpectedRegExps(thetext)
			
			self.GoThere()

			self.EmptyTextBoxAndClipboard()
			
			if liResult == FBSITE:
				return True
			elif liResult == FBPAGE_PHOTOS:
				return True
			elif liResult == FBPAGE_ALBUMS:
				return True
			elif liResult == FBPAGE:
				return True
			elif liResult == FBPAGE_ALBUM:
				return True
			elif liResult == FB_GROUP:
				return True
			elif liResult == WEBPAGE:
				return False
			elif liResult == SOMETHING_ELSE:
				return False
		else:
			self.usrIntrfcprntDbg("It doesn\'t seem we're supposed to be there, so there\'s no need to check cause we are not there.")
		return False

	def close(self):
		print("Cerrando el UserInteraction")
		self.gbEdited = False
		self.gbWeAreThere = False
		self.gbWeAreHere = True
		if self.gbWeAreThere:
			self.ComeBack()
			self.playClipBoardChecker.focus_set()

			self.usrIntrfcprntDbg(""" \'SUBRAYAR\'  """)
			pyautogui.press('home')
			pyautogui.keyDown('shift')
			pyautogui.press('end')
			pyautogui.keyUp('shift')

			self.usrIntrfcprntDbg(""" \'BORRAR\' el Contenido del Textbox  """)
			pyautogui.press('delete')
			self.GoThere()
			
		self.destroy()
		print("Terminado.")
		
	def MatchesURLSpectedRegExps(self, psCadena):
		if(WEBPAGE_REGEX.match(psCadena.lower())):
			print("Es Página Web")
			if(FBSITE_REGEX.match(psCadena.lower())):
				print("Es Página en el Sitio de Facebook")
				if(FBGROUP_REGEX.match(psCadena.lower())):
					print("Es Página de Grupo de Facebook")
					return FB_GROUP
				elif(FBPAGE_REGEX.match(psCadena.lower())):
					print("Es una \'Página de Facebook\' de alguien.")
					if(FBPAGEPHOTOS_REGEX.match(psCadena.lower())):
						print("Es \'Página de Fotos\' de una Página de Facebook")
						return FBPAGE_PHOTOS
					elif(FBPAGEALBUMS_REGEX.match(psCadena.lower())):
						print("Es \'Página de Álbums\' de una Página de Facebook")
						return FBPAGE_ALBUMS
					elif(FBPAGEALBUM_REGEX.match(psCadena.lower())):
						print("Es Un \'Álbum\' de una Página de Facebook")
						return FBPAGE_ALBUM
					return FBPAGE
				return FBSITE
			else:
				print("NO ES Página de Facebook")
				return WEBPAGE
		return SOMETHING_ELSE



class FBRepeatPassword(Frame):

	def fbRptprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	


	def __init__(self, master=None, *args, **kwargs):
		global PASS_REPEAT
		
		self.gsPassRepeat = PASS_REPEAT

		#self.master = master
		Frame.__init__(self, master)
		self.grid()


		self.fbRptprntDbg('Loading Password Repeat Frame (Window):')
		rand = random.Random()
		#self.app = Frame(self) 
		#self.tk = master.tk

		#------------------------------------------------------------------------------------------
		# Create the queue
		#self.queue = Queue() #Queue.Queue()

		self.running = 1

		# Start the periodic call in the GUI to check if the queue contains
		# anything
		self.fbRptprntDbg("Periodic Call about to start")
		self.periodicCall()
		self.fbRptprntDbg("Periodic Call STARTED!!!")
		#------------------------------------------------------------------------------------------


		self.PassRepeatDataChanged = False


		textvariable = None
		try:
			textvariable = StringVar()
		except KeyError:
			textvariable = None



		# Set up the GUI
		fbClntprnt('Adding Password Repeat InputBox:')

		self.lbl1 = Label(self, text="Por favor confirme su contraseña:")
		self.lbl1.grid()
		self.lbl2 = Label(self, text=" ")
		self.lbl2.grid()
		self.playPasswordRepeat = tkinter.Entry(self, bg="white", fg="red", cursor="xterm", 
								state=tkinter.NORMAL) # .master height=1, width=10, undo=False, 
		self.playPasswordRepeat.bind("<Key>", self.textChanged)
		self.playPasswordRepeat.bind("<Return>", self.callPasswordChecker)#lambda e: "break")
		self.playPasswordRepeat.grid()

		fbClntprnt('Adding Send/Login InputButton:')
		self.loginButton = tkinter.Button(self, text='Sign Up!', fg="blue", command=self.callOk) #.master
		self.loginButton.grid()
		
		fbClntprnt('Adding Close Button:')
		self.console = tkinter.Button(self, text='Cancel Sign Up', command=self.endWindow) #.master
		self.console.grid() # console.pack()
		# Add more GUI stuff here

		self.master.protocol("WM_DELETE_WINDOW", self.quitCnx)
		self.playPasswordRepeat.focus_set()

	def callOk():
		self.lbl2=""
		fbRptprntDbg("Validando que coincidan las contrseñas...")
		text_here = playPasswordRepeat.get()
		text_back_there = master.playPassword.get()
		if text_here == text_back_there:
			fbRptprntDbg("Las coinciden! :D ")
			self.lbl2="Las coinciden! :D "
			master.callUserLogin()
			self.destroy()
			self = None
		else:
			fbRptprntDbg("Las contraseñas no coinciden! :(" )
			self.lbl2="Las contraseñas no coinciden! :("

	def endWindow():
		self.running = False

	"""
		method: quitCnx
		description: Disables a flag (Sets running class variable to 0) to tell the computer this 
		Window (Password Repeat window) shouldn't be alive.
	"""
	def quitCnx(self):
		self.running = False
		self.periodicCall()


	"""
		method: periodicCall
		description: This method checks for the flag (variable) which tells us if this window should still
		be running or not. If it should still be running then it leaves it like that and keeps checking
		once and again, if it should not be running then closes this Window, DB (DB Connection,) etc.
	"""
	def periodicCall(self):
		"""
		Check every 100 ms if the program has to be still running.
		"""
		if not self.running:
			self.destroy()
			self = None
			
		self.master.after(100, self.periodicCall)


"""
Class: CheckNamesThreader
description: This is an OOP (object oriented programming) class definition used to instance objects of this class.
Its purpose is to call the FBClient method called CheckNames, which purpose is to Alert And Ask Main Process Permission To 
Start Checking Group Names to mantain DB current.
"""
class CheckNamesThreader(threading.Thread):

	def chkNmsprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	def __init__(self, queue, checkNamesCommand, *args, **kwargs):
		self.queue = queue
		self.namesChecker = checkNamesCommand
		threading.Thread.__init__(self, *args, **kwargs)
		self.daemon = True
		self._stop = threading.Event()
		self.start()

	def run(self):
		global TURNO
		global MODO
		while True:
			#fbClntprntDbg("Look a while true loop that doesn't block the GUI!")
			#fbClntprntDbg("Current Thread: %s" % self.name)

			"""
			This is where we handle the asynchronous I/O. For example, it may be
			a 'select()'.
			One important thing to remember is that the thread has to yield
			control.
			"""
			if MODO != MODO_MANUAL:
				#fbClntprntDbg("/*running*/")
				line = "some text" #line = self.irc.recv(4096)
				#fbClntprntDbg(line)
				self.namesChecker()
				if line.find("http") != -1 or line.find("HTTP") != -1:
					self.queue.put(str(line))
					fbClntprntDbg(str(self.queue.qsize()))
			time.sleep(60)

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()
"""
Class: NotificationsCheckerThreader
description: This is an OOP (object oriented programming) class definition used to instance objects of this class.
Its purpose is to call the FBClient method called CheckNotifications, which purpose is to look into Notifications for
those who has something to do with our Posts and get them into the DataBase for taking care of them by the user later.
"""
class NotificationsCheckerThreader(threading.Thread):

	def ntfctnsChkrprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	def __init__(self, queue, piCount=NOTIFICATIONS_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO, *args, **kwargs):
		self.queue = queue
		threading.Thread.__init__(self, *args, **kwargs)
		self.Count = piCount
		self.Turno = psTurno
		self.Modo = piModo

		self.daemon = True
		self._stop = threading.Event()
		self.start()


	def run(self): #processIncoming(self)
		strX = "\\/"
		while True:
			#fbClntprntDbg("Look a while true loop that doesn't block the GUI!")
			#fbClntprntDbg("Current Thread: %s" % self.name)
			
			"""
			This is where we handle the asynchronous I/O. For example, it may be
			a 'select()'.
			One important thing to remember is that the thread has to yield
			control.
			"""
			if not goUI.GB_PLAY:
				if goUI.Turno==self.Turno and goUI.Modo==self.Modo:
					if goUI.Count > 0:
						fbClntprnt(str(self.Turno) + " " + str(self.Modo) + " (" + str(goUI.Count) + ")")
					else:
						goUI.Procedures.remove(NOTIFICATIONS)
						fbClntprnt(str(goUI.Turno) + " " + str(goUI.Modo) + " (" + str(goUI.Count) + ")")
				elif not NOTIFICATIONS in goUI.Procedures: 
					goUI.Procedures.append(NOTIFICATIONS)
					fbClntprnt(NOTIFICATIONS + " is now programmed to Run soon.")
				else:
					fbClntprnt("Notifications is already in Procedures")
			else:
				liI = random.randint(0,1)
				fbClntprnt(strX[liI])
			time.sleep(2)


	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

class NotificationsCheckerSecondThreader(threading.Thread):

	def ntfctnsChkrprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	def __init__(self, queue, notificationsCheckerCommand, piCount=NOTIFICATIONS_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO, *args, **kwargs):
		self.queue = queue
		self.notificationsCheckerCommand = notificationsCheckerCommand
		threading.Thread.__init__(self, *args, **kwargs)

		self.Count = piCount
		self.Turno = psTurno
		self.Modo = piModo

		self.daemon = True
		self._stop = threading.Event()
		self.start()
		
	def run(self):
		strX = "-|"
		while True:
			"""
			
			"""
			## Check contents of message and do what it says
			## As a test, we simply print it
			if not goUI.GB_PLAY:
				if len(goUI.Procedures) > 0:
					if not goUI.Turno==self.Turno or not goUI.Modo==self.Modo:
						fbClntprnt("Turno: " + str(goUI.Turno) + ", Modo: " + str(goUI.Modo) + " vs. Turno: " + str(self.Turno) + ", Modo: " + str(self.Modo) + ")")
						if NOTIFICATIONS in goUI.Procedures:
							if goUI.Procedures[0] == NOTIFICATIONS:
								fbClntprnt("Attempting to run notificationsChecker now... ")
								self.notificationsCheckerCommand(maxCount=self.Count, psTurno=self.Turno, piModo=self.Modo)
							else:
								fbClntprnt("Procedures\[0\] != Notifications")
						else:
							fbClntprnt("Notifications isn't in Procedures yet.")
					else:
						fbClntprnt("Something else is Already Running \( " + str(goUI.Turno) + ", " + str(goUI.Modo) + "\)")
				else:
					fbClntprnt("Procedures is Empty")
			else:
				liI = random.randint(0,1)
				fbClntprnt(strX[liI])
			time.sleep(2)

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

class ActivityRegCheckerThreader(threading.Thread):

	def actvtRgChkrprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	def __init__(self, queue, checkActivityRegCommand, *args, **kwargs):
		self.queue = queue
		self.activityRegCheckerCommand = checkActivityRegCommand
		threading.Thread.__init__(self, *args, **kwargs)
		self.daemon = True
		self._stop = threading.Event()
		self.start()
		
	def run(self):
		while True:
			"""
			
			"""
			if self.queue.qsize():
				try:
					msg = self.queue.get(0)
					## Check contents of message and do what it says
					## As a test, we simply print it
					actvtRgChkrprntDbg("Sending Message from queue (" + str(msg) + ") to Message Checker... ")
					self.activityRegCheckerCommand(str(msg))
				except queue.Empty:
					print("-")
					pass
			time.sleep(.5)

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()


"""
Class: FBClient(Frame)
description: It's a frame put on the window (master) at the beginning, containing 
the basic objects which allow you to interact with the Database (DB Connection) behaving as the Automated User Interface.

"""
class FBClient(Frame):

	def fbClntprntDbg(self, psTexto, psUtf8=""):
		global DEBUG_MODE
		if DEBUG_MODE:
			print(datetime.now().strftime('(%d-%m-%Y %H:%M:%S)') + " dbg.- " + psTexto, psUtf8)	

	"""
		method: quitCnx
		description: Disables a flag (Sets running class variable to 0) to tell the computer this 
		Window (Main Window [Login window]) shouldn't be alive anymore.
	"""
	def quitCnx(self):
		self.running = False
		self.periodicCall()

	"""
		method: endApplication
		description: Disables a flag (Sets running class variable to 0) to tell the computer this 
		Window (FB Connection [FBClass instance])	shouldn't be alive anymore. This method is different
		from the previous one, since this method is called when the window is closed by the user 
		when he/she clicks the "x" button on the upper corner of the window.
	"""
	def endApplication(self):
		self.running = False


	"""
		method: periodicCall
		description: This method checks for the flag (variable) which tells us if this window should still
		be running or not. If it should still be running then it leaves it like that and keeps checking
		once and again, if it should not be running then closes this Window, DB (DB Connection,) etc.
	"""
	def periodicCall(self):
		"""
		Check every 100 ms if the program has to be still running.
		"""
		if not self.running:
			# This is the brutal stop of the system. You may want to do
			# some cleanup before actually shutting it down.
			
			ClosingFBClient(theFBClientToClose=self)
			
		self.master.after(100, self.periodicCall)

	def OpenConection(self):
		global STATUS_EXPIRED
		global STATUS_CANCELED
		global STATUS_POSTING
		global STATUS_PARTIALLY_POSTED
		global STATUS_POSTED
		global STATUS_VALID
		global STATUS_COMPLETED
		global STATUS_DELIVERED
		global STATUS_HANDED
		global STATUS_FINISHED

		global gaNotifications
		global gaPosts
		global gaAlbums
		
		lbOpenConnection = False
		
		fbClntprnt('opening conection...')
		self.Cnx = sqlite3.connect(self.dicParams['DB_FILE'])
		crsr = self.Cnx.cursor()
		
		lbOpenConnection = True
		
		return lbOpenConnection
		
		fbClntprnt("Se conectó a la db.")

		
		lbOpenConnection = False
		self.fbClntprntDbg("Updating log:")

		laPasswordSalts = []
		for row in crsr.execute('SELECT status, PasswordSalt FROM Users USR ' \
				' WHERE Username = ? And length(USR.EncryptedPassword) > 0 ', USER_STATUS_CLIENT_OCATIONALLY, psUsername):
			laPasswordSalts.append((row[0], row[1]))
			
		crsr.execute('SELECT idUser FROM Users USR ' \
			' WHERE USR.Username = ? And USR.EncryptedPassword = ? ', self.dicParams['FB_USERNAME'], gsEncryptedPassword)
		liRow = crsr.fetchone()
		liRowCount0 = liRow[0]
		liIdUser = liRow[1]
	
		lbOpenConnection = True

		self.fbClntprntDbg(liRowCount, " records found.")

		if liRowCount > 0:
			#Since there is a conection and presumibly a Log Table, Let's try to add a new log register.

			self.fbClntprntDbg("Actualizando el registro de acceso (log.)..")

			lbOpenConnection = False
			
			#liIdUser =
			lsBehavior = gbPARAMS[liInt]['FB_CONNECTION']
			ldtAhoraMismo = datetime.now()
			lsMensaje = "Se ha conectado a la Base de Datos..."

			crsr.execute('INSERT INTO log (idUser, idBehavior, datWhen, strMessage) ' \
						'Values(?, ?, ?, ?) ', liIdUser, lsBehavior, ldtAhoraMismo, lsMensaje)
			liRowCount1 = crsr.fetchone()[0]

			crsr.execute('SELECT ' \
						' count(*) ' \
						'FROM log L  ' \
						' Inner Join User USR ON L.idUser = USR.idUser ' \
						' Inner Join Behavior BHVR ON L.idBehavior = BHVR.idBehavior ' \
						'WHERE ' \
						' USR.user = \'' + self.dicParams['FB_USERNAME'] + '\' AND ' \
						' BHVR.idBehavior = \'' + poParams['FB_CONNECTION'] + '\' ' )
			liRowCount2 = crsr.fetchone()[0]
			if liRowCount2 > liRowCount0:
				self.fbClntprntDbg('Connection established and log written...')
				return True
			
			lbOpenConnection = True

		return lbOpenConnection


		lidGrupoDePublicaciones = None

		giBrowndex = -1

		if gbPARAMS[liInt]['FB_CONNECTION'] == "notifications":

			crsr.execute('SELECT ' \
						' count(*)' \
						'FROM ' \
						' Notifications N Inner Join ' \
						' User USR on USR.idUser = N.idUserHere ' \
						' Profile P on P.ProfileId = N.HisHerProfileId or FBP.Username = N.HisHerUsername  ' \
						'WHERE N.status <> ' + str(STATUS_CANCELED))
			liRowCount = crsr.fetchone()[0]
	
			self.fbClntprntDbg("Se encontraron ", liRowCount, " registros")
	
			if liRowCount > 0:
				for row in crsr.execute('SELECT ' \
						' N.idNotification,' \
						' N.isItAboutUs,' \
						' N.HisHerUsername,' \
						' N.HisHerProfileId,' \
						' N.idUserHere,' \
						' N.URL,' \
						' N.OurPostId,' \
						' N.IsItOnOurPage,' \
						' N.PageUsername,' \
						' N.PageId,' \
						' N.IsItInsideOurWall,' \
						' N.IsItInsideAGroupWeAreIn,' \
						' N.GroupUsername,' \
						' N.GroupId' \
						'FROM ' \
						' Notifications N Inner Join ' \
						' User USR on USR.idUser = N.idUserHere ' \
						' Profile P on P.Username = N.HisHerUsername or P.ProfileId = N.HisHerProfileId ' \
						'WHERE N.status <> ? ', str(STATUS_CANCELED)):
					#	crsr.execute('SELECT ' \
					#					' P.idGrupoDePublicaciones, ' \
					#					' idPublicacion, ' \
					#					' sURL, ' \
					#					' GMYP.iCurrentGroupStatus, ' \
					#					' sCurrentFacebookNameOrId, ' \
					#					' Estatus, ' \
					#					' GMYP.idGrupoMuroPagina, ' \
					#					' GMYP.idOwner, ' \
					#					' idProductoServicio, ' \
					#					' sName ' \
					#					'FROM ' \
					#					' Publicaciones P Inner Join ' \
					#					' GruposDePublicaciones GDP on P.idGrupoDePublicaciones = GDP.idGrupoDePublicaciones Inner Join ' \
					#					' GruposMurosYPaginas GMYP on GMYP.idGrupoMuroPagina = P.idGrupoMuroPagina ' \
					#					'WHERE GDP.EstaVigente > 0 And Estatus <= ? ', ):
					lbExiste = False
					for item in gaNotifications:
						if item[0] ==row[0]:
							lbExiste = True
							break
					if not lbExiste:
						gaNotifications.append(row)
						continue
		elif gbPARAMS[liInt]['FB_CONNECTION'] == "post":
			crsr.execute('SELECT ' \
						' count(*)' \
						'FROM ' \
						' Posts PST Inner Join ' \
						' User USR on USR.idUser = PST.idUserHere ' \
						' Profile P on P.ProfileId = PST.HisHerProfileId or P.Username = PST.HisHerUsername  ' \
						'WHERE PST.status <> ' + str(STATUS_CANCELED))
			liRowCount = crsr.fetchone()[0]
	
			self.fbClntprntDbg("Se encontraron ", liRowCount, " Publicaciones No Canceladas")
	
			if liRowCount > 0:
				for row in crsr.execute('SELECT ' \
						' PST.idPost,' \
						'FROM ' \
						' Posts PST Inner Join ' \
						' User USR on USR.idUser = PST.idUserHere ' \
						' Profile P on P.Username = PST.HisHerUsername or P.ProfileId = PST.HisHerProfileId ' \
						'WHERE PST.status <> ? ', str(STATUS_CANCELED)):
					#	crsr.execute('SELECT ' \
					#					' P.idGrupoDePublicaciones, ' \
					#					' idPublicacion, ' \
					#					' sURL, ' \
					#					' GMYP.iCurrentGroupStatus, ' \
					#					' sCurrentFacebookNameOrId, ' \
					#					' Estatus, ' \
					#					' GMYP.idGrupoMuroPagina, ' \
					#					' GMYP.idOwner, ' \
					#					' idProductoServicio, ' \
					#					' sName ' \
					#					'FROM ' \
					#					' Publicaciones P Inner Join ' \
					#					' GruposDePublicaciones GDP on P.idGrupoDePublicaciones = GDP.idGrupoDePublicaciones Inner Join ' \
					#					' GruposMurosYPaginas GMYP on GMYP.idGrupoMuroPagina = P.idGrupoMuroPagina ' \
					#					'WHERE GDP.EstaVigente > 0 And Estatus <= ? ', ):
					lbExiste = False
					for item in gaPosts:
						if item[0] ==row[0]:
							lbExiste = True
							break
					if not lbExiste:
						gaPosts.append(row)
						continue

		elif gbPARAMS[liInt]['FB_CONNECTION'] == "album":
			crsr.execute('SELECT ' \
						' count(*)' \
						'FROM ' \
						' Albums A Inner Join ' \
						' User USR on USR.idUser = A.idUserHere ' \
						' Profile P on P.ProfileId = A.HisHerProfileId or P.Username = A.HisHerUsername  ' \
						'WHERE A.status <> ' + str(STATUS_CANCELED))
			liRowCount = crsr.fetchone()[0]
	
			self.fbClntprntDbg("Se encontraron ", liRowCount, " Albums No Cancelados")
	
			if liRowCount > 0:
				for row in crsr.execute('SELECT ' \
						' A.idAlbum,' \
						'FROM ' \
						' Albums A Inner Join ' \
						' User USR on USR.idUser = A.idUserHere ' \
						' Profile P on P.Username = A.HisHerUsername or P.ProfileId = A.HisHerProfileId ' \
						'WHERE A.status <> ? ', str(STATUS_CANCELED)):
					#	crsr.execute('SELECT ' \
					#					' P.idGrupoDePublicaciones, ' \
					#					' idPublicacion, ' \
					#					' sURL, ' \
					#					' GMYP.iCurrentGroupStatus, ' \
					#					' sCurrentFacebookNameOrId, ' \
					#					' Estatus, ' \
					#					' GMYP.idGrupoMuroPagina, ' \
					#					' GMYP.idOwner, ' \
					#					' idProductoServicio, ' \
					#					' sName ' \
					#					'FROM ' \
					#					' Publicaciones P Inner Join ' \
					#					' GruposDePublicaciones GDP on P.idGrupoDePublicaciones = GDP.idGrupoDePublicaciones Inner Join ' \
					#					' GruposMurosYPaginas GMYP on GMYP.idGrupoMuroPagina = P.idGrupoMuroPagina ' \
					#					'WHERE GDP.EstaVigente > 0 And Estatus <= ? ', ):
					lbExiste = False
					for item in gaAlbums:
						if item[0] ==row[0]:
							lbExiste = True
							break
					if not lbExiste:
						gaAlbums.append(row)
						continue
		self.Cnx.commit()
		crsr.close()
		crsr = None
		

	def ClosingDBConnection(self):
		global client
	
		fbClntprnt(self.dicParams['FB_CONNECTION'] + "\'s saying good bye to the DB !")

		fbClntprnt("Commiting  " + self.dicParams['FB_CONNECTION'] + "\'s DB Changes !!!")
		self.Cnx.commit()

		fbClntprnt("Closing  " + self.dicParams['FB_CONNECTION'] + "\'s DB Conection !!!")
		self.Cnx.close()

		fbClntprnt("Setting  " + self.dicParams['FB_CONNECTION'] + "\'s DB Conection to NONE !!!")
		self.Cnx = None

#......Database Definition................................................................

	def Notifications_TableCreate(self):
		self.fbClntprntDbg("Creating Notifications Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 NOTIFICATIONS Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION'] == "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums" :
			loCrsr.execute('''CREATE TABLE if not exists Notifications
				(idNotification integer,
					bisNotifAboutUs Boolean,
					sHisHerUsername varchar(128),
					rHisHerFBProfileId real,
					iidUser integer,
					sURL text,
					iOurPostId integer,
					bIsItOnOurPage Boolean,
					sPageUsername text,
					rPageId real,
					bIsItInsideOurWall Boolean,
					bIsItInsideAGroupWeAreIn Boolean,
					sGroupUsername text,
					rGroupId real)''')
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing Notifications Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None

	
	def Posts_TableCreate(self):
		self.fbClntprntDbg("Creating POSTS Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished for POSTS Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION'] == "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists Posts
				(iidPost integer,
					iidAlbum integer,
					bisThisPostOurs Boolean,
					iidUserOwner integer,
					sWhatDoYouSell varchar(128),
					nPrice numeric(7,7),
					sWH3R3 varchar(128),
					sDescription text,
					sLocalPicturesPath varchar(254))''') \
			#liRow = self.crsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing POSTS Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None
	
	
	def OfertasDeVenta_TableCreate(self):
		self.fbClntprntDbg("Creating OFERTASDEVENTA Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished for OFERTASDEVENTA Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION'] == "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists OfertasDeVenta
				(iidOfertaDeVenta integer,
					bWeProduceIt Boolean,
					iidUserOwner integer,
					bItsAProduct Boolean,
					bItsAService Boolean,
					bItsJustOnePS Boolean,
					bMultiplePS Boolean,
					bSamePriceForEachPS Boolean,
					bDistinctPrice4EachPS Boolean,
					nPrice numeric(7,7),
					datPriceDate datetime)''') \
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing PRODUCTSERVICE4SALE Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None


	def Albums_TableCreate(self):
		self.fbClntprntDbg("Creating ALBUMS Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 ALBUMS Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION'] == "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists Albums
				(iidAlbum integer,
					bisThisAlbumOurs Boolean,
					iidUserOwner integer)''') \
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing ALBUMS Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None


	def Users_TableCreate(self):
		self.fbClntprntDbg("Creating Users Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 USERS Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION']== "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists Users
				(iidUser integer,
					sName varchar(64),
					sUsername varchar(32),
					datDateAdded datetime,
					sEncryptedPassword varchar(32),
					rFBProfileId real,
					sPasswordSalt varchar(255),
					iStatus integer)''') 
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing USERS Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None
		
	def Log_TableCreate(self):
		self.fbClntprntDbg("Creating LOG Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 LOG Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION'] == 'notifications' or \
			self.dicParams['FB_CONNECTION'] == 'posts' or \
			self.dicParams['FB_CONNECTION'] == 'albums':
			loCrsr.execute('''CREATE TABLE if not exists log
				(iidUser integer, 
					datWhen datetime, 
					strMessage text)''')
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing LOG Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None

	def FBProfiles_TableCreate(self):
		self.fbClntprntDbg("Creating FB-PROFILES Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 FB-PROFILES Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION']== "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists FBProfiles
				(iidProfile,
					sName varchar(64),
					iFBProfileId integer,
					sUsername varchar(32))''') \
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing FB-PROFILES Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None

	def MPG_TableCreate(self):
		self.fbClntprntDbg("Creating MPG (Wall/Page/Group) Table.")
		self.fbClntprntDbg("Opening specific db connection (just for this.)")
		loCnx = sqlite3.connect(self.dicParams['DB_FILE'])
		self.fbClntprntDbg("¡Specific DB Connection stablished 4 MPG Table Creation!")
		loCrsr = loCnx.cursor()
		self.fbClntprntDbg("Cursor Created")
		if self.dicParams['FB_CONNECTION']== "notifications" or \
			self.dicParams['FB_CONNECTION'] == "posts" or \
			self.dicParams['FB_CONNECTION'] == "albums":
			loCrsr.execute('''CREATE TABLE if not exists MPG
				(iidMPG,
					sName varchar(64),
					iFBId integer,
					sFBUsername varchar(32),
					iidUserOwner integer,
					iidUserMember integer,
					bViwersAreMaleGender Boolean,
					bViwersAreFemaleGender Boolean,
					bViwersAreMixedGender Boolean,
					bNorthArea Boolean,
					bSouthArea Boolean,
					bEastArea Boolean,
					bWestArea Boolean,
					bWholeCity Boolean)''') \
			#liRow = loCrsr.fetchone()
		self.fbClntprntDbg("Closing Cursor...")
		loCrsr.close()
		self.fbClntprntDbg("Closing FB-PROFILES Specific Connection...")
		loCnx.close()
		loCrsr = None
		loCnx = None



#...... UserLogin METHOD ................................................................

	def UserLogin(psUserToVerify, psPassToVerify):
		loCrsr = self.Cnx.cursor()
		for row in loCrsr.execute('SELECT PasswordSalt, EncryptedPassword FROM Users USR ' \
					' WHERE Username = ? and status not in (?, ?, ?)', psUserToVerify, \
					USER_STATUS_EXPIRED, USER_STATUS_CANCELED, USER_STATUS_FINISHED):
			self.fbclntprntDbg(row(0), ", ", "row(1)")
			if self.EncryptString(psPassToVerify, row(0), False) == row(1):
				return True
		return False
			
	
	
#...... __INIT__ METHOD ................................................................

	"""
		Method: __init__
		description: This FBClient's method runs at the begining of its creation, making some
		needed tasks for it to start working: 1) Opens the DB Connection to the specified 
		Database (stablished inside pdicParams), 2)Creates and starts CheckNamesThreader and NotificationsCheckerThreader instances
		which will be staying around doing what's described on it's definition, 3) Sets the GUI (
		The TextArea, Send Button and Close Button) for it to work as spected.
	"""
	def __init__(self, master=None, pdicParams=None, psTitle="Login", *args, **kwargs):
		global goUI
		global USER_HERE
		global PASS_HERE
		global JOIN
		global gbLoggedIn
		
		self.gsUsername = USER_HERE
		self.gsPassword = PASS_HERE

		self.mute = True
		self.dicParams = pdicParams
		
		#self.master = master
		Frame.__init__(self, master)
		self.grid()
		
		if psTitle==CHECKNAMES:
			lsTitle = "@Check Names"
		elif psTitle==NOTIFICATIONS:
			lsTitle = "@Notifications"
		elif psTitle==SPECIFIC_POST:
			lsTitle = "@Specific Post"
		elif psTitle==SPECIFIC_ALBUM:
			lsTitle = "@Specific Album"
		elif psTitle==ACTIVITYREG:
			lsTitle = "@Activities Registry"

		self.master.title(lsTitle)

		#......file..................................................
		#directory = "C:\\irc"
		#if not os.path.exists(directory):
		#	os.makedirs(directory)
		#target = open(os.path.join(directory,"file.txt"), 'w')
		##/sdcar/folder/file.py for android remove the join etc

		fbClntprnt('Loading first Frame:')
		rand = random.Random()
		#self.app = Frame(self) 
		#self.tk = master.tk

		#------------------------------------------------------------------------------------------
		# Create the queue
		self.queue = Queue() #Queue.Queue()


		#------------------------------------------------------------------------------------------
		# Check Database Tables (create a table if it doesn't exist)
		self.Notifications_TableCreate()
		self.Posts_TableCreate()
		self.Albums_TableCreate()
		self.Users_TableCreate()
		self.Log_TableCreate()
		self.MPG_TableCreate()
		self.FBProfiles_TableCreate()

		#------------------------------------------------------------------------------------------
		# Open DB Connection
		if not self.OpenConection():
			self.fbClntprnt('Couldn\'t establish Database Connection this time.')

		self.running = 1

		ntfWindow = tkinter.Toplevel()
		
		if goUI==None:
			if psTitle==CHECKNAMES:
				goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_CHECKNAMES, piModo=MODO_MANUAL, piCount=CHECKNAMES_MAXCOUNT, psTitle=lsTitle)
			elif psTitle==NOTIFICATIONS:
				goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_MANUAL, piCount=NOTIFICATIONS_MAXCOUNT, psTitle=lsTitle)
			elif psTitle==SPECIFIC_POST:
				goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_POSTS, piModo=MODO_MANUAL, piCount=SPECIFIC_POST_MAXCOUNT, psTitle=lsTitle)
			elif psTitle==SPECIFIC_ALBUM:
				goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_ALBUMS, piModo=MODO_MANUAL, piCount=SPECIFIC_ALBUM_MAXCOUNT, psTitle=lsTitle)
			elif psTitle==ACTIVITYREG:
				goUI = UserInteraction(master=ntfWindow, psTurno=TURNO_REGISTRO_DE_ACTIVIDAD, piModo=MODO_MANUAL, piCount=ACTIVITYREG_MAXCOUNT, psTitle=lsTitle)
		#elif goUI!=None: NO
		#	if psTitle==CHECKNAMES: NO
		#		goUI.Turno=TURNO_CHECKNAMES
		#		goUI.Modo=MODO_MANUAL
		#		goUI.Count=CHECKNAMES_MAXCOUNT
		#		goUI.master.title=lsTitle
		#	elif psTitle==NOTIFICATIONS: NO
		#		goUI.Turno=TURNO_CHECKNAMES
		#		goUI.Modo=MODO_MANUAL
		#		goUI.Count=NOTIFICATIONS_MAXCOUNT
		#		goUI.master.title=lsTitle
		#	elif psTitle==SPECIFIC_POST: NO
		#		goUI.Turno=TURNO_CHECKNAMES
		#		goUI.Modo=MODO_MANUAL
		#		goUI.Count=SPECIFIC_POST_MAXCOUNT
		#		goUI.master.title=lsTitle
		#	elif psTitle==SPECIFIC_ALBUM: NO
		#		goUI.Turno=TURNO_CHECKNAMES
		#		goUI.Modo=MODO_MANUAL
		#		goUI.Count=SPECIFIC_ALBUM_MAXCOUNT
		#		goUI.master.title=lsTitle
		#	elif psTitle==ACTIVITYREG: NO
		#		goUI.Turno=TURNO_CHECKNAMES
		#		goUI.Modo=MODO_MANUAL
		#		goUI.Count=ACTIVITYREG_MAXCOUNT
		#		goUI.master.title=lsTitle

		fbClntprnt("Periodic Call about to start")
		self.periodicCall()
		fbClntprnt("Periodic Call STARTED!!!")
		#------------------------------------------------------------------------------------------


		self.UserAuthDataChanged = False


		textvariable = None
		try:
			textvariable = StringVar()
		except KeyError:
			textvariable = None

		InnerFrame = Frame(self, width=768, height=576, bg="", colormap="new")

		# Set up the GUI
		fbClntprnt('Adding Username InputBox:')
		self.playUsername = tkinter.Entry(InnerFrame, bg="white", fg="black", cursor="xterm", 
								state=tkinter.NORMAL) # .master height=1, width=10,  undo=False, 
		self.playUsername.bind("<Key>", self.usernameChanged)
		self.playUsername.bind("<Return>", self.callUsernameChecker)#lambda e: "break")
		self.playUsername.grid()

		fbClntprnt('Adding Pasword InputBox:')
		self.playPassword = tkinter.Entry(InnerFrame, bg="white", fg="black", cursor="xterm", 
								state=tkinter.NORMAL) # .master height=1, width=10,  undo=False, 
		self.playPassword.bind("<Key>", self.passwordChanged)
		self.playPassword.bind("<Return>", self.callPasswordChecker)#lambda e: "break")
		self.playPassword.grid()

		fbClntprnt('Adding Send/Login InputButton:')
		self.loginButton = tkinter.Button(InnerFrame, text='Sign In', fg="blue", command=self.callUserLogin) #.master
		self.loginButton.grid()
		
		self.SignUpButton = tkinter.Button(InnerFrame, text='Sign Up', fg="green", command=self.callSignUp) #.master
		self.SignUpButton.grid()
		
		if gbLoggedIn:
			InnerFrame.grid_remove()
		else:
			InnerFrame.grid()

		fbClntprnt('Adding Close Button:')
		self.console = tkinter.Button(self, text='Close', command=self.endApplication) #.master
		self.console.grid() # console.pack()
		# Add more GUI stuff here

		#playButton.pack(side=TOP)
		#stopButton.pack(side=BOTTOM)

		# Set up the thread to do asynchronous I/O
		# More can be made if necessary
#		self.thread1 = CheckNamesThreader(queue=self.queue, checkNamesCommand=lambda: CheckNames(ACTIVITYREG_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO)) #, target=self.workerThread1

		#self.thread3 = NotificationsCheckerThreader(queue=self.queue, piCount=NOTIFICATIONS_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO)
		#self.thread4 = NotificationsCheckerSecondThreader(queue=self.queue, notificationsCheckerCommand=CheckNotifications, piCount=NOTIFICATIONS_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO)

#		self.thread5 = ActivityRegCheckerThreader(queue=self.queue, checkActivityRegCommand=lambda: ActivityRegChecker(ACTIVITYREG_MAXCOUNT, psTurno=TURNO_NOTIFICACIONES, piModo=MODO_AUTOMATICO))

		# Start the periodic call in the GUI to check if the queue contains
		# anything

		self.master.protocol("WM_DELETE_WINDOW", self.quitCnx)
		
		
	


	def callUsernameChecker(self, event):
		x=""

	def callPasswordChecker(self, event):
		x=""
    	
	def usernameChanged(self, event):
		x=""
    
    	
	"""
	method: passwordChanged
	description: Enables a flag (Sets UserAuthDataChanged variable to True) when the TextArea of the Window has been edited.
	"""
	def passwordChanged(self, event):
		lsText = self.playPassword.get()
		self.GetNewSalt2EncryptString(lsText)
		self.UserAuthDataChanged = True


	def Authenticate(self, psIncomingUsername, psIncomingPassword, psSalt, piStatus):
		lbAuthenticated = False
		return lbAuthenticated
	
	
	def EncryptString(self, psString, psSalt, pbRemixSalt=False):
		lsEncryptedString = u''
		#lsSpacio = " "
		#lsEncryptedString = lsSpacio.encode('raw_unicode_escape')
		liCount = 0
		ljCount = 0
		lsFinalSalt = ''
		#for x in filter(str.isdigit, str(psString)):
		#	liCount = liCount + 1
		#	for y in filter(str.isdigit, str(psSalt)):
		#		ljCount = ljCount + 1
		#		if int(x) > int(y):
		#			r = random.randint(0,len(psString) - 1)
		#			lsEncryptedString += str(psString[r])
		#			break
		#		elif int(x) <= int(y):
		#			r = random.randint(0,len(psSalt) - 1)
		#			lsEncryptedString += str(psSalt[r])
		#			break
		if pbRemixSalt:
			for stringletter in psString:
				for saltletter in random.choice(psSalt.replace(" ",'')):
					#str1 = stringletter.encode('raw_unicode_escape')
					#str2 = saltletter.encode('raw_unicode_escape')
					lbtstringletter1 = cgi.escape(stringletter).encode('ascii', 'xmlcharrefreplace')
					lbtsaltletter2 = cgi.escape(saltletter).encode('ascii', 'xmlcharrefreplace')
					str1 = str(lbtstringletter1)
					str2 = str(lbtsaltletter2)
					if len(str1) == 1 and (not str1.find(b"&") == 0 and not str1.find(b"#") == 1 and not str1.find(b";") == (len(str1) - 1)):
						str1 = '&#' + ord(str1) + ';'
					if len(str2) == 1 and (not str2.find(b"&") == 0 or not str2.find(b"#") == 1 and not str2.find(b";") == (len(str2) - 1)):
						str2 = '&#' + ord(str2) + ';'
					if int(re.findall('\d+', str1)) > int(re.findall('\d+', str2)):
						self.fbClntprntDbg(stringletter, "(", str(str1), "), ", saltletter, " (", str(str2), ")")
						lsEncryptedString += str(stringletter)
						lsFinalSalt += str(saltletter)
						break
					elif int(re.findall('\d+', str1 )[0]) <= int(re.findall('\d+', str2 )[0]):
						self.fbClntprntDbg(stringletter, "(", str(str1), "), ", saltletter, " (", str(str2), ")")
						lsEncryptedString += str(saltletter)
						lsFinalSalt += str(saltletter)
						break
		elif not pbRemixSalt:
			for stringletter in psString:
				for i in range(0, len(psSalt) - 1):
					saltletter = psSalt[i]
					#str1 = stringletter.encode('raw_unicode_escape')
					#str2 = saltletter.encode('raw_unicode_escape')
					lbtstringletter1 = cgi.escape(stringletter).encode('ascii', 'xmlcharrefreplace')
					lbtsaltletter2 = cgi.escape(saltletter).encode('ascii', 'xmlcharrefreplace')
					str1 = str(lbtstringletter1)
					str2 = str(lbtsaltletter2)
					if len(str1) == 1 and (not str1.find(b"&") == 0 or not str1.find(b"#") == 1 and not str1.find(b";") == (len(str1) - 1)):
						str1 = '&#' + ord(str1) + ';'
					if len(str2) == 1 and (not str2.find(b"&") == 0 or not str2.find(b"#") == 1 and not str2.find(b";") == (len(str2) - 1)):
						str2 = '&#' + ord(str2) + ';'
					if int(re.findall('\d+', str(str1))[0]) > int(re.findall('\d+', str(str2))[0]):
						self.fbClntprntDbg(stringletter, "(", str(str1), "), ", saltletter, " (", str(str2), ")")
						lsEncryptedString += str(stringletter)
						lsFinalSalt += str(saltletter)
						break
					elif int(re.findall('\d+', str(str1))[0]) <= int(re.findall('\d+', str(str2))[0]):
						self.fbClntprntDbg(stringletter, "(", str(str1), "), ", saltletter, " (", str(str2), ")")
						lsEncryptedString += str(saltletter)
						lsFinalSalt += str(saltletter)
						break
		return lsEncryptedString

	def GetNewSalt2EncryptString(psCadena):
		liCount = 0
		l = len(psCadena)
		utf8_seq = u''
		for i in range(0, l):
			rndmint = random.randint(liCount + 32, 32593)
			self.fbClntprntDbg(str(i), ".- ", str(rndmint), chr(rndmint))
			utf8_seq += chr(rndmint)
		return utf8_seq



	def callSignUp(self, *args, **kvargs):
		self.reptPass = FBRepeatPassword(master=self)
		self.reptPass.master.title("Repita su Contraseña:")
		#fbClntprntDbg("/* " + self.dicParams['FB_BEHAVIOR'] + "  @" + self.dicParams['FB_USERNAME'] + "'s " + self.dicParams['FB_CONNECTION'] + " must have been started by now. */")
		liInteger = 0
	
	

	"""
		method: callUserLogin
		description: 
	"""
	def callUserLogin(self, *args, **kwargs):
		global TEXT_HERE
		global gbLoggedIn
	
		if not self.gbEdited:
			fbClntprntDbg("It's not allowed to login nor anonimously neither twice!")
		else:
			self.fbClntprntDbg(TEXT_HERE)
			self.fbClntprntDbg(self.playUsername.get( 1.0, tkinter.END ))
			self.gsUserToVerify = self.gsUserToVerify.replace(USER_HERE, self.playUsername.get( 1.0, tkinter.END )) 
			self.gsUserToVerify = self.gsUserToVerify.replace("\n", "")
			self.gsUserToVerify = self.gsUserToVerify.replace("\r", "")
			self.gsPassToVerify = self.gsPassToVerify.replace(PASS_HERE, self.playPassword.get( 1.0, tkinter.END )) 
			self.gsPassToVerify = self.gsPassToVerify.replace("\n", "")
			self.gsPassToVerify = self.gsPassToVerify.replace("\r", "")
			if self.UserLogin(self.gsUserToVerify, self.gsPassToVerify):
				self.fbClntprntDbg("Authentication Succesfull!!!")
				self.gsUsername = self.USER_HERE
				self.gsPassword = self.PASS_HERE
				self.gbEdited = False
				self.playUsername.delete('1.0', tkinter.END)
				self.playPassword.delete('1.0', tkinter.END)
				gbLoggedIn = True
			else:
				gbLoggedIn = False
				self.fbClntprntDbg("Hasn't got back!!")
		if gbLoggedIn:
			InnerFrame.grid_remove()
		else:
			InnerFrame.grid()


#......close................................................................

"""
	method: quitApp
	description: This global method (outside oop) is called when you want to get out of this program 
	closing each and every Window/Connection/etc.
"""
def quitApp():
	global gbRunning
	gbRunning = False
	for liInt in range(0, len(sys.argv)):
		if str(sys.argv[liInt]).lower() == "-notifications" or str(sys.argv[liInt]).lower() == "-posts" or str(sys.argv[liInt]).lower() == "-albums":
			client[liInt].quitCnx()
	if tkinter.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()
		sys.exit(1)

#......open................................................................
"""
	method: ToCreateCnx
	description: Used To instantiate each and every FBClient you wanted to open from the begining.
	Note.- Each FB Connection you spect to connect should open a separate Window for it.
"""
def ToCreateCnx(poWindow=None, poParams=None, psTitle=None): #run(self)
	"""
	This is where we handle the asynchronous I/O. For example, it may be
	a 'select()'.
	One important thing to remember is that the thread has to yield
	control.
	"""
	fbClntprnt("/*starting: " + poParams['FB_BEHAVIOR'] + "  @" + poParams['FB_USERNAME'] + "'s " + poParams['FB_CONNECTION'] + " */")
	#time.sleep(.4)

	loFBClient = FBClient(master=poWindow, pdicParams=poParams, psTitle=psTitle)
	#tkinter.Label(window, text=self.title).pack()		
	
	#self.FBClient.mainloop()
	fbClntprnt("/* " + poParams['FB_BEHAVIOR'] + "  @" + poParams['FB_USERNAME'] + "'s " + poParams['FB_CONNECTION'] + " must have been started by now. */")
	#time.sleep(.4)

	return loFBClient


#......open................................................................
"""
"""
def ToCreateReader(poWindow=None, poParams=None, psTitle=None): #run(self)
	"""
	"""
	fbClntprnt("/*starting: " + poParams['FB_BEHAVIOR'] + "  @" + poParams['FB_USERNAME'] + "'s " + poParams['FB_CONNECTION'] + " */")
	#time.sleep(.4)

	loFBClient = PostRaiser(master=poWindow, pdicParams=poParams, psTitle=psTitle)
	#tkinter.Label(window, text=self.title).pack()		
	
	#self.FBClient.mainloop()
	fbClntprnt("/* " + poParams['FB_BEHAVIOR'] + "  @" + poParams['FB_USERNAME'] + "'s " + poParams['FB_CONNECTION'] + " must have been started by now. */")
	#time.sleep(.4)

	return loFBClient

	


#......start tk................................................................

root = tkinter.Tk()

fbClntprnt(str(sys.argv))

client = [None, None, None, None]

#......Cnx initializers................................................................
"""
	method: ConnectNotifications
	description: used to call ToCreateCnx to create a connection/window/etc. for the Notifications Behavior Interface as
	described in NOTIFICATIONS_PARAMS (uphere at the top of this doc.)
"""
def ConnectNotifications():
	global client
	global ntfWindow

	if client[1] != None:
		client[1].grid_remove()

	if client[2] != None:
		client[2].grid_remove()

	if client[3] != None:
		client[3].grid_remove()

	if client[0] != None:
		fbClntprnt('Object already exists!')
		client[0].grid()
		return client[0]

	ntfWindow = tkinter.Toplevel()
	return ToCreateCnx(poWindow=ntfWindow, poParams=NOTIFICATIONS_PARAMS, psTitle=NOTIFICATIONS)

"""
	method: ConnectSpecificPost
	description: used to call ToCreateCnx to create a connection/window/etc. to the Specific Post as
	described in PostParams (uphere at the top of this doc.)
"""
def ConnectSpecificPost():
	global client
	global spstWindow
	if client[0] != None:
		client[0].grid_remove()

	if client[2] != None:
		client[2].grid_remove()

	if client[3] != None:
		client[3].grid_remove()

	if client[1] != None:
		fbClntprnt('Object already exists!')
		client[1].grid()
		return client[1]
	spstWindow = tkinter.Toplevel()
	return ToCreateCnx(poWindow=spstWindow, poParams=SPECIFIC_POST_PARAMS, psTitle=SPECIFIC_POST)

"""
	method: ConnectSpecificAlbum
	description: used to call ToCreateCnx to create a connection/window/etc. for the Specific Album as
	described in SPECIFIC_ALBUM_PARAMS (uphere at the top of this doc.)
"""
def ConnectSpecificAlbum():
	global client
	global albmWindow
	if client[0] != None:
		client[0].grid_remove()

	if client[1] != None:
		client[1].grid_remove()

	if client[3] != None:
		client[3].grid_remove()

	if client[2] != None:
		fbClntprnt('Object already exists!')
		client[2].grid()
		return client[2]
	albmWindow = tkinter.Toplevel()
	return ToCreateCnx(poWindow=albmWindow, poParams=SPECIFIC_ALBUM_PARAMS, psTitle=SPECIFIC_ALBUM)

"""
"""
def ConnectRaisePost():
	global client
	global raiserWindow
	if client[0] != None:
		client[0].grid_remove()

	if client[1] != None:
		client[1].grid_remove()

	if client[2] != None:
		client[2].grid_remove()

	if client[3] != None:
		fbClntprnt('Object already exists!')
		client[3].grid()
		return client[3]

	raiserWindow = tkinter.Toplevel()
	return ToCreateReader(poWindow=raiserWindow, poParams=SPECIFIC_RAISER_PARAMS, psTitle=SPECIFIC_RAISER)


DEBUG_MODE = False

#......initializers caller................................................................
"""
	Main cycle which starts the process of instantiating each FBClient from the begining, i mean
	if you told this App to open Notifications (-notif) and SpecificPost (-post) then here it will start each, one by one.
	
	Note.- To start a connection you've got to call this App like this: 
	
	To open one of this use:

	$python3 fbclnt.py -notif #For Notifications
	$python3 fbclnt.py -post #For An Specific Post Connection
	$python3 fbclnt.py -album #For a Connection to an Specific Album
	
	$python3 fbclnt.py -notif -post #For Notifications + Specific Post (Two Windows are created)

	Note 2.- When you close One of these Windows you can reopen it by going to the "Master Window" and
	click on "Re-Connect <Connection-Name>"

	Note 3.- To close it all just go there again (Master Window) and click "Close" button.

"""
for liInt in range(0, len(sys.argv)):
	if str(sys.argv[liInt]).lower() == "-debug": 
		DEBUG_MODE = True
		continue
	if str(sys.argv[liInt]).lower() == "-notifs":
		fbClntprnt("Opening Notifications Connection...")
		client[0] = ConnectNotifications()
	elif str(sys.argv[liInt]).lower() == "-posts":
		fbClntprnt("Opening an Specific Post Connection...")
		client[1] = ConnectSpecificPost()
	elif str(sys.argv[liInt]).lower() == "-albums":
		fbClntprnt("Opening Specific Album Connection...")
		client[2] = ConnectSpecificAlbum()
	elif str(sys.argv[liInt]).lower() == "-raiser":
		fbClntprnt("Opening Raise Post Procedure...")
		client[3] = ConnectRaisePost()

#......main window behavior initializer................................................................

for liInt in range(0,len(gbPARAMS)):
	if gbPARAMS[liInt]['FB_CONNECTION'] == "notifications":
		btnopnfn = tkinter.Button( root, text='Open ' + gbPARAMS[liInt]['FB_CONNECTION'], command=ConnectNotifications)
		btnopnfn.grid()
	elif gbPARAMS[liInt]['FB_CONNECTION'] == "posts":
		btnopnfn = tkinter.Button( root, text='Open ' + gbPARAMS[liInt]['FB_CONNECTION'], command=ConnectSpecificPost)
		btnopnfn.grid()
	elif gbPARAMS[liInt]['FB_CONNECTION'] == "albums":
		btnopnfn = tkinter.Button( root, text='Open ' + gbPARAMS[liInt]['FB_CONNECTION'], command=ConnectSpecificAlbum)
		btnopnfn.grid()
	elif gbPARAMS[liInt]['FB_CONNECTION'] == "raiser":
		btnopnfn = tkinter.Button( root, text='Raise ' + gbPARAMS[liInt]['FB_CONNECTION'], command=ConnectRaisePost)
		btnopnfn.grid()

root.title('Master Window')
console = tkinter.Button( root, text='Close', command=quitApp)
console.grid()

root.protocol("WM_DELETE_WINDOW", quitApp)

#......void main() {................................................................
gbRunning = True
#root.mainloop()
while gbRunning:
	root.update_idletasks()
	root.update()
#......}................................................................



