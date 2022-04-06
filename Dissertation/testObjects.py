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
import vizshape

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


#### ADD THE OBJECTS TO BE MANIPULATED


# Make background wall
#stout
WALL_SCALE1 = [.7, 1, .15]
TEXT_SCALE1 = [1.5,1.5,1.5]

#tall
# WALL_SCALE2 = [.5, 2, .15]

OBJECT_PAIRS = [[[.76, 1, .15],[.68, 1.25, .15]],[[.76, 1, .15],[.6, 1.5, .15]],[[.76, 1, .15],[.52, 1.75, .15]],\
				[[.68, 1.25, .15],[.76, 1, .15]],[[.68, 1.25, .15],[.6, 1.5, .15]],[[.68, 1.25, .15],[.52, 1.75, .15]],\
				[[.6, 1.5, .15],[.76, 1, .15]],[[.6, 1.5, .15],[.68, 1.25, .15]],[[.6, 1.5, .15],[.52, 1.75, .15]],\
				[[.52, 1.75, .15],[.76, 1, .15]],[[.52, 1.75, .15],[.68, 1.25, .15]],[[.52, 1.75, .15],[.68, 1.25, .15]]]
marbleG = viz.addTexture('Models/brittanybaxter/stone4gr.tga')
marbleY = viz.addTexture('Models/brittanybaxter/stone4ye.tga')
comModels = {}
comparisionObjects = []
adjustableObjects = []



for pp in OBJECT_PAIRS:
	PAIR = OBJECT_PAIRS[pp]
	comScale = PAIR[0]
	adjScale = PAIR[1]
	# Build the comparison pole in the pair
	TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*comScale[0]
	TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*comScale[1]
	TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*comScale[2]
	TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
	comparisonPole = vizshape.addBox(splitFaces=True)
	comparisonPole.setScale(comScale)
	comMatrix = vizmat.Transform()
	comMatrix.setScale( comScale )
	comparisonPole.texmat( comMatrix )
	marbleG.wrap(viz.WRAP_T, viz.REPEAT)
	marbleG.wrap(viz.WRAP_S, viz.REPEAT)
	comparisonPole.texture(marbleG)
	comparisionObjects[pp] = comparisonPole
	# comparisionObjects[pp] = viz.add(comparisonPole)

	# Build the adjustment pole in the pair
	TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
	TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
	TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
	TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
	adjustablePole = vizshape.addBox(splitFaces=True)
	adjustablePole.setScale(comScale)
	adjMatrix = vizmat.Transform()
	adjMatrix.setScale( adjScale )
	adjustablePole.texmat( adjMatrix )
	marbleY.wrap(viz.WRAP_T, viz.REPEAT)
	marbleY.wrap(viz.WRAP_S, viz.REPEAT)
	adjustablePole.texture(marbleY)
	adjustableObjects[pp] = adjustablePole
	# adjustableObjects[pp] = viz.add(adjustablePole)

end





