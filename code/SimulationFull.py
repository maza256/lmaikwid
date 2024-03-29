#!/usr/bin/env python
# coding: Latin-1

############################################################
# This is the start-up script for the Formula Pi Race Code #
#                                                          #
# It is responsible for managing the threads which control #
# the MonsterBorg during a race                            #
############################################################

# Load all the library functions we want
import time
import os
import sys
import threading
import cv2
import numpy
import random
import inspect
import Globals
import urllib2
print 'Libraries loaded'

simulationIP = '127.0.0.1'			# Address of the machine running the simulation
simulationPort = 10000				# Port number used by the simulation
frameLimiter = True


imageUrl = r'http://%s:%d/view.png' % (simulationIP, simulationPort)
setDriveUrl = r'http://%s:%d/?m1=%%.2f&m2=%%.2f&l1=%%d' % (simulationIP, simulationPort)

# Change the current directory to where this script is

# FINHACK: sort out error.
# scriptDir = os.path.dirname(sys.argv[0])
scriptDir = os.path.dirname(os.path.abspath(__file__))

print 'Running script in directory "%s"' % (scriptDir)
os.chdir(scriptDir)

# Functions used by the processing to control the MonsterBorg
def MonsterLed(r, g, b):
	global simLed
	print '>>> LED: %.1f %.1f %.1f' % (r, g, b)
	simLed = (r, g, b)
	SendToSimulation()

def MonsterMotors(driveLeft, driveRight):
	global simLeft
	global simRight
	simLeft = driveLeft * Settings.simulationDrivePower
	simRight = driveRight * Settings.simulationDrivePower
	#print '>>> MOTORS: %.3f | %.3f (x%.2f)' % (driveLeft, driveRight, Settings.simulationDrivePower)
	SendToSimulation()

# Function and data used to maintain the simulator state
global simLed
global simLeft
global simRight
simLed = (0, 0, 0)
simLeft = 0.0
simRight = 0.0

def SendToSimulation():
	global simLed
	global simLeft
	global simRight
	if (simLed[0] > 0.0) or (simLed[1] > 0.0) or (simLed[2] > 0.0):
		url = setDriveUrl % (simLeft, simRight, 1)
	else:
		url = setDriveUrl % (simLeft, simRight, 0)
	try:
		request = urllib2.urlopen(url, timeout=1)
	except IOError:
		print 'Failed to send motor values to simulation!'
	except urllib2.URLError:
		print 'Failed to send motor values to simulation!'

# Add the cross-module functions to the global list
Globals.MonsterLed = MonsterLed
Globals.MonsterMotors = MonsterMotors

# Setup synchronisation locks
Globals.frameLock = threading.Lock()

# Load the standard processing code after the built-ins
import ImageProcessor
from RaceCodeFunctions import *
print 'Image processor and Race Code Functions loaded'

