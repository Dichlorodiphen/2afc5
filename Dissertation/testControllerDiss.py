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
import vizshape
import steamvr
from os.path import exists
import audioControls
import emergencyWalls
import lights
import oculus
import winsound


ODYSSEY = 'Samsung Odyssey'
MONITOR = 'PC Monitor'
controlOptions = [MONITOR,ODYSSEY,MONITOR]
controlType = controlOptions[viz.choose('How would you like to explore? ', controlOptions)]

viz.clearcolor(0,0.4,1.0) # blue sky
#viz.add('Models/ground4.3DS') # ground plane


# Load models, ignore "Unknown Chunk" errors
models = {}
models['welcomeBox'] = viz.add('Models/brittanybaxter/redBox.osgb')
models['viewPlate'] = viz.add('Models/brittanybaxter/whiteBox.osgb')
models['boardwalk'] = viz.add('Models/brittanybaxter/carpetGround.osgb')
#models['sand'] = viz.add('Models/brittanybaxter/brownGround.osgb')
models['sand'] = viz.add('Models/brittanybaxter/Beach_sand.osgb')
#
#models['boardwalk'].visible(viz.OFF)
#models['sand'].visible(viz.OFF)
 
# Adjust models size
# 1m x 1m
models['welcomeBox'].setScale([.33,.15,.56])
models['viewPlate'].setScale([0.305,.155,0.305])
## 100 X 0 X 200
#models['boardwalk'].setScale([1,1,1])
## 100 X 0 X 200
#models['sand'].setScale([1,1,1])


####### THE ORIGIN OF THE ROOM WILL DEPEND ON THE PLACEMENT OF THE HEADSET
# IN THE REAL WORLD - MAKE SURE THAT THE PLATE IS BISECTED BY THE SAND AND WOOD
# IF THE HEADSET IS INITIALIZED ON THE PLATFORM THEN 0 GROUND HEIGHT SHOULD BE THE PLATFORM
# REMEMBER THAT THE POLE POSITIONS ARE SET FROM (0,0,0) SO THE HEADSET SHOULD BE INITIALIZED FROM OVERTOP OF THE PLATE


# set the position of the environment objects
# new plate size
#	THE ROOM SET UP SHOULD HAVE THE PLATE CENTERED ON THE Z-AXIS BUT THE FRONT EDGE RELATIVELY SHIFTED FROM THE (0,0)
# .33,.15,.56
models['welcomeBox'].setPosition(0, 0, -.255)
# 0.305,.155,0.305
models['viewPlate'].setPosition(0, 0, -.155)
## 100 X 0 X 200
#models['boardwalk'].setPosition(100, 0.148, 0)
## 100 X 0 X 200
#models['sand'].setPosition(-100, 0.148, 0)

### ADD THE POLES TO BE MANIPULATED
adjustablePole = viz.addChild('Models/yellowPole.3ds', pos=[3,0,3])
comparisonPole = viz.addChild('Models/brittanybaxter/greenPole.3ds', pos=[-3,0,3])
adjustablePole.setPosition(-1.5,0,1)
comparisonPole.setPosition(-.5,0,1)


# Choose display mode:

# Use moniter and keyboard
# Controls:
# q - Strafe L		w - Forward		e - Strafe R
# a - Turn L		s - Back		d - Turn R
#
# y - Face Up		r - Fly Up
# h - Face Down		f - Fly Down
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

cur_pos = viz.get(viz.HEAD_POS)
decisionMade = False

#These don't work
##controller = __builtin__.SteamVRController(1)
##controller = steamvr.getControllerList(0)
poleDistA = math.sqrt(2)
incrementOfAdjustment = 0.1
xPosA = 0
zPosA = 10
#adjustablePolePosition = [1,0,1]
xSignA = 1
zSignA = 1 
poleAngleA = 45
decisionMade = False
THRESHOLD_THETA = 15


