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


POLE_HEIGHT = 1
	
STANDARD_POSITIONS = dict([
	(Terrain.SAND_FIRM, [2, POLE_HEIGHT, -5]),
	(Terrain.SAND_SAND, [5, POLE_HEIGHT, 2]),
	(Terrain.FIRM_FIRM, [-5, POLE_HEIGHT, 2]),
	(Terrain.FIRM_SAND, [2, POLE_HEIGHT, 5])
])

COMPARISON_POSITIONS = dict([
	(Terrain.SAND_FIRM, [-2, POLE_HEIGHT, -5]),
	(Terrain.SAND_SAND, [5, POLE_HEIGHT, -2]),
	(Terrain.FIRM_FIRM, [-5, POLE_HEIGHT, -2]),
	(Terrain.FIRM_SAND, [-2, POLE_HEIGHT, 5])
])
	
	
class Experiment:
	"""A class that encapsulates an experiment and its adaptive staircase."""	
	def __init__(self, terrain, standard_position, distance, quest):
		self.terrain = terrain
		self.standard_position = standard_position
		self.distance = distance 
		self.quest = quest
		self.trials = 5
		self.star = None
		self.comparison_pole = None
		self.standard_pole = None
		
		
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
		self.standard_pole.setPosition(STANDARD_POSITIONS[self.terrain])
		self.comparison_pole.setPosition(COMPARISON_POSITIONS[self.terrain])
		
		
	def teardown(self):
		"""Clean up all objects associated with a run of experiment."""
		self.star.remove()
		self.comparison_pole.remove()
		self.standard_pole.remove()
		
	
	def hasNext(self):
		"""Returns whether or not the current experiment is unfinished."""
		return not (self.trials <= 0)
		
	
	def next(self):
		"""Returns the next stimulus."""
		print(self.quest.marginal_posterior)
		return self.quest.next_stim
		
		
	def update(self, stimulus, outcome):
		"""Update the staircase with a stimulus-response pair."""
		self.trials -= 1
		q.update(stim=stimulus, outcome=outcome)
		
	
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
	
	
def initQuest() -> qp.QuestPlus:
	"""Initialize and return a QuestPlus staircase."""
	# Stimulus domain
	distances = np.arange(start=3, stop=15, step=0.05)
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
	responses = [Position.LEFT, Position.RIGHT]
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
	
	
def runExperiments():
	"""Run each experiment until all are finished."""
	# Initialize experiments
	experiments = []
	distances = [7, 9, 11]
	for i in range(0, 2):
		for terrain in Terrain:
			for standard_position in Position:
				for distance in distances:
					quest = initQuest()
					current = Experiment(terrain, standard_position, distance, quest)
					experiments.append(current)
	
	done = False
	while (not done):
		yield viztask.waitTime(4)
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
		experiment.setup(1)
		yield viztask.waitTime(3)
		experiment.teardown()
		print(experiment.quest)


def main():
	# Start rendering
	viz.MainWindow.fov(60)
	viz.setMultiSample(4)
	viz.MainView.collision(viz.ON)
	viz.go()

	"""
	# Get subject info
	subject_number = viz.input("Please enter the subject number (0 for testing):")
	print(subject_number)
	subject_filename = str(subject_number) + "_data.txt"
	data_directory = os.getcwd() + os.sep + "data"

	content = viz.input("Type content")

	more_content = viz.input("Type more content")

	# Create file
	file = open(subject_filename, "w")
	file.write(content + "\n")
	file.write(more_content)
	file.close()
	"""
	
	# Load terrain
	generateTerrain()
	
	# Proceed until all staircases exhausted
	experiment_runner = viztask.schedule(runExperiments())


if __name__ == "__main__":
	main()