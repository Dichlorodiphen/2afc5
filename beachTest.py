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
viz.add('Models/ground4.3DS') # ground plane
frontOfPlate = viz.addTexQuad()
frontOfPlate.setScale([.305,3,1])
backOfPlate = viz.addTexQuad()
backOfPlate.setScale([.305,1,1])
stepOff = viz.addTexQuad()
stepOff.setScale([.5,.15,1])
# Make sand surface
WALL_SCALE = [100, 100, 1]
beach = viz.addTexQuad()
beach.setPosition( [0, 0.148,0] )
beach.setEuler([0,90,0])
beach.setScale( WALL_SCALE )
# Apply nice repeating sand texture
C = 5
TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C, WALL_SCALE[2]]
matrix = vizmat.Transform()
matrix.setScale( TEXT_SCALE)
beach.texmat( matrix )
sand = viz.addTexture('Models/brittanybaxter/Sand2.jpg')
sand.wrap(viz.WRAP_T, viz.MIRROR)
sand.wrap(viz.WRAP_S, viz.REPEAT)
beach.texture(sand)

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