print 'now I test the controller buttons'
def testButtonPress():
	# Add controllers
	for controller in steamvr.getControllerList():
		# Create model for controller
		controller = controller

	print 'controller connected'
	print 'controller connected'
	print 'controller connected'
	print 'getPosition', controller.getPosition(flag=0)
	print 'trackpad', controller.getTrackpad()
	print 'steamvr.BUTTON_TRigger', steamvr.BUTTON_TRIGGER #2
	print 'steamvr.BUTTON_TRACKPAD', steamvr.BUTTON_TRACKPAD #3
	print 'steamvr.BUTTON_TRACKPAD_TOUCH', steamvr.BUTTON_TRACKPAD_TOUCH #4
	print 'controller.isButtonDown(3)', controller.isButtonDown(3)
	print 'controller.isButtonDown(4)', controller.isButtonDown(4)

vizact.ontimer(1/90, testButtonPress)

# button_down to trigger object movement
# button_up to end movement

# def moveComparison():
#     global poleDistA, xPosA, zPosA, poleAngleA, decisionMade,THRESHOLD_THETA, trial_stage
        
#     # Add controllers
#     for controller in steamvr.getControllerList():
#       # Create model for controller
#       controller = controller

# #      print 'controller connected'
# #      print 'joystickX', controller.getThumbstick()
# steamvr.BUTTON_TRACKPAD_TOUCH
# # try
# # viz.controller.getState()

#   # Current position and roation of the participant
#     cur_pos = viz.get(viz.HEAD_POS)
#     cur_rot = viz.get(viz.HEAD_ORI)
    

#     # if trial_stage == 'experimental_setup':
# 	# if universals.facing(cur_pos, adjustablePole.getPosition(), cur_rot[0], THRESHOLD_THETA):
# # 
# 	# print 'button', e.button, 'is down'
# 	print 'trackpad', controller.getTrackpad()
# 	xT,yT = controller.getTrackpad()
# 	print 'trackpad y', yT
# 	print ' '
# 	trigger = controller.getTrigger()
# 	print 'trigger', trigger
# 	# print decisionMade
# 	if trigger >.5:
# 		decisionMade = True
# 		print 'decision', decisionMade
# 		adjustablePole.clearActions()

# 	print 'decision', decisionMade
# 	print 'pole distance', poleDistA

# 	if e.button == 4:
# 		if yT > 0.5:
# 		#incrementOfAdjustment=.05m
# 			poleDistA = poleDistA + incrementOfAdjustment*2
# 		elif yT < -0.5:
# 			poleDistA = poleDistA - incrementOfAdjustment*2

# 		#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
# 		poleAngleA = condition[trial_num-1, 4]
# 		poleAngleARad = math.radians(poleAngleA)
# 		#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
# 		adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
# 		print 'adjustableSpot', adjustableSpot
# 		xSignA = poleSpots[adjustableSpot-1][0]  #-1 to correct for array position
# 		zSignA = poleSpots[adjustableSpot-1][1]

# 		xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
# 		zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
# 		adjustablePolePosition = [xPosA,0,zPosA]
# 		print 'adjustablePolePosition', adjustablePolePosition
# 		#???????????????? play with speed and increment of adjustment
# 		#Use a moveTo action to move a node to the point [0,0,25] at X meters per second 
# 		flyToPoint = vizact.moveTo(adjustablePolePosition, speed=.25, interpolate=vizact.easeInOut)
# 		adjustablePole.addAction(flyToPoint)

# 	if e.button == 3:
# 		if yT > 0.5:
# 		#incrementOfAdjustment=.05m
# 			poleDistA = poleDistA + incrementOfAdjustment*10
# 		elif yT < -0.5:
# 			poleDistA = poleDistA - incrementOfAdjustment*10

# 		#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
# 		poleAngleA = condition[trial_num-1, 4]
# 		poleAngleARad = math.radians(poleAngleA)
# 		#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
# 		adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
# 		print 'adjustableSpot', adjustableSpot
# 		xSignA = poleSpots[adjustableSpot-1][0]  #-1 to correct for array position
# 		zSignA = poleSpots[adjustableSpot-1][1]

# 		xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
# 		zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
# 		adjustablePolePosition = [xPosA,0,zPosA]
# 		print 'adjustablePolePosition', adjustablePolePosition
# 		#???????????????? play with speed and increment of adjustment
# 		#Use a moveTo action to move a node to the point [0,0,25] at X meters per second 
# 		flyToPoint = vizact.moveTo(adjustablePolePosition, speed=1.25, interpolate=vizact.easeInOut)
# 		adjustablePole.addAction(flyToPoint)
#     adjustablePole.clearActionList()   