# Function for displaying the current settings
def ShowSettings():
	print '=== NEW SETTINGS ==='
	print

	print '[Image setup]'
	print 'Camera %d x %d at %d fps' % (Settings.imageWidth, Settings.imageHeight, Settings.frameRate)
	print 'X cropped from %d to %d' % (Settings.cropX1, Settings.cropX2)
	print 'Y cropped from %d to %d' % (Settings.cropY1, Settings.cropY2)
	print 'Image processing threads: %d' % (Settings.processingThreads)
	print

	print '[Startup]'
	print 'Initial mode: %d' % (Settings.startupMode)
	print

	print '[Y scan lines]'
	for Y in Settings.croppedYScan:
		print '%d (%d)' % (Y + Settings.cropY1, Y)
	print

	print '[Colour identification]'
	print 'Black limit: %d %d %d' % (Settings.blackMaxR, Settings.blackMaxG, Settings.blackMaxB)
	print 'Green gain: %.2f' % (Settings.greenGain)
	print 'Blue gain: %.2f' % (Settings.blueGain)
	print 'Target level for auto-gain: %.0f' % (Settings.targetLevel)
	print 'Erosion factor for colour channels: %.0f' % (Settings.erodeChannels)
	print 'Final colour minimums: %d %d %d' % (Settings.redMin, Settings.greenMin, Settings.blueMin)
	print

	print '[Line correction]'
	print 'Colour edge gap: %.0f pixels' % (Settings.maxSepX)
	print 'Lane gap: %.0f pixels' % (Settings.trackSepX)
	print 'Offset Y calculation target %d: (%d)' % (Settings.offsetTargetY, Settings.croppedTargetY)
	print 'Corrective gain for derivative: %.3f' % (Settings.gainCorrection)
	print

	print '[Start marker detection]'
	print 'Levels: Min Red = %d, Max Green = %d, Max Blue = %d' % (Settings.startMinR, Settings.startMaxG, Settings.startMaxB)
	print 'Start minimum match ratio: %.1f %%' % (Settings.startRatioMin * 100.0)
	print 'Start crossed delay %.2f s (%d frames)' % (Settings.startCrossedSeconds, Settings.startCrossedFrames)
	print 'Start re-detection delay: %.1f s' % (Settings.startRedetectionSeconds)
	print 'Start detection zone X limits: %d to %d' % (Settings.startX1, Settings.startX2)
	print 'Start detection zone Y position: %d' % (Settings.startY)

	print '[PID values]'
	print '    P0: %f   I0:%f   D0: %f' % (Settings.Kp0, Settings.Ki0, Settings.Kd0)
	print '    P1: %f   I1:%f   D1: %f' % (Settings.Kp1, Settings.Ki1, Settings.Kd1)
	print '    P2: %f   I2:%f   D2: %f' % (Settings.Kp2, Settings.Ki2, Settings.Kd2)
	print

	print '[FIR filter]'
	print '    Taps: %d' % (Settings.firTaps)
	print

	print '[Drive settings]'
	steeringMin = Settings.steeringOffset - Settings.steeringGain
	steeringMax = Settings.steeringOffset + Settings.steeringGain
	print 'Maximum output: %.1f %%' % (Settings.maxPower * 100.0)
	print 'Steering %+.1f %% to %+.1f %% (central %+.1f %%)' % (steeringMin * 100.0, steeringMax * 100.0, Settings.steeringOffset * 100.0)
	print 'Missing frames before stopping: %d' % (Settings.maxBadFrames)
	print

	print '[Override settings]'
	print 'Stuck detection threshold: %.2f' % (Settings.stuckIdenticalThreshold)
	print 'Stuck detection time: %.2f s (%d frames)' % (Settings.stuckIdenticalSeconds, Settings.stuckIdenticalFrames)
	print 'Stuck reversing time: %.2f s (%d frames)' % (Settings.stuckOverrideSeconds, Settings.stuckOverrideFrames)
	print 'Stuck hunting time: %.2f s (%d frames)' % (Settings.stuckHuntSeconds, Settings.stuckHuntFrames)
	print 'Stuck colour detection at %d x %d' % (Settings.stuckDetectColourX, Settings.stuckDetectColourY)
	print 'Wrong way detection threshold: %d' % (Settings.wrongWayThreshold)
	print 'Wrong way spin time: %.2f s (%d frames)' % (Settings.wrongWaySpinSeconds, Settings.wrongWaySpinFrames)
	print 'Robot in front detection threshold: %d' % (Settings.overtakeThreshold)
	print 'Overtaking lane shift: %.2f' % (Settings.overtakeLaneOffset)
	print 'Overtaking time: %.2f s (%d frames)' % (Settings.overtakeDurationSeconds, Settings.overtakeDurationFrames)
	print

	print '===================='
	print

# Function to load settings overrides
def SettingsOverrides():
	Settings.flippedImage = True
	Settings.horizontalFlip = False
	Settings.monsterSpeed = Settings.simulationMonsterSpeed

# Function for auto-loading the settings file when it has changed
global modificationStamp
modificationStamp = 0
def AutoReloadSettings():
	global modificationStamp
	newModificationStamp = os.path.getmtime('Settings.py')
	if newModificationStamp != modificationStamp:
		reload(Settings)
		SettingsOverrides()
		ImageProcessor.Settings = Settings
		if Globals.controller:
			Globals.controller.Reset()
		ShowSettings()
		Globals.startLights = ImageProcessor.READY_OFF
		modificationStamp = newModificationStamp
		if frameLimiter:
			Globals.frameWaitMs = int(1000 / Settings.frameRate)
		else:
			Globals.frameWaitMs = 1

