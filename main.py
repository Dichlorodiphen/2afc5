import viz
import vizact
import vizshape
import vizmat
import viztask
import os
from enum import Enum
import random
import time
import questplus as qp
import numpy as np
import warnings
import csv


class Terrain(Enum):
	"""An enum to describe the terrain conditions."""
	SAND_FIRM = 0
	SAND_SAND = 1
	FIRM_FIRM = 2
	FIRM_SAND = 3
	
	
class Position(Enum):
	"""An enum to describe the side the standard pole is on."""
	LEFT = 0
	RIGHT = 1
	
	
STAR_HEIGHT = 10

# xyz coordinates for star positions
STAR_POSITIONS = dict([
	(Terrain.SAND_FIRM, [0, STAR_HEIGHT, -20]),
	(Terrain.SAND_SAND, [20, STAR_HEIGHT, 0]),
	(Terrain.FIRM_FIRM, [-20, STAR_HEIGHT, 0]),
	(Terrain.FIRM_SAND, [0, STAR_HEIGHT, 20])
])

# quaternions for orientation of star
STAR_ORIENTATIONS = dict([
	(Terrain.SAND_FIRM, [0, 1, 0, 0]),
	(Terrain.SAND_SAND, [0, 1, 0, 1]),
	(Terrain.FIRM_FIRM, [0, 1, 0, 1]),
	(Terrain.FIRM_SAND, [0, 1, 0, 0])
])

RIGHT_ROTATIONS = dict([
	(Terrain.SAND_FIRM, 210),
	(Terrain.SAND_SAND, 120),
	(Terrain.FIRM_FIRM, 300),
	(Terrain.FIRM_SAND, 30)
])

LEFT_ROTATIONS = dict([
	(Terrain.SAND_FIRM, 150),
	(Terrain.SAND_SAND, 60),
	(Terrain.FIRM_FIRM, 240),
	(Terrain.FIRM_SAND, -30)
])
	
	
class Experiment:
	"""A class that encapsulates an experiment and its adaptive staircase."""	
	def __init__(self, id, terrain, standard_position, distance, quest, log):
		self.id = id
		self.terrain = terrain
		self.standard_position = standard_position
		self.distance = distance 
		self.quest = quest
		self.trials = 5
		self.star = None
		self.standard_pole = None
		self.comparison_pole = None
		self.log = log
		
		
	def setup(self, stimulus):
		"""Sets up the scene with the comparison pole at the specified distance."""
		# Display star
		self.star = viz.add('./models/star/scene.gltf')
		self.star.setPosition(STAR_POSITIONS[self.terrain])
		self.star.setQuat(STAR_ORIENTATIONS[self.terrain])
		
		# Display poles
		POLE_HEIGHT = 1.3
		POLE_RADIUS = 0.35
		blue_texture = viz.addTexture('./textures/blue_granite.jpg')
		blue_texture.wrap(viz.WRAP_T, viz.REPEAT)
		blue_texture.wrap(viz.WRAP_S, viz.REPEAT)
		self.standard_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
		self.comparison_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
		self.standard_pole.texture(blue_texture)
		self.comparison_pole.texture(blue_texture)
		
		self.standard_pole.setPosition(0, 1, self.distance)
		self.standard_pole.setCenter(0, -1, -1 * self.distance)
		self.comparison_pole.setPosition(0, 1, stimulus)
		self.comparison_pole.setCenter(0, -1, -1 * stimulus)
		
		if (self.standard_position == Position.LEFT):
			print("POSITION LEFT")
			self.standard_pole.setAxisAngle(0, 1, 0, LEFT_ROTATIONS[self.terrain])
			self.comparison_pole.setAxisAngle(0, 1, 0, RIGHT_ROTATIONS[self.terrain])
		else:
			print("POSITION RIGHT")
			self.standard_pole.setAxisAngle(0, 1, 0, RIGHT_ROTATIONS[self.terrain])
			self.comparison_pole.setAxisAngle(0, 1, 0, LEFT_ROTATIONS[self.terrain])
		
		
	def teardown(self):
		"""Clean up all objects associated with a run of experiment."""
		self.star.remove()
		self.standard_pole.remove()
		self.comparison_pole.remove()
		
	
	def hasNext(self):
		"""Returns whether or not the current experiment is unfinished."""
		return not (self.trials <= 0)
		
	
	def next(self):
		"""Returns the next stimulus."""
		return self.quest.next_stim
		
		
	def update(self, stimulus, outcome):
		"""Update the staircase with a stimulus-response pair."""
		self.trials -= 1
		self.quest.update(stim=stimulus, outcome=outcome)
		self.log.writerow([self.id, self.trials, stimulus, outcome, self.estimate()])
		
	
	def estimate(self):
		"""Returns the final parameter estimates."""
		return self.quest.param_estimate
		