# #viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)
# # check the controller at this time
# vizact.ontimer(1/60, moveComparison)





# ######TRY THIS TO IMPLIMENT INTO EPERIMENTAL LOOP
# #if viz.SENSOR_DOWN_EVENT:
# ## this has just been put seperately and where they look is part of the function
# #    onSensorDown()
# #print viz.SENSOR_DOWN_EVENT
# #
# #if decisionMade:
# #    print 'decision triggered'
# #    decisionMade = False


# trial_stage = 'welcome'
# DISC_TRIGGER_RADIUS = .5
# time = 0
# def masterLoop(num):
#      global poleDistA, xPosA, zPosA, poleAngleA, decisionMade,incrementOfAdjustment,trial_stage, \
#      DISC_TRIGGER_RADIUS, time

#      # Time elapsed since the last run of masterLoop and then added to the global time
#      frame_elapsed = viz.getFrameElapsed()
#      time += frame_elapsed
    
#  # Current position and roation of the participant
#      cur_pos = viz.get(viz.HEAD_POS)
#      cur_rot = viz.get(viz.HEAD_ORI)
#      # Add controllers
#      for controller in steamvr.getControllerList():
#       # Create model for controller
#       controller = controller



#      if trial_stage == 'welcome':
# #         viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)

#          # add in instruction to walk to disc
#          if (universals.inRadius(cur_pos, models['viewPlate'].getPosition(), DISC_TRIGGER_RADIUS)):
#              models['welcomeBox'].visible(viz.OFF)
#              print 'standing on plate'
#              trial_stage = 'experimental_setup'
#              print 'pole should move'
# #             trial_stage = 'other_setup'
# #             print 'pole should N move'
             
#      if trial_stage == 'other_setup':
#          models['boardwalk'].visible(viz.ON)
#          models['sand'].visible(viz.ON)
#          adjustablePole.visible(viz.ON)
#          comparisonPole.visible(viz.ON)
#      if trial_stage == 'experimental_setup':

#          models['boardwalk'].visible(viz.ON)
#          models['sand'].visible(viz.ON)
#          adjustablePole.visible(viz.ON)
#          comparisonPole.visible(viz.ON)

#      if trial_stage == 'experimental_setup':
# #        if universals.facing(cur_pos, adjustablePole.getPosition(), cur_rot[0], THRESHOLD_THETA):
#         print 'trackpad', controller.getTrackpad()
#         xT,yT = controller.getTrackpad()
#         print 'trackpad y', yT
#         print ' '
#         trigger = controller.getTrigger()
#         print 'trigger', trigger
#         print decisionMade
#         if trigger >.5:
#             decisionMade = True
#             print decisionMade
#         print ' '
#         print 'pole distance', poleDistA
#         if e.button == 3:
#             if yT > 0.2:
#                 poleDistA = poleDistA + incrementOfAdjustment
#             elif yT < -0.2:
#                 poleDistA = poleDistA - incrementOfAdjustment
           
#         #models['triggerPole'].setPosition(0,0,10)red pole
#             xPosA = math.sin(poleAngleA)*poleDistA*xSignA
#             zPosA = math.cos(poleAngleA)*poleDistA*zSignA
#             adjustablePolePosition = [xPosA,0,zPosA]
#             print 'adjustablePolePosition', adjustablePolePosition
#         #Use a moveTo action to move a node to the point [0,0,25] at 2 meters per second 
#             flyToPoint = vizact.moveTo(adjustablePolePosition, speed=2, interpolate=vizact.easeInOut)
#             adjustablePole.addAction(flyToPoint)
#     	adjustablePole.clearActionList() 
# #         if steamvr.getControllerList() == []:
# #            for controller in steamvr.getControllerList():
# #  # Create model for controller
# #                controller = controller 
# #                print 'it works'
             
# #         if decisionMade == True:
# #             print 'yup'
#  #        viz.callback(viz.SENSOR_DOWN_EVENT, onSensorDown)
# viz.callback(viz.TIMER_EVENT,masterLoop)
# viz.starttimer(0,1/90,viz.FOREVER)





