# Load the initial settings (does a reload)
import Settings
AutoReloadSettings()
Globals.imageMode = Settings.startupMode
Globals.lastImageMode = ImageProcessor.READY_TO_RACE

# Image processing debugging settings
ImageProcessor.filePattern = './test-%05d-%s.jpg'
ImageProcessor.writeRawImages = False 
ImageProcessor.writeImages = False
ImageProcessor.debugImages = False
ImageProcessor.showProcessing = False
ImageProcessor.showFps = True
ImageProcessor.showUnknownPoints = False
ImageProcessor.predatorView = False
ImageProcessor.scaleFinalImage = 1.0
ImageProcessor.scaleDebugImage = 1.0
ImageProcessor.dPlotY = -10

# Thread for running Race.py
raceGlobals = globals().copy()
raceLocals = locals().copy()
class RaceLoop(threading.Thread):
	def __init__(self):
		super(RaceLoop, self).__init__()
		self.start()

	def run(self):
		# This method runs in a separate thread, but shares global and local values / functions
		execfile('Race.py', raceGlobals.copy(), raceLocals.copy())

# Simulation image capture thread
class SimulationImageCapture(threading.Thread):
	def __init__(self):
		super(SimulationImageCapture, self).__init__()
		self.timeLast = time.time()
		self.holdMs = 0
		self.frameQueue = []
		self.lagFrames = Settings.simulationLagFrames
		self.start()

	# Stream delegation loop
	def run(self):
		while Globals.running:
			# Grab the oldest unused processor thread
			with Globals.frameLock:
				if Globals.processorPool:
					processor = Globals.processorPool.pop()
				else:
					processor = None
			if processor:
				# Grab the next frame from the simulation and send it to the processor
				try:
					request = urllib2.urlopen(imageUrl, timeout=5)
					frame = numpy.fromstring(request.read(), dtype='uint8')
					frame = cv2.imdecode(frame, cv2.CV_LOAD_IMAGE_COLOR)
					okay = True
				except IOError:
					okay = False
				except urllib2.URLError:
					okay = False
				# FINHACK: below, '==' changed to 'is'
				if frame is None:
					# Something went wrong decoding the image
					print '!!! BAD IMAGE !!!'
					with Globals.frameLock:
						Globals.processorPool.insert(0, processor)
					continue
				if okay:
					# Resize / crop the image if the resolution does not match
					if (frame.shape[1] != Settings.imageWidth) or (frame.shape[0] != Settings.imageHeight):
						ratioIn = frame.shape[1] / float(frame.shape[0])
						ratioOut = Settings.imageWidth / float(Settings.imageHeight)
						if abs(ratioIn - ratioOut) < 0.01:
							# Straight resize
							pass
						elif ratioIn > ratioOut:
							# Crop width
							width = frame.shape[1]
							cropWidth = ratioOut / ratioIn
							cropOffset = (1.0 - cropWidth) / 2.0
							cropWidth = int(cropWidth * width)
							cropOffset = int(cropOffset * width)
							frame = frame[:, cropOffset : cropOffset + cropWidth, :]
						else:
							# Crop height
							height = frame.shape[0]
							cropHeight = ratioIn / ratioOut
							cropOffset = (1.0 - cropHeight) / 2.0
							cropHeight = int(cropHeight * height)
							cropOffset = int(cropOffset * height)
							frame = frame[cropOffset : cropOffset + cropHeight, :, :]
						frame = cv2.resize(frame, (Settings.imageWidth, Settings.imageHeight), interpolation = cv2.INTER_CUBIC)
					# Generate a delay buffer to simulate camera lag
					if self.lagFrames != Settings.simulationLagFrames:
						self.lagFrames = Settings.simulationLagFrames
						self.frameQueue = []
					self.frameQueue.insert(0, frame)
					if len(self.frameQueue) > self.lagFrames:
						frame = self.frameQueue.pop()
					else:
						frame = numpy.zeros_like(frame)
					processor.nextFrame = frame
					processor.event.set()
					# Work out the time delay required for the frame limiter
					self.timeNow = time.time()
					lagMs = (self.timeNow - self.timeLast) * 1000
					self.timeLast = self.timeNow
					self.holdMs = int(Globals.frameWaitMs - lagMs) + self.holdMs
					if self.holdMs > 0:
						time.sleep(self.holdMs * 0.001)
				else:
					ImageProcessor.LogData(ImageProcessor.LOG_CRITICAL, 'Simulation stream lost...')
					Globals.running = False
					break
			else:
				# When the pool is starved we wait a while to allow a processor to finish
				time.sleep(0.01)
		ImageProcessor.LogData(ImageProcessor.LOG_CRITICAL, 'Streaming terminated.')