def generateTerrain():
	# Sky
	viz.clearcolor(0, 0.4, 1.0)

	# Make concrete surface
	WALL_SCALE_CONCRETE = [200, 400, 1]
	concrete = viz.addTexQuad()
	concrete.setPosition([-100, 0.148,0])
	concrete.setEuler([0,90,0])
	concrete.setScale(WALL_SCALE_CONCRETE)
	
	# Concrete texture
	C_CONCRETE = 1
	TEXT_SCALE_CONCRETE = [
		WALL_SCALE_CONCRETE[0]/C_CONCRETE,
		WALL_SCALE_CONCRETE[1]/C_CONCRETE*.8,
		WALL_SCALE_CONCRETE[2]
	]
	matrix = vizmat.Transform()
	matrix.setScale(TEXT_SCALE_CONCRETE)
	concrete.texmat(matrix)
	concrete_texture = viz.addTexture('./textures/concrete2.jpg')
	concrete_texture.wrap(viz.WRAP_T, viz.MIRROR)
	concrete_texture.wrap(viz.WRAP_S, viz.REPEAT)
	concrete.texture(concrete_texture)
	
	# Make sand surface
	WALL_SCALE_SAND = [200, 400, 1]
	beach = viz.addTexQuad()
	beach.setPosition( [100, 0.148,0] )
	beach.setEuler([0,90,0])
	beach.setScale(WALL_SCALE_SAND)
	
	# Sand texture
	C_SAND = 5
	TEXT_SCALE_SAND = [
		WALL_SCALE_SAND[0]/C_SAND,
		WALL_SCALE_SAND[1]/C_SAND,
		WALL_SCALE_SAND[2]
	]
	matrix = vizmat.Transform()
	matrix.setScale(TEXT_SCALE_SAND)
	beach.texmat(matrix)
	sand = viz.addTexture('./textures/sand.jpg')
	sand.wrap(viz.WRAP_T, viz.MIRROR)
	sand.wrap(viz.WRAP_S, viz.REPEAT)
	beach.texture(sand)
	
	
def initQuest(standard_position, distance) -> qp.QuestPlus:
	"""Initialize and return a QuestPlus staircase."""
	# Stimulus domain
	lower_bound = distance / 2 - 1
	upper_bound = distance * 2 + 1
	distances = np.arange(start=lower_bound, stop=upper_bound, step=0.01)
	stim_domain = dict(intensity=distances)
	
	# Parameter domain
	thresholds = distances.copy() # threshold (free parameter)
	slope = 1 # slope (fixed parameter)
	guess_rate = 0.5 # guess rate (fixed parameter)
	lapse_rate = 0.01 # lapse rate (fixed parameter)
	param_domain = dict(threshold=thresholds,
		slope=slope,
		lower_asymptote=guess_rate,
		lapse_rate=lapse_rate)
	
	# Response domain
	if (standard_position == Position.LEFT):
		responses = [Position.LEFT, Position.RIGHT]
	else:
		responses = [Position.RIGHT, Position.LEFT]
	outcome_domain = dict(response=responses)
	
	# Misc parameters
	func = 'weibull'
	stim_scale = 'log10'
	stim_selection_method = 'min_entropy'
	param_estimation_method = 'mean'
	
	# Init staircase
	staircase = qp.QuestPlus(stim_domain=stim_domain,
		func=func,
		stim_scale=stim_scale,
		param_domain=param_domain,
		outcome_domain=outcome_domain,
		stim_selection_method=stim_selection_method,
		param_estimation_method=param_estimation_method)
	
	return staircase
	
	
def runExperiments(log, csvfile):
	"""Run each experiment until all are finished."""
	# Initialize experiments
	experiments = []
	distances = [7, 9, 11]
	id = 0
	for i in range(0, 2):
		for terrain in Terrain:
			for standard_position in Position:
				for distance in distances:
					quest = initQuest(standard_position, distance)
					current = Experiment(id, terrain, standard_position, distance, quest, log)
					id += 1
					experiments.append(current)
	
	done = False
	while (not done):
		# Check if all staircases exhausted
		done = True
		for e in experiments:
			if (e.hasNext()):
				done = False
				break
		if (done):
			break
				
		# Randomly select an experiment
		# TODO: can we just remove from experiments to improve
		# runtime?
		experiment = experiments[random.randint(0, len(experiments) - 1)]
		while (not experiment.hasNext()):
			experiment = experiments[random.randint(0, len(experiments) - 1)]
		
		# Perform experiment
		stimulus = experiment.next()
		experiment.setup(stimulus["intensity"])
		
		# Handle keypresses (wait for s, d, or q)
		yield viztask.waitKeyDown(('s', 'd', 'q'))
		outcome = None
		if (viz.key.isDown('s')):
			outcome = Position.LEFT
		elif (viz.key.isDown('d')):
			outcome = Position.RIGHT
		elif (viz.key.isDown('q')):
			# TODO: handle quit key
			print(experiment.distance)
			print(experiment.estimate())
			print("should exit here")
			break
		print(np.var(experiment.quest.marginal_posterior["threshold"]))
			
		experiment.update(stimulus, dict(response=outcome))
		
		experiment.teardown()
		
	csvfile.close()
		
		
def handleViewIntersection():
	pass


def main():
	# Start rendering
	viz.MainWindow.fov(60)
	viz.setMultiSample(4)
	viz.MainView.collision(viz.ON)
	viz.go()

	# Ignore xarray deprecation warnings
	warnings.filterwarnings("ignore", category=DeprecationWarning)

	# Get subject info
	subject_number = viz.input("Please enter the subject number (0 for testing):")
	print(subject_number)
	subject_filename = str(subject_number) + "_data.csv"
	data_directory = "data"
	
	# Create data directory if it does not exist
	if (not os.path.exists(data_directory)):
		os.makedirs(data_directory)
	
	# CSV logic
	csvfile = open(data_directory + os.path.sep + subject_filename, 'w', newline='')
	
	log = csv.writer(csvfile)
	
	# Load terrain
	generateTerrain()
	
	# Viewpoint intersection handler0
	
	#intersection_handler = viztask.schedule(handleViewIntersection())
	
	# Proceed until all staircases exhausted
	experiment_runner = viztask.schedule(runExperiments(log, csvfile))


if __name__ == "__main__":
	main()