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
import vizmat
import vizact
import viztracker
import vizconfig
import steamvr
from os.path import exists
import audioControls
#import emergencyWallsSandbox
import lights
import oculus
import winsound
import vizdlg
import vizinfo
#####################################################################################
#####################################################################################
# Control Options
# Sets the controls / displays
#####################################################################################
#####################################################################################
ODYSSEY = 'Samsung Odyssey'
MONITOR = 'PC Monitor'
controlOptions = [ODYSSEY,MONITOR]
controlType = controlOptions[viz.choose('How would you like to explore? ', controlOptions)]
# Choose display mode:
if controlType == ODYSSEY:	
	# add Odyssey tracker
	ODTracker = steamvr.HMD().getSensor()
	# link the ISTracker to the camera
	link = viz.link(ODTracker, viz.MainView)
	# Add controllers

# Use moniter and keyboard
# Controls:
# q - Strafe L		w - Forward		e - Strafe R
# a - Turn L		s - Back		d - Turn R
#
# y - Face Up		r - Fly Up
# h - Face Down		f - Fly Down
elif controlType == MONITOR:
	headTrack = viztracker.Keyboard6DOF()
	# link the keyboard control to the camera
	link = viz.link(headTrack, viz.MainView)
	headTrack.eyeheight(1.6)
	link.setEnabled(True)
# start rendering
viz.go()

for controller in steamvr.getControllerList():
  # Create model for controller
  controller = controller
  print('controller connected')
  print('controller connected')
  print('controller connected')

#####################################################################################
# Experiment Input and Output files # Dialog box asking for subject name
#####################################################################################
subject = viz.input('Please enter the subject number:','')
# 1100 - 1199 DissA; 1200 - 1299 DissB;1300 - 1399 DissC;  TEST 1500s
if subject < 1000 or subject > 1600:
	subject = viz.input('Please enter the subject number (1000-1599):','')
# dissStudy = 'DissTest' # subject = 1501
# studyOptions =  ['Test','A','B','C']
# dissStudy = studyOptions[viz.choose('Please enter the study(Test, A, B, or C):', studyOptions)]
if subject > 1200 and subject < 1299:
	dissStudy = 'DissA'
elif subject > 1300 and subject < 1399:
	dissStudy = 'DissB'
elif subject > 1400 and subject < 1499:
	dissStudy = 'DissC'
else:
	dissStudy = 'DissTest'
# dissStudy = 'Diss'+ dissStudy
print(dissStudy)
subjectFile = dissStudy + str(subject)
print(subjectFile)


skipControllerInstructions = False

# Starts trial count at 1
trial_num = 1


#check if output file for a subject already exists
#if os.path.isfile(output_dir + '/'+  str(subject_name)+'_'+'summary.txt') == True:
#    print 'output file for participant #: ', subject_name, ' already exists' 
#    answer = viz.ask('output file for this participant number already exists. Do you want to continue?')
#    if answer:
#        print 'Continue. Data will be appended to existing output file'
#        viz.message('Continue. Data will be appended to existing output file')
#    else:
#        viz.message('Session stopped')
#        viz.quit()
#elif os.path.isfile(output_dir + '/'+ str(subject_name)+'_'+'summary.txt') == False:
#    print 'new output file for participant "', subject_name, '" will be created'


#
#INSTRUCTIONS = 'run_instructions'
#NO_INSTRUCTIONS = 'skip_instructions'
# WELCOME, CONTROLLER_MOVE, CONTROLLER_INSTRUCTIONS, WALK_INSTRUCTIONS, WALK, CONTROLLER_TRIGGER_INSTRUCTIONS, CONTROLLER_TRIGGER, EXPERIMENT_INSTRUCTIONS, EXPERIMENT
# Initializes trial_stage, which is the current step of a given trial
#WELCOME =  'welcome_environment'
#PRACTICE_1 = 'practice_controller_setup1'
#EXPLORATION = 'practice_disc_height'
#PRACTICE_2 = 'start_of_four_practice'
#EXPERIMENT = 'done_practice_start_experiment'
#experimentStart = [WELCOME, PRACTICE_1, EXPLORATION, PRACTICE_2, EXPERIMENT]
#controlBegin = experimentStart[viz.choose('Where to start', experimentStart)]

experimentStart = ['welcome_environment', 'practice_controller_setup1', 'practice_disc_height', 'start_of_four_practice', 'done_practice_start_experiment']
controlBegin = experimentStart[viz.choose('Where to start', ['WELCOME', 'PRACTICE_1', 'EXPLORATION', 'PRACTICE_2', 'EXPERIMENT'])]
trial_stage = controlBegin
print('Begin at', trial_stage)


initializeInstructions = ['run_instructions', 'skip_instructions']
if trial_stage == 'practice_controller_setup1' or trial_stage == 'practice_disc_height':
	prompt = initializeInstructions[viz.choose('Instructions?', ['INSTRUCTIONS', 'NO_INSTRUCTIONS'])]
	if prompt == 'skip_instructions':
		# passes to controller_instructions
		skipControllerInstructions = True
	elif prompt == 'run_instructions':
		skipControllerInstructions = False
print('trial_stage', trial_stage)

if trial_stage == 'start_of_four_practice':
	subFour = ['start_of_four_practice', 'decision_instructions','practice_controller_setup2']
	subSelection = subFour[viz.choose('practice instructions, decison instructions, or practice trial 1?', ['INTRO TO FOUR PRACTICE', 'DIST/EASE/ENERGY', 'START AT practice_num 1'])]
	trial_stage = subSelection
	print('trial_stage', trial_stage)
	
elif trial_stage == 'start_at_experiment':
	subExperiment = ['done_practice_start_experiment', 'experiment_instructions', 'start_at_experiment']
	subSelection = subExperiment[viz.choose('Starting experiment, specific instructions, or trial 1?', ['DONE PRACTICE', 'DIST/EASE/ENERGY', 'TRIAL 1'])]
	trial_stage = subSelection
	print('trial_stage', trial_stage)
	tNum = viz.input('Please enter the trial number (1-128):','')
	trial_num = float(tNum)
	print('trial_num', trial_num)

	
print('trial_stage', trial_stage)
print('skipControllerInstructions', skipControllerInstructions)

########################################################################################################################
#     Set working directory for writing data_rot     #      Set working directory for writing data_rot     #
########################################################################################################################
# write into output folder regardless of experiment
working_dir = '/'.join(['Data','brittanybaxter','Dissertation', 'output'])
universals.make_dir_path(working_dir)
#ABC_dir = '/'.join(['Data','brittanybaxter','Dissertation'])
ABC_dir = '.'

counterbalanceCondition = '/'.join([ABC_dir, 'counterbalance.csv'])
# Practice code for CSV reading
with open(counterbalanceCondition,'rb') as csvfile:
	counterbalance = numpy.genfromtxt(csvfile, delimiter=',')
# condition[ROW, COLUMN] == [0]subjectNum [1]sandLR(0:1) [2]compGY(0:1)
subjectColumn = counterbalance[:, 0]
print(subjectColumn)
subjectRow = numpy.where(subjectColumn==subject)
sandLR = counterbalance[subjectRow, 1]
compGY = counterbalance[subjectRow, 2]
# set the firm ground to the left or right
# choices = ['sandLeft', 'sandRight']
# firmSandOrder = choices[viz.choose('Platform Setup', choices)]
print('sandLR',sandLR, 'compGY',compGY)
print('sandLR',sandLR, 'compGY',compGY)
#'Is the sand to the right: 1 for yes, 0 for no',''
firmSandOrder = sandLR

practiceTrialsFile = '/'.join([ABC_dir, 'practiceTrials.csv'])
with open(practiceTrialsFile,'rb') as csvfile:
	allPracticeTrials = numpy.genfromtxt(csvfile, delimiter=',')
	# varNames =  {'subjectNum','practiceNum', 'compQuad','adjQuad','compAngle','adjAngle','compDist', 'adjDist'} ;
# Where True, yield x, otherwise yield y.
subjectColumn = allPracticeTrials[:, 0]
print(subjectColumn)
subjectRows = numpy.where(subjectColumn==subject)
#practiceTrials = allPracticeTrials[subjectRows, 1:7]
practiceTrials = allPracticeTrials[subjectRows, 1:8]
print('practiceTrials', practiceTrials)
print(practiceTrials[0,0,1])
#[[   1.      1.      4.     45.    135.     10.     13.33]
# [   2.      4.      1.    135.     45.      8.      4.96]
# [   3.      2.      3.     45.    135.      6.      9.99]
# [   4.      3.      2.    135.     45.     12.      6.33]]
	# varNames = {'subjectNum','practiceNum', 'sandFirm', 'dist'};

# Input Trial
# Used for file naming
input_dir = '/'.join([dissStudy])
# 100 - 1199 DissA; 1200 - 1299 DissB;1300 - 1399 DissC;  TEST 1500s
# outputFilename = strcat(dissStudy, subject, '.csv');
# Load Experimental Conditions
expCondition = '/'.join([input_dir, subjectFile +'.csv'])
# Practice code for CSV reading
with open(expCondition,'rb') as csvfile:
	condition = numpy.genfromtxt(csvfile, delimiter=',')
