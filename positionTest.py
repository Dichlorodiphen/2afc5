#####################################################################################
# Imports
#####################################################################################
import csv
import math
import numpy
import random
import sys
import time
import universals
import viz
import vizact
import viztracker
import vizconfig
import steamvr
from os.path import exists
import audioControls
import emergencyWalls
import lights
import oculus
import winsound
if controlType == MONITOR:
	headTrack = viztracker.Keyboard6DOF()
	# link the keyboard control to the camera
	link = viz.link(headTrack, viz.MainView)
	headTrack.eyeheight(1.6)
	link.setEnabled(True)
# Use Odyssey
elif controlType == ODYSSEY:	
	# add Odyssey tracker
	ODTracker = steamvr.HMD().getSensor()
	# link the ISTracker to the camera
	link = viz.link(ODTracker, viz.MainView)
	# Load DirectInput plug-in
# start rendering
viz.go()

# Add controllers
for controller in steamvr.getControllerList():
  # Create model for controller
  controller = controller
  print 'controller connected'
  print 'controller connected'
  print 'controller connected'

viz.clearcolor(0,0.4,1.0) # blue sky
models = {}
models['welcomeBox'] = viz.add('Models/brittanybaxter/redBox.osgb')
models['viewPlate'] = viz.add('Models/brittanybaxter/whiteBox.osgb')

models['practiceDisc'] = viz.add('Models/brittanybaxter/redPole.3ds')
models['boardwalk'] = viz.add('Models/brittanybaxter/carpetGround.osgb')
models['sand'] = viz.add('Models/brittanybaxter/brownGround.osgb')

models['viewPlate'].setScale([0.305,.155,0.305])
# 100 X 0 X 200
models['boardwalk'].setScale([1,1,1])
# 100 X 0 X 200
models['sand'].setScale([1,1,1])
# 0.305,.155,0.305
models['viewPlate'].setPosition(0, 0, -.155)
#firmSandOrder = viz.input('Is the sand to the right: 1 for yes, 0 for no','')
# 100 X 0 X 200
models['boardwalk'].setPosition(0, 0.148, 0)
# 100 X 0 X 200
models['sand'].setPosition(0, 0.148, 0)

pole1 = viz.addChild('Models/brittanybaxter/greenPole.3ds', pos=[3,0,3])
pole2 = viz.addChild('Models/brittanybaxter/greenPole.3ds', pos=[-3,0,3])
pole3 = viz.addChild('Models/brittanybaxter/greenPole.3ds', pos=[-3,0,-3])
pole4 = viz.addChild('Models/brittanybaxter/greenPole.3ds', pos=[3,0,-3])
pole1.setScale([1,.5,1])
pole2.setScale([1,1.5,1])
pole3.setScale([1,3,1])
pole4.setScale([1,4.5,1])

poles = [pole1,pole2,pole3,pole4]

poleSpots = [[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]]

condition = [1,5,10,16]
#poleAngle = [45,45,135,135]

for p in range(4)

	#	   [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   
	poleDistA = condition[p] # 5, 7, 9, 11 m
	#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
	poleAngleA = 45
	#poleAngleA = poleAngle[p]

	poleAngleARad = math.radians(poleAngleA)

	xSignA = poleSpots[p][0]  #-1 to correct for array position
	zSignA = poleSpots[p][1]

	xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
	zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
	pole = poles[p]
	pole.setPosition(xPosA, 0, zPosA)