# Dummy startup
try:
	request = urllib2.urlopen(imageUrl, timeout=10)
except IOError:
	print 'Failed to open the simulation stream'
	sys.exit(75)

print 'Setup stream processor threads'
Globals.processorPool = [ImageProcessor.StreamProcessor(i+1) for i in range(Settings.processingThreads)]
allProcessors = Globals.processorPool[:]

print 'Setup control loop'
Globals.controller = ImageProcessor.ControlLoop()

print 'Start Race.py'
raceThread = RaceLoop()

print 'Start simulation capture thread'
captureThread = SimulationImageCapture()

try:
	print 'Press CTRL+C to quit'
	if ImageProcessor.showProcessing:
		cv2.namedWindow('Processed', cv2.WINDOW_AUTOSIZE)
	if ImageProcessor.predatorView:
		cv2.namedWindow('Predator', cv2.WINDOW_AUTOSIZE)
	# Loop indefinitely
	while Globals.running:
		# See if there is a frame to show
		if Globals.displayFrame != None:
			if ImageProcessor.scaleFinalImage != 1.0:
				size = (int(Globals.displayFrame.shape[1] * ImageProcessor.scaleFinalImage), 
						int(Globals.displayFrame.shape[0] * ImageProcessor.scaleFinalImage))
				processed = cv2.resize(Globals.displayFrame, size, interpolation = cv2.INTER_CUBIC)
			else:
				processed = Globals.displayFrame
			cv2.imshow('Processed', processed)
		if Globals.displayPredator != None:
			if ImageProcessor.scaleFinalImage != 1.0:
				size = (int(Globals.displayPredator.shape[1] * ImageProcessor.scaleFinalImage), 
						int(Globals.displayPredator.shape[0] * ImageProcessor.scaleFinalImage))
				predator = cv2.resize(Globals.displayPredator, size, interpolation = cv2.INTER_CUBIC)
			else:
				predator = Globals.displayPredator
			cv2.imshow('Predator', predator)
		# Wait either way
		if (Globals.displayFrame != None) or (Globals.displayPredator != None):
			cv2.waitKey(100)
		else:
			# Wait for the interval period
			time.sleep(0.1)
		# Check if on-the-fly settings have been changed
		AutoReloadSettings()
	# Disable all drives
	MonsterMotors(0.0, 0.0)
except KeyboardInterrupt:
	# CTRL+C exit, disable all drives
	print '\nUser shutdown'
	MonsterMotors(0.0, 0.0)
except:
	# Unexpected error, shut down!
	e = sys.exc_info()
	print
	print e
	print '\nUnexpected error, shutting down!'
	MonsterMotors(0.0, 0.0)
# Tell each thread to stop, and wait for them to end
Globals.running = False
while allProcessors:
	with Globals.frameLock:
		processor = allProcessors.pop()
	processor.terminated = True
	processor.event.set()
	processor.join()
Globals.controller.terminated = True
raceThread.terminated = True
Globals.controller.join()
captureThread.join()
raceThread.join()
MonsterMotors(0.0, 0.0)
MonsterLed(Globals.colour[0] * 0.3, Globals.colour[1] * 0.3, Globals.colour[2] * 0.3)
print 'Program terminated.'