# [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   
#                         [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
#                         [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
#                         [7]{'compTerrainCode'}    [8]{'AdjustTerrainCode'} 1='firm' 2 ='sand
#						  [9] compsz			[10] adjSz
#                   Matlab doesn't care about the strings condition[:,11:13]
print(condition[0])
########################################################################################################################
# 	LOAD SOUNDS  	# 	LOAD SOUNDS  	# 	LOAD SOUNDS  	# 	LOAD SOUNDS  	# 	LOAD SOUNDS  	# 	LOAD SOUNDS    #
########################################################################################################################
helloWait = viz.addAudio(ABC_dir + '/AudioInstructions/helloWait.mp3')
welcomeAudio = viz.addAudio(ABC_dir + '/AudioInstructions/welcomeAudio.mp3')
# experimentInstructions = viz.addAudio(input_dir + 'turnAround.mp3') moved to later depending on whether 
# adjustable pole is green or yellow
practiceWalkAudio = viz.addAudio(ABC_dir + '/AudioInstructions/practiceWalkAudio.mp3')
#doneExploration = viz.addAudio(ABC_dir + '/AudioInstructions/doneExploration.mp3')
# TODO: replace with actual file
doneExploration = viz.addAudio(ABC_dir + '/AudioInstructions/practiceWalkAudio.mp3')
#beginPractice = viz.addAudio(ABC_dir + '/AudioInstructions/beginPractice.mp3')
beginPractice = viz.addAudio(ABC_dir + '/AudioInstructions/practiceWalkAudio.mp3')

# great you are now about to begin the experimental trials
beginExperiment = viz.addAudio(ABC_dir + '/AudioInstructions/beginExperiment.mp3')
stayInViewingBox = viz.addAudio(ABC_dir + '/AudioInstructions/stayInViewingBox.mp3')

#turnLeft = viz.addAudio(input_dir + '/turnLeft.mp3')
turnLeft = viz.addAudio(ABC_dir + '/AudioInstructions/turnLeft.mp3')
lookLeft = viz.addAudio(ABC_dir + '/AudioInstructions/lookLeft.mp3')
#turnRight = viz.addAudio(input_dir + '/turnRight.mp3')
turnRight = viz.addAudio(ABC_dir + '/AudioInstructions/turnRight.mp3')
lookRight = viz.addAudio(ABC_dir + '/AudioInstructions/lookRight.mp3')
turnAround = viz.addAudio(ABC_dir + '/AudioInstructions/turnAround.mp3')

duration = 0

########################################################################################################################
# 	LOAD MODELS  	# 	LOAD MODELS  	# 	LOAD MODELS  	# 	LOAD MODELS  	# 	LOAD MODELS  	# 	LOAD MODELS    #
########################################################################################################################
viz.clearcolor(0,0.4,1.0) # blue sky
# ground plane
# Make sand surface
WALL_SCALE = [400, 400, 1]
ground = viz.addTexQuad()
ground.setPosition( [0,0,0] )
ground.setEuler([0,90,90])
ground.setScale( WALL_SCALE )
# Apply nice repeating sand texture
C = 2
TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C*.8, WALL_SCALE[2]]
matrix = vizmat.Transform()
matrix.setScale( TEXT_SCALE)
ground.texmat( matrix )
#*****************************************************************
#*****************************************************************
#*****************************************************************
carpet = viz.addTexture('textures/marble2.jpg')
#carpet = viz.addTexture('Models/brittanybaxter/ground.tga')
carpet.wrap(viz.WRAP_T, viz.MIRROR)
carpet.wrap(viz.WRAP_S, viz.REPEAT)
ground.texture(carpet)
ground.visible(viz.ON)
# Load models, ignore "Unknown Chunk" errors
models = {}
models['welcomeBox'] = viz.add('models/redBox.gltf')
models['viewPlate'] = viz.add('models/whiteBox.gltf')
#models['practiceDisc'] = viz.add('textures/redPole.3ds')

# Create red pole
POLE_HEIGHT = 1.3
POLE_RADIUS = 0.35
blue_texture = viz.addTexture('./textures/blue_granite.jpg')
blue_texture.wrap(viz.WRAP_T, viz.REPEAT)
blue_texture.wrap(viz.WRAP_S, viz.REPEAT)
pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
pole.texture(blue_texture)
models['practiceDisc'] = pole
		
## Hide loaded models
models['practiceDisc'].visible(viz.OFF)
# 1m x 1m
models['welcomeBox'].setScale([.5,.15,.58])
# models['viewPlate'].setScale([0.305,.155,0.305])
# models['viewPlate'].setScale([0.305,1.155,0.305])
#cur_pos = viz.get(viz.HEAD_POS)
#eyeheight = cur_pos[1]
#models['viewPlate'].setScale([0.305,(eyeheight*.5)+0.155,0.305])
models['viewPlate'].setScale([0.305,1+0.155,0.305])
# 100 X 0 X 200 # models['boardwalk'].setScale([1,1,1])
####### THE ORIGIN OF THE ROOM WILL DEPEND ON THE PLACEMENT OF THE HEADSET
# IN THE REAL WORLD - MAKE SURE THAT THE PLATE IS BISECTED BY THE SAND AND WOOD
# IF THE HEADSET IS INITIALIZED ON THE PLATFORM THEN 0 GROUND HEIGHT SHOULD BE THE PLATFORM
# REMEMBER THAT THE POLE POSITIONS ARE SET FROM (0,0,0) SO THE HEADSET SHOULD BE INITIALIZED FROM OVERTOP OF THE PLATE
# set the position of the environment objects
# THE ROOM SET UP SHOULD HAVE THE PLATE CENTERED ON THE Z-AXIS BUT THE FRONT EDGE RELATIVELY SHIFTED FROM THE (0,0)
#models['welcomeBox'].setPosition(0, 0, -.095)
# 0.305,.155,0.305
# middle of the plate needs to be at 0 bacause that is where the objects are moved relative to
# the 'front' of the plate changes depending on the direction they are facing
models['viewPlate'].setPosition(0, 0, 0.025)
#firmSandOrder = viz.input('Is the sand to the right: 1 for yes, 0 for no','')
# 100 X 0 X 200 # models['boardwalk'].setPosition(0, 0.148, 0)
# Make firm surface
WALL_SCALE = [200, 400, 1]
concrete = viz.addTexQuad()
concrete.setPosition( [-100, 0.148,0] )
#yaw, pitch, roll
concrete.setEuler([0,90,0])
concrete.setScale( WALL_SCALE )
# Apply nice repeating sand texture
C = 1
TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C*.8, WALL_SCALE[2]]
matrix = vizmat.Transform()
matrix.setScale( TEXT_SCALE)
concrete.texmat( matrix )
concreteImage = viz.addTexture('textures/ground.tga')
concreteImage.wrap(viz.WRAP_T, viz.MIRROR)
concreteImage.wrap(viz.WRAP_S, viz.REPEAT)
concrete.texture(concreteImage)
concrete.visible(viz.OFF)
# Make sand surface
WALL_SCALE = [200, 400, 1]
beach = viz.addTexQuad()
beach.setPosition( [100, 0.148,0] )
beach.setEuler([0,90,0])
beach.setScale( WALL_SCALE )
# Apply nice repeating sand texture
C = 5
TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C, WALL_SCALE[2]]
matrix = vizmat.Transform()
matrix.setScale( TEXT_SCALE)
beach.texmat( matrix )
#*****************************************************************
#*****************************************************************
#*****************************************************************
sand = viz.addTexture('textures/sand.jpg')
#sand = viz.addTexture('Models/brittanybaxter/ground.tga')
sand.wrap(viz.WRAP_T, viz.MIRROR)
sand.wrap(viz.WRAP_S, viz.REPEAT)
beach.texture(sand)
beach.visible(viz.OFF)
################ Make the 8 objects needed ###########
four_sizes = [[.86, 1, .15],[.74, 1.25, .15],[.62, 1.5, .15],[.5, 1.75, .15]]
if compGY == 0:
	instructions = 'comparisonGreen'
	comMarble = viz.addTexture('textures/stone4gr.tga')
	adjMarble = viz.addTexture('textures/stone4ye.tga')
	moveController = viz.addAudio(ABC_dir + '/AudioInstructions/yellowMoveAudio.mp3')
	# you will see green and yellow using the controller to move the XXXX box
#	beginPractice = viz.addAudio(ABC_dir + '/AudioInstructions/practiceYellow.mp3')

	if dissStudy == 'DissA':
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowDistance.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowDistance.mp3')
	elif dissStudy == 'DissB':
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowEnergy.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowEnergy.mp3')
	else:
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowAffordance.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustYellowAffordance.mp3')


elif compGY == 1:
	instructions = 'comparisonYellow'
	comMarble = viz.addTexture('textures/stone4ye.tga')
	adjMarble = viz.addTexture('textures/stone4gr.tga')
	moveController = viz.addAudio(ABC_dir + '/AudioInstructions/greenMoveAudio.mp3')
#	beginPractice = viz.addAudio(ABC_dir + '/AudioInstructions/practiceGreen.mp3')
	
	if dissStudy == 'DissA':
	# adjust to match distance and then pull trigger
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenDistance.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenDistance.mp3')
	elif dissStudy == 'DissB':
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenEnergy.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenEnergy.mp3')
	else:
		moveTriggerController = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenAffordance.mp3')
		experimentInstructions = viz.addAudio(ABC_dir + '/AudioInstructions/adjustGreenAffordance.mp3')


WALL_SCALE1 = [.7, 1, .05]
TEXT_SCALE1 = [1.5,1.5,1.5]

