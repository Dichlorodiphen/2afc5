import viz
import vizact
import vizshape
import vizmat
import viztask
import os
from enum import Enum
import random
import time


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
	
	
class Experiment:
	"""A class that encapsulates an experiment and its adaptive staircase."""	
	def __init__(self, terrain, standard_position, distance, quest):
		self.terrain = terrain
		self.standard_position = standard_position
		self.distance = distance 
		self.quest = quest
		
	
	def hasNext(self):
		"""Returns whether or not the current experiment is unfinished."""
		return True
		
		
	def run(self):
		pass

def generateTerrainAndObjects():
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
	
	# Generate objects
	POLE_HEIGHT = 1.3
	POLE_RADIUS = 0.35
	
	## Textures
	blue_texture = viz.addTexture('./textures/blue_granite.jpg')
	blue_texture.wrap(viz.WRAP_T, viz.REPEAT)
	blue_texture.wrap(viz.WRAP_S, viz.REPEAT)
	red_texture = viz.addTexture('./textures/red_granite.jpg')
	red_texture.wrap(viz.WRAP_T, viz.REPEAT)
	red_texture.wrap(viz.WRAP_S, viz.REPEAT)
	
	## Generate blue standard and comparison poles
	blue_standard_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
	blue_comparison_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
	blue_standard_pole.texture(blue_texture)
	blue_comparison_pole.texture(blue_texture)
	
	### Generate red pole
	#adjustable_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
	#adjustable_pole.texture(red_texture)
	
	## Set pole positions
	blue_standard_pole.setPosition(2, 1, 5)
	blue_comparison_pole.setPosition(-2, 1, 5)
	
	## Generate star
	star = viz.add('./models/star/scene.gltf')
	star.setPosition(0, 10, 20)
	
	
def runExperiments():
	"""Run each experiment until all are finished."""
	# Initialize QUEST+
	
	# Initialize experiments
	experiments = []
	distances = [7, 9, 11]
	count = 0
	for i in range(0, 2):
		for terrain in Terrain:
			for standard_position in Position:
				for distance in distances:
					quest = count ## TODO: change this
					count += 1
					current = Experiment(terrain, standard_position, distance, quest)
					experiments.append(current)
	
	done = False
	while (not done):
		yield viztask.waitTime(1)
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
	
	# Load models / textures
	generateTerrainAndObjects()
	
	# Proceed until all staircases exhausted
	experiment_runner = viztask.schedule(runExperiments())


if __name__ == "__main__":
	main()