#practice
adjScale = [.9, .8, .15]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
practicePole = vizshape.addBox(splitFaces=True)
practicePole.setScale(adjScale)
adjMatrix = vizmat.Transform()
adjMatrix.setScale( adjScale )
practicePole.texmat( adjMatrix )
adjMarble.wrap(viz.WRAP_T, viz.REPEAT)
adjMarble.wrap(viz.WRAP_S, viz.REPEAT)
practicePole.texture(adjMarble)
practicePole.visible(viz.OFF)
practicePoleComp = vizshape.addBox(splitFaces=True)
practicePoleComp.setScale(adjScale)
practicePoleComp.texmat( adjMatrix )
comMarble.wrap(viz.WRAP_T, viz.REPEAT)
comMarble.wrap(viz.WRAP_S, viz.REPEAT)
practicePoleComp.texture(comMarble)
practicePoleComp.visible(viz.OFF)
### Make green comparision poles
## Build the comparison pole in the pair
#1
comScale = four_sizes[0]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*comScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*comScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*comScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
comparisonPole1 = vizshape.addBox(splitFaces=True)
comparisonPole1.setScale(comScale)
comMatrix = vizmat.Transform()
comMatrix.setScale( comScale )
comparisonPole1.texmat( comMatrix )
comMarble.wrap(viz.WRAP_T, viz.REPEAT)
comMarble.wrap(viz.WRAP_S, viz.REPEAT)
comparisonPole1.texture(comMarble)
comparisonPole1.visible(viz.OFF)
#2
comScale = four_sizes[1]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*comScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*comScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*comScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
comparisonPole2 = vizshape.addBox(splitFaces=True)
comparisonPole2.setScale(comScale)
comMatrix = vizmat.Transform()
comMatrix.setScale( comScale )
comparisonPole2.texmat( comMatrix )
comMarble.wrap(viz.WRAP_T, viz.REPEAT)
comMarble.wrap(viz.WRAP_S, viz.REPEAT)
comparisonPole2.texture(comMarble)
comparisonPole2.visible(viz.OFF)
#3
comScale = four_sizes[2]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*comScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*comScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*comScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
comparisonPole3 = vizshape.addBox(splitFaces=True)
comparisonPole3.setScale(comScale)
comMatrix = vizmat.Transform()
comMatrix.setScale( comScale )
comparisonPole3.texmat( comMatrix )
comMarble.wrap(viz.WRAP_T, viz.REPEAT)
comMarble.wrap(viz.WRAP_S, viz.REPEAT)
comparisonPole3.texture(comMarble)
comparisonPole3.visible(viz.OFF)
#4
comScale = four_sizes[3]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*comScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*comScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*comScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
comparisonPole4 = vizshape.addBox(splitFaces=True)
comparisonPole4.setScale(comScale)
comMatrix = vizmat.Transform()
comMatrix.setScale( comScale )
comparisonPole4.texmat( comMatrix )
comMarble.wrap(viz.WRAP_T, viz.REPEAT)
comMarble.wrap(viz.WRAP_S, viz.REPEAT)
comparisonPole4.texture(comMarble)
comparisonPole4.visible(viz.OFF)
### Make yellow adjustable object
## Build the adjustment pole in the pair
#1
adjScale = four_sizes[0]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
adjustablePole1 = vizshape.addBox(splitFaces=True)
adjustablePole1.setScale(comScale)
adjMatrix = vizmat.Transform()
adjMatrix.setScale( adjScale )
adjustablePole1.texmat( adjMatrix )
adjMarble.wrap(viz.WRAP_T, viz.REPEAT)
adjMarble.wrap(viz.WRAP_S, viz.REPEAT)
adjustablePole1.texture(adjMarble)
adjustablePole1.visible(viz.OFF)
#2
adjScale = four_sizes[1]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
adjustablePole2 = vizshape.addBox(splitFaces=True)
adjustablePole2.setScale(comScale)
adjMatrix = vizmat.Transform()
adjMatrix.setScale( adjScale )
adjustablePole2.texmat( adjMatrix )
adjMarble.wrap(viz.WRAP_T, viz.REPEAT)
adjMarble.wrap(viz.WRAP_S, viz.REPEAT)
adjustablePole2.texture(adjMarble)
adjustablePole2.visible(viz.OFF)
#3
adjScale = four_sizes[2]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
adjustablePole3 = vizshape.addBox(splitFaces=True)
adjustablePole3.setScale(comScale)
adjMatrix = vizmat.Transform()
adjMatrix.setScale( adjScale )
adjustablePole3.texmat( adjMatrix )
adjMarble.wrap(viz.WRAP_T, viz.REPEAT)
adjMarble.wrap(viz.WRAP_S, viz.REPEAT)
adjustablePole3.texture(adjMarble)
adjustablePole3.visible(viz.OFF)
#4
adjScale = four_sizes[3]
TEXT_X = TEXT_SCALE1[0]/WALL_SCALE1[0]*adjScale[0]
TEXT_Y = TEXT_SCALE1[1]/WALL_SCALE1[1]*adjScale[1]
TEXT_Z = TEXT_SCALE1[2]/WALL_SCALE1[2]*adjScale[2]
TEXT_SCALE = [TEXT_X,TEXT_Y,TEXT_Z]
adjustablePole4 = vizshape.addBox(splitFaces=True)
adjustablePole4.setScale(comScale)
adjMatrix = vizmat.Transform()
adjMatrix.setScale( adjScale )
adjustablePole4.texmat( adjMatrix )
adjMarble.wrap(viz.WRAP_T, viz.REPEAT)
adjMarble.wrap(viz.WRAP_S, viz.REPEAT)
adjustablePole4.texture(adjMarble)
adjustablePole4.visible(viz.OFF)

########################################################################################################################
# SET UP QUADRANTS AND ANGLES # SET UP QUADRANTS AND ANGLES # SET UP QUADRANTS AND ANGLES # SET UP QUADRANTS AND ANGLES #
########################################################################################################################
# [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   
#                         [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
#                         [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
#                         [7]{'compTerrainCode'}    [8]{'AdjustTerrainCode'} 1='firm' 2 ='sand
#						  [9] compsz			[10] adjSz 	                1,2,3, or 4
#                   Matlab doesn't care about the strings condition[:,11:13]
#condition[:,8] 1 or 0:
practiceSpotsFirst = [[40.0, .75], [15.0, 1], [0,0.035], [25.0, 1.0], [0,0.035],[30.0, 1.25]]
practiceSpotsSecond = [[40.0, .75], [15.0, 1], [0,0.035], [30.0, 1.25], [25.0, 1.0], [0,0.035]]
# condition [8,9] give the comparison and adjustable pole quadrant numbered by plane geometry 1-4
# because we use 4 quadrants we use 45 and 135 the sign of the z value will be correctly calculated but the 
#x needs to be changed to mirror it about the x axis
poleSpots = [[1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0], [1.0, 1.0]]
# the true sandbox is quadrant 1 before adjustment
if firmSandOrder == 1:
	# TODO: replace with actual file
	lookEnvironment = viz.addAudio(ABC_dir + '/AudioInstructions/lookLeft.mp3')

#practiceTrials[0,0,1] == 1/4 means the practice and walk should also start on sand
	if practiceTrials[0,0,1] == 1 or practiceTrials[0,0,1] == 4:
		# set up the pole on the sand first
		practice_stage = 'sand'
		surface_order = ['sand','sand','sand','firm','firm','firm','sand','firm','sand','firm', 'sand', 'firm']
		practiceSpotsSand = practiceSpotsFirst
		practiceSpotsFirm = practiceSpotsSecond
			# audio_order = [1-2,2-3,3-4,4-5,6-7,7-8,8-9,9-10,10-11,11-12,12-13]
		audio_order = ['n','n','l','r','n','r','l','l','l','r','r','r']

	elif practiceTrials[0,0,1] == 2 or practiceTrials[0,0,1] == 3:
		practice_stage = 'firm'
		surface_order = ['firm','firm','firm','sand','sand','sand','firm','sand','firm','sand', 'firm', 'sand']
		practiceSpotsFirm = practiceSpotsFirst
		practiceSpotsSand = practiceSpotsSecond
		# audio_order = [1-2,2-3,3-4,4-5,6-7,7-8,8-9,9-10,10-11,11-12,12-13]
		# audio_order =[F1,F2, home,S1,S2, home,F3,S3, home,S4,F4,home]
		audio_order = ['n','n','r','l','n','l','r','r','r','l','l','l']
		
#firmSandOrder = viz.input('Is the sand to the right: 1 for yes, 0 for no','')
elif firmSandOrder == 0:
	poleSpots[0][0] = -1.0
	poleSpots[1][0] = 1.0
	poleSpots[2][0] = 1.0
	poleSpots[3][0] = -1.0
	# TODO: replace with actual file
	lookEnvironment = viz.addAudio(ABC_dir + '/AudioInstructions/lookLeft.mp3')
#	poleSpots[2][1] = -1.0
#	poleSpots[3][1] = 1.0
	# 100 X 0 X 200
	concrete.setPosition(100, 0.148, 0)
	# 100 X 0 X 200
	beach.setPosition(-100, 0.148, 0)

#practiceTrials[0,0,1] == 1|4 means the practice and walk should also start on firm
	if practiceTrials[0,0,1] == 1 or practiceTrials[0,0,1] == 4:
		practice_stage = 'firm'
		surface_order = ['firm','firm','firm','sand','sand','sand','firm','sand','firm','sand', 'firm', 'sand']
		practiceSpotsFirm = practiceSpotsFirst
		practiceSpotsSand = practiceSpotsSecond
	#firmSandOrder = viz.input('Is the sand to the right: 1 for yes, 0 for no','')
		audio_order = ['n','n','l','r','n','r','l','l','l','r','r','r']		
		
	elif practiceTrials[0,0,1] == 2 or practiceTrials[0,0,1] == 3:
		# set up the pole on the sand first
		practice_stage = 'sand'
		surface_order = ['sand','sand','sand','firm','firm','firm','sand','firm','sand','firm', 'sand', 'firm']
		practiceSpotsSand = practiceSpotsFirst
		practiceSpotsFirm = practiceSpotsSecond
		# audio_order = [1-2,2-3,3-4,4-5,6-7,7-8,8-9,9-10,10-11,11-12,12-13]
		# audio_order =[S1,S2, home,F1,F2, home,S4,F4,home,F3,S3, home]
		audio_order = ['n','n','r','l','n','l','r','r','r','l','l','l']


print('practice_stage', practice_stage)
print('surface_order', surface_order)
print('practice_stage', practice_stage)
print('')
print('audio_order', audio_order)




########################################################################################################################
# 	Initialized counts and variables  # 	Initialized counts and variables  # 	Initialized counts and variables  #
########################################################################################################################
# Number of practice trials
# practice_walk_num is starting at 0 so 5 is a total of 6
# PRACTICE_TRIALS = 11
PRACTICE_TRIALS = 12
# Total number of trials in experiment
# 4 distances x 4 terrain pairs (e.g. firm-firm, firm-sand) x 8 repititions                      
TOTAL_TRIALS = 128
#TOTAL_TRIALS = 30
THRESHOLD_THETA = 15 # Maximum angle participant can deviate when looking at orienting pole
DISC_TRIGGER_RADIUS = .2 #plate is 30 cm wide
# frequency of masterloop, display, and data collection
Hz = 90 
sand_count = 0
firm_count = 0		
end_practice_time = 0
appearance_time = 0
end_time = 0
xPosP = 3.0
poleDistP = 5.0
poleAnglePRad = math.radians(90)
#initialize output strings
data_batch_pos = ''
data_batch_polePos = ''
data_batch_rot = ''

DATA_COLLECT = True

# Trial and global time counter set to 0
time = 0
time_stamp = 0
time_global = 0
playStart = 0
trial_start = 0

# Starts practice count at 1
practice_num = 0
practice_walk_num = 0
incrementOfAdjustment = 0.05
time = 0
end_instructions_time = 0
xSignP = -1

# the trigger has not been pulled
decisionMade = False
poleDistA = condition[trial_num-1, 2]
#poleRotations = [-45,45,-45,45]
poleRotations = [45,-45,45,-45]
for controller in steamvr.getControllerList():
	# Create model for controller
	controller = controller
	print('controller found')
	print('controller found')
	print('controller found')
	print('controller found')
degBw = 0
signedDirection = 0
experimentStart = 0
controllerInstructionPlayed = 0
controllerInstructionDuration = moveController.getDuration()
turnInstructionPlayed = 0
durationRight = lookRight.getDuration()
durationLeft = lookLeft.getDuration()
durationAround = turnAround.getDuration()
outsideOfViewingBox = False #make True in the interactive bar to play reminder
durationPracticeWalkAudio = practiceWalkAudio.getDuration()
practiceWalkAudioPlayed = 0
beginExperimentPlayed = 0
beginExperimentDuration = beginExperiment.getDuration()
experimentInstructionDuration = experimentInstructions.getDuration()
experimentInstructionPlayed = 0
lookEnvironmentPlayed = 0
lookEnvironmentDuration = lookEnvironment.getDuration()
data = []
trialLoopNum = 0
emergencyStop = False
start_response = 0
########################################################################################################################
# HELPER FUNCTIONS # HELPER FUNCTIONS # HELPER FUNCTIONS # HELPER FUNCTIONS # HELPER FUNCTIONS # HELPER FUNCTIONS #
########################################################################################################################
def printLoop(trialLoopNum, framePrintRate, phrase, variable):
# trialLoopNum: one each loop the num grows at the specified HZ (probably 90/sec)
# framePrintRate: how often do I want it to print? every frame? every other?
	if trialLoopNum%framePrintRate == 0:
		print(phrase, variable)


def leftOrRight(lookingObjectPosn, lookedAtObjectPosn, lookingObjectYaw):
	global signedDirection
# a distanc greater than any of the positions
	distToObject = 20
	lookingObjectRad = math.radians(lookingObjectYaw)
	
	lookingPosition = [math.sin(lookingObjectRad)*distToObject, 0, math.cos(lookingObjectRad)*distToObject]
# Assuming the points are (Ax,Ay) (Bx,By) and (Cx,Cy), you need to compute:
# (Bx - Ax) * (Cy - Ay) - (By - Ay) * (Cx - Ax)
# This will equal zero if the point C is on the line formed by points A and B, and will have a different sign 
# depending on the side. Which side this is depends on the orientation of your (x,y) coordinates, but you can plug 
# test values for A,B and C into this formula to determine whether negative values are to the left or to the right.
	signedDirection =(lookingPosition[0] - lookingObjectPosn[0]) * (lookedAtObjectPosn[2] - lookingObjectPosn[2]) - (lookingPosition[2] - lookingObjectPosn[2]) * (lookedAtObjectPosn[0] - lookingObjectPosn[0])
	return signedDirection

# used to determine the alpha value for the comaprision and adjustable objects
def looking(lookingObjectPosn, lookedAtObjectPosn, lookingObjectYaw):
	global degBw
	"""lookingObjectPosn: position of object that is looking
	lookedAtObjectPosn: position of object looked at
	lookingObjectYaw: yaw of the object that is looking (degrees)
	thresholdTheta: viewing angle must be +/- this amount in order to be considered 'looking at' the object. degrees
	"""
	degRelOrientation = universals.relativeOrientation(lookingObjectPosn, lookedAtObjectPosn)*180.0/math.pi #radToDeg(val):	return val*(180.0/math.pi)
	degRelOrientation = (degRelOrientation+180)%360-180 #into 0to 180 am 0 to -180
	degBw = (degRelOrientation-lookingObjectYaw)
	return degBw
########################################################################################################################
########################################################################################################################
# Master Loop ## Master Loop ## Master Loop ## Master Loop ## Master Loop ## Master Loop ## Master Loop ## Master Loop #
########################################################################################################################
########################################################################################################################
def masterLoop(num):
	global time,  poleSpots, trial_stage, trial_num, practice_walk_num, practice_num, incrementOfAdjustment, practiceTrials,\
	frame,data_batch_polePos, data_batch_pos, data_batch_rot, sand_count, firm_count, \
	DATA_COLLECT, THRESHOLD_THETA, DISC_TRIGGER_RADIUS, PRACTICE_TRIALS, TOTAL_TRIALS,\
	decisionMade, trigger, poleDistA, practice_stage, end_practice_time,\
	appearance_time, surface_order, end_time, practiceSpotsFirm, practiceSpotsSand, controller,\
	xPosP,poleDistP,poleAnglePRad,end_instructions_time,xSignP, instructions, degBw,signedDirection, experimentStart,\
	controllerInstructionPlayed, controllerInstructionDuration, turnInstructionPlayed, durationRight, durationLeft, durationAround,\
	outsideOfViewingBox, audio_order, data, \
	beginExperimentPlayed, experimentInstructionDuration, experimentInstructionPlayed,beginExperimentDuration, practiceWalkAudioPlayed, durationPracticeWalkAudio,\
	trialLoopNum, skipControllerInstructions, straightToInstructions, emergencyStop, lookEnvironmentPlayed, lookEnvironmentDuration, \
	comparisonPole, adjustablePole, playStart,trial_start, start_response

	trialLoopNum = trialLoopNum + 1

	for controller in steamvr.getControllerList():
		controller = controller
#		print 'controller found'
# 	# practiceSpots,
# myTracker = viz.add('sensor.dls')   # Connect to a sensor
# print myTracker.getPosition() # Print sensor position
# print myTracker.getEuler() # Print sensor euler rotation
# data = myTracker.getData()  # Access the raw data from the sensor
# print data  # Print the array of data

	# Time (in sec) elapsed since the last run of masterLoop and then added to the global time
	frame_elapsed = viz.getFrameElapsed()
	time += frame_elapsed
# Current position and roation of the participant
	cur_pos = viz.get(viz.HEAD_POS)
	cur_rot = viz.get(viz.HEAD_ORI)
######################
# Initial Start Up   #
######################
	if trial_stage ==  'welcome_environment':
		welcomeAudio.play()
		playStart = time
		trial_stage = 'step_up_on_plate'
		print(trial_stage)

	if trial_stage ==  'step_up_on_plate':
		if (universals.inRadius(cur_pos, models['viewPlate'].getPosition(), DISC_TRIGGER_RADIUS+.15)) and \
		not (universals.inRadius(cur_pos, [0, 0, 0], DISC_TRIGGER_RADIUS)):
			printLoop(trialLoopNum, 120, 'getting warmer +++++++++++++++++++++++++++++++++++++++++++', universals.distance(cur_pos[0],cur_pos[2],0,0.025))
			# print 'getting warmer +++++++++++++++++++++++++++++++++++++++++++'
			# print universals.distance(cur_pos[0],cur_pos[2],0,0.025)
		if (universals.inRadius(cur_pos,[0, 0, 0] , DISC_TRIGGER_RADIUS)) and \
		(time - playStart) > 16.25:
			print('standing on plate')
			print('done playing welcome')
			trial_stage = 'enter_environment'
			print(trial_stage)

######################
# World Triggered   #
######################
	if trial_stage ==  'enter_environment':
	# cur_rot[1] should be pitch; [0] is yaw
		if universals.facing(cur_pos, [0,0,100], cur_rot[1], THRESHOLD_THETA+7) and \
		not universals.facing(cur_pos, [0,0,100], cur_rot[1], THRESHOLD_THETA):
			printLoop(trialLoopNum, 120, 'look up more ++++++++++++++++++++++++++++++++', 0)
			# print 'look up more ++++++++++++++++++++++++++++++++'
		if universals.facing(cur_pos, [0,0,100], cur_rot[1], THRESHOLD_THETA):
			models['welcomeBox'].visible(viz.OFF)
			concrete.visible(viz.ON)
			beach.visible(viz.ON)
			print('World appears!')
			# trial_stage = 'practice_disc_setup'		
			trial_stage = 'look_environment_prepractice'
			print(trial_stage)

	if trial_stage ==  'look_environment_prepractice':
		playStart = time
		lookEnvironment.play()
		trial_stage = 'look_environment_playing'
		print(trial_stage)

	if trial_stage ==  'look_environment_playing':
#		if	(time - lookEnvironmentPlayed) > lookEnvironmentDuration:
		if	(time - playStart) > 9:
			trial_stage = 'practice_controller_setup1'
			print(trial_stage)

################################
# pratice with the controller  #
################################
	if trial_stage == 'practice_controller_setup1':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
		# poleSpots = [[1 1], [-1 1], [-1 -1], [1 -1]]
#        the sand is on the LEFT poleSpots = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
		if practice_stage == 'sand':
			xSignP = poleSpots[0][0]
		elif practice_stage == 'firm':
			xSignP = poleSpots[1][0]
#		print 'xSignP', xSignP
		printLoop(trialLoopNum, 180,'xSignP', xSignP)

		practicePole.setPosition(xPosP*xSignP, 0, 0)
		practicePole.setEuler([90,0,0])
		practicePole.visible(viz.ON)

# play which direction they need to turn
		leftOrRight(cur_pos, practicePole.getPosition(), cur_rot[0]) 
	# negative is turn right # positive is turn left
		printLoop(trialLoopNum, 180,'signedDirection', signedDirection)
		# if they are not already looking at the practice pole then tell them to turn
		if not universals.facing(cur_pos, practicePole.getPosition(), cur_rot[0], (THRESHOLD_THETA+10)):
			if signedDirection < -15:
				playStart = time
				turnRight.play()
				print('instructed to turn right')
				print('instructed to turn right')
				print('instructed to turn right')
			elif signedDirection > 15:
				playStart = time
				turnLeft.play()
				print('instructed to turn left')
				print('instructed to turn left')
				print('instructed to turn left')

		if skipControllerInstructions:
			trial_stage = 'controller_practice'
			print(trial_stage)
		elif not skipControllerInstructions:
			trial_stage = 'controller_instructions'
			print(trial_stage)

###################################
# pratice move instructions #
###################################
	if trial_stage == 'controller_instructions':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
		# if they have turned to face the practice pole then the instructions can play
		if universals.facing(cur_pos, practicePole.getPosition(), cur_rot[0], (THRESHOLD_THETA+10)):
			playStart = time
	# instructions = comparisonGreen
#	# talk about the trackpad and move onto next stage while playing
			moveController.play()
			trial_stage = 'controller_practice'
			print(trial_stage)

################################
# pratice with the controller  #
################################
	if trial_stage == 'controller_practice':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
#		print 'World appears!'
#		print 'xSignP', xSignP
		if universals.facing(cur_pos, practicePole.getPosition(), cur_rot[0], THRESHOLD_THETA):

			printLoop(trialLoopNum, 180, 'is trigger down', controller.isButtonDown(2))

			printLoop(trialLoopNum, 180, 'is the trackpad pushed down', controller.isButtonDown(3))

			printLoop(trialLoopNum, 180, 'is the trackpad touched', controller.isButtonDown(4))

			printLoop(trialLoopNum, 180, 'trackpad', controller.getTrackpad())

			xT,yT = controller.getTrackpad()

			printLoop(trialLoopNum, 180, 'trackpad y', yT)

#			if the frame rate is 90 frames per seconds and the pole doesn't need to be moved more than 8m
# 			and the subject could eaisily have 20 seconds per trial, then moving .3m/sec is good for slow speed
#			1.8m/90fm = 0.02
			# small increment change
			xx,yy,zz = practicePole.getPosition()
#			def distance(x,y,a,b):
#				return ((x-a)**2+(y-b)**2)**.5
			printLoop(trialLoopNum, 180, 'xx same as dist....  and consider sign', xx)
			poleDistP = universals.distance(0.0,0.0,xx,zz)
			# the first distance should be 3 m
			printLoop(trialLoopNum, 180, 'poleDistP', poleDistP)

			if practice_stage == 'sand':
				xSignP = poleSpots[0][0]
			elif practice_stage == 'firm':
				xSignP = poleSpots[1][0]
	#		print 'xSignP', xSignP
			printLoop(trialLoopNum, 180,'xSignP', xSignP)

#			moving .9m/sec is good for fast speed#			0.3m/90 is the distance per frame = 0.003
			# large increment change
			if controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistP + 0.04 < 24:
						poleDistP = poleDistP + 0.04
				elif yT < -0.6:
					if poleDistP - 0.04 > 1.5:
						poleDistP = poleDistP - 0.04
				xPosP = poleDistP*xSignP
				practicePolePosition = [xPosP,0,0]
#				print 'moving to new practicePolePosition', practicePolePosition
				printLoop(trialLoopNum, 90, 'moving to new practicePolePosition', practicePolePosition)
				flyToPoint = vizact.moveTo(practicePolePosition, speed=3.6, interpolate=None)
				practicePole.addAction(flyToPoint)

			elif controller.isButtonDown(4) and not controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistP + 0.02 < 24:
						poleDistP = poleDistP + 0.02
				elif yT < -0.6:
					if poleDistP - 0.02 > 1.5:
						poleDistP = poleDistP - 0.02

				xPosP = poleDistP*xSignP
				practicePolePosition = [xPosP,0,0]
#				print 'moving to new practicePolePosition', practicePolePosition
				printLoop(trialLoopNum, 90, 'moving to new practicePolePosition', practicePolePosition)
				flyToPoint = vizact.moveTo(practicePolePosition, speed=1.8, interpolate=None)
				practicePole.addAction(flyToPoint)


			# touchpad is not touched
			elif not controller.isButtonDown(3) and not controller.isButtonDown(4):
				practicePole.clearActionList(pool = 0)

			printLoop(trialLoopNum, 180, 'poleDistP new', poleDistP)

			# print 'since controllerInstructionPlayed', (time - controllerInstructionPlayed)
			printLoop(trialLoopNum, 180, 'since controllerInstructionPlayed', (time - controllerInstructionPlayed))


	#			*****************************************************
	#			*****************************************************
	#			*****************************************************
			if (time - playStart) > controllerInstructionDuration + 4:
#			if (time - controllerInstructionPlayed) > controllerInstructionDuration + 4:
				# trial_stage = 'decision_instructions'
				practicePole.visible(viz.OFF)
				trial_stage = 'practice_disc_height'
				models['viewPlate'].setPosition(0, 0, 0.035)
				print(trial_stage)

####################
# Practice  Setup  #
####################
	if trial_stage == 'practice_disc_height':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
#		print 'World appears!'
#		height = cur_pos[1] - .155
		# Adjust models size
		#.4 x 3 x .4
		models['practiceDisc'].setScale([.70,1.3/3,.70])
		practiceWalkAudioPlayed = time
		practiceWalkAudio.play()
		trial_stage = 'practice_walk_playing'
		print('trial_stage', trial_stage)

	if trial_stage == 'practice_walk_playing':
		printLoop(trialLoopNum, 120, 'percent clip has been playing',((time - practiceWalkAudioPlayed)/durationPracticeWalkAudio))
		if skipControllerInstructions:
			trial_stage = 'practice_disc_setup'
			print('trial_stage', trial_stage)

		if (time - practiceWalkAudioPlayed) > (durationPracticeWalkAudio - 3):
			trial_stage = 'practice_disc_setup'
			print('trial_stage', trial_stage)
			
	if trial_stage == 'practice_disc_setup':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
#		print 'World appears!'
		# surface_order = ['firm','firm','firm','sand','sand','sand','firm','sand','firm','sand', 'firm', 'sand']
		# the audio is for the audio played to arrive at that pole; they can see F1 from practice so nothing plays before it appears
		# # audio_order =[F1,F2, home,S1,S2, home,F3,S3, home,S4,F4,home]
		# audio_order = ['n','n','r','l','n','l','r','r','r','l','l','l']
		print('practice_walk_num', practice_walk_num)
		practice_walk_audio = audio_order[practice_walk_num]
		print('audio_order', practice_walk_audio)
		if practice_walk_audio == 'r':
			print('playing look right')
			lookRight.play()
		elif practice_walk_audio == 'l':
			print('playing look left')
			lookLeft.play()
		# experiment starts at 0, the participant walks to P1
		if practice_stage == 'sand':
			print('practice_stage', practice_stage)
			print('sand count', sand_count)
			print('firm count', firm_count)
			print('practice num', practice_walk_num)
			# SET UP THE practiceDisc POSTIONS 
			# loop throught the 3 spots with their angles and distances
			# the sand is on the RIGHT# poleSpots = [[1 1], ...]
			# the sand is on the LEFT# poleSpots = [[-1, 1], ...]
			xSign = poleSpots[0][0]
			zSign = poleSpots[0][1]
			poleAngle = practiceSpotsSand[sand_count][0]
			# cos/sin takes argument in radians
			poleAngleRad = math.radians(poleAngle)
			poleDist = practiceSpotsSand[sand_count][1]
			xPos = math.sin(poleAngleRad)*poleDist*xSign
			zPos = math.cos(poleAngleRad)*poleDist*zSign
			models['practiceDisc'].setPosition(xPos, 0, zPos)
			appearance_time = time
			models['practiceDisc'].alpha(0)
			models['practiceDisc'].visible(viz.ON)
			print('practice disc set to', models['practiceDisc'].getPosition())
			sand_count = sand_count + 1
			practice_walk_num = practice_walk_num + 1

		if practice_stage == 'firm':
			print('practice_stage', practice_stage)
			print('sand count', sand_count)
			print('firm count', firm_count)
			print('practice practice_walk_num', practice_walk_num)
			# loop throught the 3 spots with their angles and distances
	# the next 3 trials should loop through the spots again
	#        the sand is on the RIGHT; firm is on the left# poleSpots = [[1 1], [-1 1], ...]
	#        the sand is on the LEFT; firm is on the right#        poleSpots = [[-1, 1], [1, 1], ...]
			xSign = poleSpots[1][0]
			zSign = poleSpots[1][1]
			# practiceSpots = [[20 1], [45 2], [30 .5]]
			# poleAngle = practiceSpots[firm_count][0]
			poleAngle = practiceSpotsFirm[firm_count][0]
			# cos/sin takes argument in radians
			poleAngleRad = math.radians(poleAngle)
			poleDist = practiceSpotsFirm[firm_count][1]
			xPos = math.sin(poleAngleRad)*poleDist*xSign
			zPos = math.cos(poleAngleRad)*poleDist*zSign
			models['practiceDisc'].setPosition(xPos, 0, zPos)
			appearance_time = time
			models['practiceDisc'].alpha(0)
			models['practiceDisc'].visible(viz.ON)
			print('practice disc set to', models['practiceDisc'].getPosition())
			firm_count = firm_count + 1
			practice_walk_num = practice_walk_num + 1
			
		trial_stage = 'practice_head_to_disc'
		print(trial_stage)
		
####################
# Practice  Walk   #
####################
	if trial_stage == 'practice_head_to_disc':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)

		printLoop(trialLoopNum, 160, 'time-appearance_time', (time - appearance_time))

		if (time - appearance_time)*1.2 < 1:
			models['practiceDisc'].alpha((time - appearance_time)*1.2)
		elif (time - appearance_time)*1.2 >= 1:
			models['practiceDisc'].alpha(1)

		# they have reached the pole, trigger trial end and play where they should look for the next spot
		if (universals.inRadius(cur_pos, models['practiceDisc'].getPosition(), .12)):
			models['practiceDisc'].visible(viz.OFF)
			print('standing in disc++++++++++++++++')
			trial_stage = 'practice_arrived_at_disc'
			print(trial_stage)

####################
# Practice at Disc #
####################
	if trial_stage == 'practice_arrived_at_disc':
#		PRACTICE_TRIALS = 12
		if practice_walk_num == PRACTICE_TRIALS:
			models['viewPlate'].setPosition(0, 0, 0.04)
			end_practice_time = time
			trial_stage = 'done_exploration'
			print(trial_stage)
		else:
			trial_stage = 'practice_disc_setup'
			practice_stage = surface_order[practice_walk_num]

############################
# Practice at sand is sand #
############################
	if trial_stage == 'done_exploration':
		# now you have experianced that the surface that looks like sand is sand and the surface the looks solid is solid
		lookEnvironmentPlayed = time
		lookEnvironmentDuration = doneExploration.getDuration()
		doneExploration.play()
		trial_stage = 'playing_notice_terrain'
		print(trial_stage)

	if trial_stage == 'playing_notice_terrain':

		if	(time - lookEnvironmentPlayed) > lookEnvironmentDuration:
		# to be used to figure out how long experiment has been running
			end_practice_time = time
			trial_stage = 'start_of_four_practice'
			print(trial_stage)

################################
# pratice with the controller  #
################################
# practice_num starts at 0
# practiceTrials  = ['practiceNum', 'compQuad','adjQuad','compAngle','adjAngle', 'compDist', 'adjDist'];

###################################
# pratice decision instructions #
###################################
	if trial_stage == 'start_of_four_practice':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
		# play the practice with the standard and comparison
		controllerInstructionPlayed = time
		beginPractice.play()	
		controllerInstructionDuration = beginPractice.getDuration()
		trial_stage = 'playing_four_practice'
		print(trial_stage)

	if trial_stage == 'playing_four_practice':
		if (time - controllerInstructionPlayed) > controllerInstructionDuration:
			trial_stage = 'decision_instructions'
			print(trial_stage)	
			
	if trial_stage == 'decision_instructions':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
		# play instructions that the trigger makes the decision final
		# move it again and then make a decision by pulling the trigger all thge way
		# play instructions the green/yellow pole you see
		controllerInstructionPlayed = time
		# this will say distance, energy, or ease of walking
		moveTriggerController.play()
		controllerInstructionDuration = moveTriggerController.getDuration()
		print('controllerInstructionDuration', controllerInstructionDuration)
		trial_stage = 'playing_decision_instructions'
		print(trial_stage)

	if trial_stage == 'playing_decision_instructions':
#			controllerInstructionPlayed = controllerInstructionPlayed + 3
		printLoop(trialLoopNum, 180, 'still playing instructions ', ((time - controllerInstructionPlayed)/controllerInstructionDuration))
		# trial_stage = 'decision_practice'
		if (time - controllerInstructionPlayed) > controllerInstructionDuration:
			trial_stage = 'practice_controller_setup2'
			print(trial_stage)	
			
################################
# set  up pratice boxes  #
################################
	if trial_stage == 'practice_controller_setup2':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
#print practiceTrials[0]
#[[   1.      1.      4.     45.    135.     10.     13.33]
# [   2.      4.      1.    135.     45.      8.      4.96]
# [   3.      2.      3.     45.    135.      6.      9.99]
# [   4.      3.      2.    135.     45.     12.      6.33]]
		####### SET UP THE COMPARISON POLE #######
		# poleSpots = [[1 1], [-1 1], [-1 -1], [1 -1]]
#        the sand is on the LEFT poleSpots = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
		poleDist = practiceTrials[0,practice_num, 5] # 6,8,10,12 m
#	   [3]{'compAngle'}   [4]{'adjAngle'}       45 deg or 135 deg
		poleAngle = practiceTrials[0,practice_num, 3]
		# cos/sin takes argument in radians
		poleAngleRad = math.radians(poleAngle)
#	   [1]{'compQuadrant'}   [2]{'adjQuad'}               by plane geometry 1-4
		comparisonSpot = int(practiceTrials[0,practice_num, 1])
#		print 'comparisonSpot', comparisonSpot
		printLoop(trialLoopNum, 180, 'comparisonSpot', comparisonSpot)
		# plane geometry 1:4 subtract 1 to get relevant array value
		xSign = poleSpots[comparisonSpot-1][0]
		zSign = poleSpots[comparisonSpot-1][1]
		xPos = math.sin(poleAngleRad)*poleDist*xSign
		zPos = math.cos(poleAngleRad)*poleDist*zSign
		practicePoleComp.setPosition(xPos, 0, zPos)
		poleRot = poleRotations[comparisonSpot-1]
		practicePoleComp.setEuler([poleRot,0,0])
		practicePoleComp.visible(viz.ON)

		####### SET UP THE ADJUSTABLE POLE #######
		poleDistP = practiceTrials[0,practice_num, 6] # randomly generated between 4 and 14
#	   [3]{'compAngle'}   [4]{'adjAngle'}       45 deg or 135 deg
		poleAngle = practiceTrials[0,practice_num, 4]
		# cos/sin takes argument in radians
		poleAngleARad = math.radians(poleAngle)
#	   [1]{'compQuadrant'}   [2]{'adjQuad'}               by plane geometry 1-4
		adjustableSpot = int(practiceTrials[0,practice_num, 2])
		printLoop(trialLoopNum, 180,'adjustableSpot', adjustableSpot)
		# plane geometry 1:4 subtract 1 to get relevant array value
		xSignA = poleSpots[adjustableSpot-1][0]
		zSignA = poleSpots[adjustableSpot-1][1]
		xPosA = math.sin(poleAngleARad)*poleDistP*xSignA
		zPosA = math.cos(poleAngleARad)*poleDistP*zSignA
		practicePole.setPosition(xPosA, 0, zPosA)
		poleRot = poleRotations[adjustableSpot-1]
		practicePole.setEuler([poleRot,0,0])
		practicePole.visible(viz.ON)
		trial_stage = 'decision_practice'
		
		print(trial_stage)


###############################
## pratice moving & decision  #
###############################
				
	if trial_stage == 'decision_practice':
		practicePoleComp.visible(viz.ON)
		practicePole.visible(viz.ON)
		if universals.facing(cur_pos, practicePole.getPosition(), cur_rot[0], THRESHOLD_THETA):
			printLoop(trialLoopNum, 180, 'is trigger down', controller.isButtonDown(2))
			printLoop(trialLoopNum, 180, 'is the trackpad pushed down', controller.isButtonDown(3))
			printLoop(trialLoopNum, 180, 'is the trackpad touched', controller.isButtonDown(4))
			printLoop(trialLoopNum, 180, 'trackpad', controller.getTrackpad())
			xT,yT = controller.getTrackpad()
			printLoop(trialLoopNum, 180, 'trackpad y', yT)

			# adjustable pole
			xx,yy,zz = practicePole.getPosition()
			poleDistP = universals.distance(0.0,0.0,xx,zz)
	#	   [3]{'compAngle'}   [4]{'adjAngle'}       45 deg or 135 deg
			poleAngle = practiceTrials[0,practice_num, 4]
			# cos/sin takes argument in radians
			poleAngleARad = math.radians(poleAngle)
	#	   [1]{'compQuadrant'}   [2]{'adjQuad'}               by plane geometry 1-4
			adjustableSpot = int(practiceTrials[0,practice_num, 2])
			# print 'adjustableSpot', adjustableSpot
			printLoop(trialLoopNum, 360, 'adjustableSpot', adjustableSpot)
			# plane geometry 1:4 subtract 1 to get relevant array value
			xSignA = poleSpots[adjustableSpot-1][0]
			zSignA = poleSpots[adjustableSpot-1][1]
			
#			moving .3m/sec is good for fast speed
			# large increment change
			if controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistP + 0.04 < 24:
						poleDistP = poleDistP + 0.04
				elif yT < -0.6:
					if poleDistP - 0.04 > 1.5:
						poleDistP = poleDistP - 0.04
				# print 'adjustableSpot', adjustableSpot
				printLoop(trialLoopNum, 270,'adjustableSpot', adjustableSpot)
				xPosA = math.sin(poleAngleARad)*poleDistP*xSignA
				zPosA = math.cos(poleAngleARad)*poleDistP*zSignA
				adjustablePolePosition = [xPosA,0,zPosA]
				print('moving to new adjustablePolePosition', adjustablePolePosition)
				# Use a moveTo action to move a node to the point [0,0,25] at X meters per second 
				flyToPoint = vizact.moveTo(adjustablePolePosition, speed=3.6, interpolate=None)
				print('object moving')
				practicePole.addAction(flyToPoint)
			# touch slow	
			elif controller.isButtonDown(4) and not controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistP + 0.02 < 24:
						poleDistP = poleDistP + 0.02
				elif yT < -0.65:
					if poleDistP - 0.02 > 1.5:
						poleDistP = poleDistP - 0.02
				print('adjustableSpot', adjustableSpot)
				xPosA = math.sin(poleAngleARad)*poleDistP*xSignA
				zPosA = math.cos(poleAngleARad)*poleDistP*zSignA
				adjustablePolePosition = [xPosA,0,zPosA]
#				print 'moving to new adjustablePolePosition', adjustablePolePosition
				printLoop(trialLoopNum, 120, 'slowly moving to new adjustablePolePosition', adjustablePolePosition)

				flyToPoint = vizact.moveTo(adjustablePolePosition, speed=1.8, interpolate=None)
				practicePole.addAction(flyToPoint)
			# touchpad is not touched
			elif not controller.isButtonDown(3) and not controller.isButtonDown(4):
				practicePole.clearActionList(pool = 0)
				# print 'object NOT moving'
				printLoop(trialLoopNum, 180, 'object NOT moving', 0)

			if controller.isButtonDown(2):
				trigger = controller.getTrigger()
				print('trigger', trigger)
				if trigger >.75:
					decisionMade = True
					practicePoleComp.visible(viz.OFF)
					practicePole.visible(viz.OFF)
					practicePole.clearActionList(pool = 0)
					# practice_num 0:3 == 4 practice trials
					practice_num = practice_num + 1
					if practice_num == 4 and (time - controllerInstructionPlayed) > controllerInstructionDuration:
						models['viewPlate'].setPosition(0, 0, 0.045)
						trial_stage = 'done_practice_start_experiment'
						print(trial_stage)
					elif practice_num < 4:
						trial_stage = 'practice_controller_setup2'
						print('trial_stage', trial_stage)
						print('practice_num', practice_num)

		if not universals.facing(cur_pos, practicePole.getPosition(), cur_rot[0], THRESHOLD_THETA):
			printLoop(trialLoopNum, 210, 'not looking at pole', controller.isButtonDown(2))
			
################################
#  experiment 	  intsructions #
################################
	if trial_stage == 'done_practice_start_experiment':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)

		beginExperiment.play()
		beginExperimentPlayed = time
		print('instructions playing')
		print('instructions playing')
		print('instructions playing')
		print('instructions playing')
		trial_stage = 'playing_start_experiment'
		print(trial_stage)
			
	if trial_stage == 'playing_start_experiment':
		if (time - beginExperimentPlayed) > beginExperimentDuration:
			trial_stage = 'experiment_instructions'
			print('trial stage', trial_stage)

	if trial_stage == 'experiment_instructions':
		models['welcomeBox'].visible(viz.OFF)
		concrete.visible(viz.ON)
		beach.visible(viz.ON)
		# trial_stage = 'set_comparison'

		# play instruction
		if instructions == 'comparisonGreen':
			print('comparisonGreen')
			print('comparisonGreen')
			print('comparisonGreen')
			print('comparisonGreen')
			# experimentInstructions == turnLeft
		elif instructions == 'comparisonYellow':
			print('comparisonYellow')
			print('comparisonYellow')
			print('comparisonYellow')
			print('comparisonYellow')
			# experimentInstructions == turnRight
		
		experimentInstructions.play()
		experimentInstructionDuration = experimentInstructions.getDuration()
		experimentInstructionPlayed = time
		print('instructions playing')
		print('instructions playing')
		print('instructions playing')
		print('instructions playing')
		trial_stage = 'playing_experiment_instructions'
		print(trial_stage)
			
	if trial_stage == 'playing_experiment_instructions':			
		# let the instruction play for 3 seconds and then have trial 1 appear
		if (time - experimentInstructionPlayed) > 3:
			trial_stage = 'start_at_experiment'
			print('trial stage', trial_stage)

#################################
#  straight to experiment trials #
#################################
	if trial_stage == 'start_at_experiment':

			models['welcomeBox'].visible(viz.OFF)
			concrete.visible(viz.ON)
			beach.visible(viz.ON)
			trial_stage = 'set_comparison'
########################
#  setup  comparision  #
########################
	if trial_stage == 'set_comparison':
		print('Start Trial ' + str(trial_num))
		print('Start Trial ' + str(trial_num))
		trial_start = time
		
		
		#	comparisionObjects, adjustableObjects
		comparisionSize = int(condition[trial_num-1, 9])
		print('comparisionSize',comparisionSize)	
	#		print 'comparisionSize',comparisionSize
		if comparisionSize == 1:
			comparisonPole = comparisonPole1
		elif comparisionSize == 2:
			comparisonPole = comparisonPole2
		elif comparisionSize == 3:
			comparisonPole = comparisonPole3
		elif comparisionSize == 4:
			comparisonPole = comparisonPole4

# [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   
#                         [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
#                         [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
#                         [7]{'compTerrainCode'}    [8]{'AdjustTerrainCode'} 1='firm' 2 ='sand
#						  [9] compsz			[10] adjSz
#                   Matlab doesn't care about the strings condition[:,11:13]
#	   [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   5, 7, 9, 11 m
		poleDist = condition[trial_num-1, 1] # 5, 7, 9, 11 m
#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
		poleAngle = condition[trial_num-1, 3]
		# cos/sin takes argument in radians
		poleAngleRad = math.radians(poleAngle)
#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
#        the sand is on the RIGHT poleSpots = [[1 1], [-1 1], [-1 -1], [1 -1]]
#        the sand is on the LEFT poleSpots = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
		comparisonSpot = int(condition[trial_num-1, 5])
		print('comparisonSpot', comparisonSpot)
		# plane geometry 1:4 subtract 1 to get relevant array value
		xSign = poleSpots[comparisonSpot-1][0]
		zSign = poleSpots[comparisonSpot-1][1]
		xPos = math.sin(poleAngleRad)*poleDist*xSign
		zPos = math.cos(poleAngleRad)*poleDist*zSign
		comparisonPole.setPosition(xPos, 0, zPos)
		poleRot = poleRotations[comparisonSpot-1]
		comparisonPole.setEuler([poleRot,0,0])
#		comparisonPole.visible(viz.ON)
		print('comparision pole location', comparisonPole.getPosition())
		print('comparision pole location', comparisonPole.getPosition())

		trial_stage = 'set_adjustable'
		print(trial_stage)
		
##############################
# setup the adustable object #
############################## 
	elif trial_stage == 'set_adjustable':
		print(trial_stage)
		
		
		adjustableSize = int(condition[trial_num-1, 10])
		if adjustableSize == 1:
			adjustablePole = adjustablePole1
		elif adjustableSize == 2:
			adjustablePole = adjustablePole2
		elif adjustableSize == 3:
			adjustablePole = adjustablePole3
		elif adjustableSize == 4:
			adjustablePole = adjustablePole4
			
#	   [0]{'trialNum'}         [1]{'compPoleDist'}  [2]{'adjPoleStrtPos'}   
		poleDistA = condition[trial_num-1, 2] # 5, 7, 9, 11 m
#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
		poleAngleA = condition[trial_num-1, 4]
		poleAngleARad = math.radians(poleAngleA)
#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
		adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
#		print 'adjustableSpot', adjustableSpot
		printLoop(trialLoopNum, 180,'adjustableSpot', adjustableSpot)
		xSignA = poleSpots[adjustableSpot-1][0]  #-1 to correct for array position
		zSignA = poleSpots[adjustableSpot-1][1]
		
		xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
		zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
		adjustablePole.setPosition(xPosA, 0, zPosA)
		poleRot = poleRotations[adjustableSpot-1]
		adjustablePole.setEuler([poleRot,0,0])
		print('adjustable pole location', adjustablePole.getPosition())
		print('adjustable pole location', adjustablePole.getPosition())
		
		
		trial_stage = 'comparison_adjustable_visible'
		
		adjustablePole.visible(viz.ON)
		comparisonPole.visible(viz.ON)
		adjustablePole.alpha(0)
		comparisonPole.alpha(0)
		appearance_time = time
		print(trial_stage)
		
	elif trial_stage == 'comparison_adjustable_visible':
		if (time - appearance_time)*1.2 < 1:
			models['practiceDisc'].alpha((time - appearance_time)*1.2)
		elif (time - appearance_time)*1.2 >= 1:
			models['practiceDisc'].alpha(1)
			start_response = time
			trial_stage = 'make_response'
			print(trial_stage)
####################################
# move adjustable to make response #
####################################
	elif trial_stage == 'make_response':
		printLoop(trialLoopNum, 210, 'trial number', trial_num)
#		printLoop(trialLoopNum, 90, 'trial number', trial_num)
#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
		poleAngleA = condition[trial_num-1, 4]
		poleAngleARad = math.radians(poleAngleA)
#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
		adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
#		print 'adjustableSpot', adjustableSpot
		xSignA = poleSpots[adjustableSpot-1][0]  #-1 to correct for array position
		zSignA = poleSpots[adjustableSpot-1][1]
		
#		if ~(universals.inRadius(cur_pos,[0, 0, 0] , DISC_TRIGGER_RADIUS)):
#			# add one for every frame that they are outside the box
#			outsideOfViewingBoxCount = outsideOfViewingBoxCount + 1
##			print 'outside of viewing box'
##			print 'outside of viewing box'

		looking(cur_pos, adjustablePole.getPosition(), cur_rot[0])
#		print degBw
		if degBw > 40 or degBw < -40:
			adjustablePole.alpha(0)
		elif degBw < 40 and degBw > 15:
			adjustablePole.alpha((40 - degBw)/25)
		elif degBw > -40 and degBw < -15:
			adjustablePole.alpha((40 + degBw)/25)
		elif degBw < 15 and degBw > -15:
			adjustablePole.alpha(1)
		looking(cur_pos, comparisonPole.getPosition(), cur_rot[0])
		if degBw > 40 or degBw < -40:
			comparisonPole.alpha(0)
		elif degBw < 40 and degBw > 15:
			comparisonPole.alpha((40 - degBw)/25)
		elif degBw > -40 and degBw < -15:
			comparisonPole.alpha((40 + degBw)/25)
		elif degBw < 15 and degBw > -15:
			comparisonPole.alpha(1)
			
			
		if universals.facing(cur_pos, adjustablePole.getPosition(), cur_rot[0], THRESHOLD_THETA):
			# print 'is trigger down', controller.isButtonDown(2)
			printLoop(trialLoopNum, 180, 'is trigger down', controller.isButtonDown(2))

			# print 'is the trackpad pushed down', controller.isButtonDown(3)
			printLoop(trialLoopNum, 180, 'is the trackpad pushed down', controller.isButtonDown(3))

			# print 'is the trackpad touched', controller.isButtonDown(4)
			printLoop(trialLoopNum, 180, 'is the trackpad touched', controller.isButtonDown(4))

			# print 'trackpad', controller.getTrackpad()
			printLoop(trialLoopNum, 180, 'trackpad', controller.getTrackpad())

			xT,yT = controller.getTrackpad()
			# print 'trackpad y', yT
			# print ' '
			printLoop(trialLoopNum, 180, 'trackpad y', yT)

#			if the frame rate is 90 frames per seconds and the pole doesn't need to be moved more than 8m
# 			and the subject could eaisily have 20 seconds per trial, then moving .15m/sec is good for slow speed
#			0.15m/90 is the distance per frame = 0.0017
			# small increment change
			xx,yy,zz = adjustablePole.getPosition()
			poleDistA = universals.distance(0.0,0.0,xx,zz)
			# print 'poleDistA', poleDistA
			printLoop(trialLoopNum, 180, 'poleDistA', poleDistA)

			
#			moving .3m/sec is good for fast speed
#			0.3m/90 is the distance per frame = 0.003
			# large increment change
			if controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistA + 0.04 < 24:
						poleDistA = poleDistA + 0.04
				elif yT < -0.6:
					
					if poleDistA - 0.04 > 1.5:
						poleDistA = poleDistA - 0.04
				#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
				poleAngleA = condition[trial_num-1, 4]
				poleAngleARad = math.radians(poleAngleA)
				#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
				adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
				printLoop(trialLoopNum, 120, 'adjustableSpot', adjustableSpot)
				xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
				zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
				adjustablePolePosition = [xPosA,0,zPosA]
				printLoop(trialLoopNum, 120, 'moving to new adjustablePolePosition', adjustablePolePosition)
				# Use a moveTo action to move a node to the point [0,0,25] at X meters per second 
				flyToPoint = vizact.moveTo(adjustablePolePosition, speed=3.6, interpolate=None)
				printLoop(trialLoopNum, 120, 'object moving fast', 0)
				adjustablePole.addAction(flyToPoint)
			elif controller.isButtonDown(4) and not controller.isButtonDown(3):
				if yT > 0.35:
					if poleDistA + 0.02 < 24:
						poleDistA = poleDistA + 0.02
				elif yT < -0.60:
					if poleDistA - 0.02 > 1.5:
						poleDistA = poleDistA - 0.02
				#	   [3]{'compAngle'}   [4]{'adjAngle'}                 45 deg or 135 deg
				poleAngleA = condition[trial_num-1, 4]
				poleAngleARad = math.radians(poleAngleA)
				#	   [5]{'compQuadrant'}   [6]{'adjQuad'}               by plane geometry 1-4
				adjustableSpot = int(condition[trial_num-1, 6]) # 1:4
#				printLoop(trialLoopNum, 180,'adjustableSpot', adjustableSpot)
				xPosA = math.sin(poleAngleARad)*poleDistA*xSignA
				zPosA = math.cos(poleAngleARad)*poleDistA*zSignA
				adjustablePolePosition = [xPosA,0,zPosA]
				printLoop(trialLoopNum, 180, 'moving to new adjustablePolePosition', adjustablePolePosition)
				printLoop(trialLoopNum, 120, 'object moving slow', 0)
				flyToPoint = vizact.moveTo(adjustablePolePosition, speed=1.8, interpolate=None)
				adjustablePole.addAction(flyToPoint)
			# touchpad is not touched
			elif not controller.isButtonDown(3) and not controller.isButtonDown(4):
				adjustablePole.clearActionList(pool = 0)
				# print 'object NOT moving'
				printLoop(trialLoopNum, 180, 'object NOT moving', 0)
#			chaeck that they have moved the adjustable pole
			if controller.isButtonDown(2) and abs(poleDistA - condition[trial_num-1, 2])> 0.05:
				trigger = controller.getTrigger()
				print('trigger', trigger)
				if (time - start_response) > .25:
					if trigger >.75:
						decisionMade = True
						print('decision', decisionMade)
						adjustablePole.clearActionList()
						xx,yy,zz = adjustablePole.getPosition()
						poleDistA = universals.distance(0.0,0.0,xx,zz)
			printLoop(trialLoopNum, 180, 'decision', decisionMade)
			printLoop(trialLoopNum, 180, 'pole distance', poleDistA)

		if decisionMade: # they have aqueezed the trigger more than half way
			# Position: Target_x, Target_y, Participant_x, Participant_y, time stamp
#			data = [target_loc[0],target_loc[2],cur_pos[0], cur_pos[2], cur_rot[0], cur_rot[1], cur_rot[2]]
			xx,yy,zz = adjustablePole.getPosition()
			adjustablePolePosition = [xx,zz]
			# firmSandOrder = viz.input('Is the sand to the right: 1 for yes, 0 for no','')
			strPolePos = [str(round(t,4)) for t in adjustablePolePosition+[poleDistA]+[trial_num]+[firmSandOrder]+[subject] + [time - trial_start]]
			strPolePos = ','.join(strPolePos)+'\n'
			data_batch_polePos = data_batch_polePos + strPolePos

			print('participant has made final decision')
			print(strPolePos)
			print(data_batch_polePos)
			end_time = time
			trial_stage = 'endtrial'
			print('trial_stage', trial_stage)
##################################################################
# End Trial: Close out the trial and reset values for next trial #
##################################################################
	elif trial_stage == 'endtrial':
		if time - end_time > .5:
			print('End Trial ' + str(trial_num))
			print(' ')
			comparisonPole.visible(viz.OFF)
			adjustablePole.visible(viz.OFF)
			# Returns to Stage 1, resets clock
			trial_num = trial_num + 1
			time = 0
			trialLoopNum = 0
			decisionMade = False
			# make True in the interactive bar to write file
			# emergencyStop = True
			# emergencyStop = True
			# emergencyStop = True
			if trial_num > TOTAL_TRIALS or emergencyStop:
				if DATA_COLLECT:
					print('writing file')
					fileName = working_dir + '/' + subjectFile + 'adjustablePoleResponses.csv'
					file = open(fileName, 'a')
					file.write(data_batch_polePos)
					file.close()
				viz.quit()
			elif trial_num < (TOTAL_TRIALS+1):
	# outsideOfViewingBox = False #make True in the interactive bar to play reminder
	# outsideOfViewingBox = True
	# outsideOfViewingBox = True
	# outsideOfViewingBox = True
				if outsideOfViewingBox:
					outsideOfViewingBox = False
					stayInViewingBox.play()

					print('stayInViewingBox')
					print('stayInViewingBox')
					print('stayInViewingBox')
					print('stayInViewingBox')
					trial_stage = 'set_comparison'

				trial_stage = 'set_comparison'



#	in the interactive bar: (end_practice_time - time) to get how long the experiment has been going for
# print (time - end_practice_time)



viz.callback(viz.TIMER_EVENT,masterLoop)
viz.starttimer(0,1/90,viz.FOREVER)
