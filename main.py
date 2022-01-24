import viz
import vizact
import vizshape
import vizmat
import os

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
	comp_texture = viz.addTexture('./textures/stone.jpg')
	adj_texture = viz.addTexture('./textures/stone2.jpg')
	
	## Comparison pole
	comp_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
	comp_texture.wrap(viz.WRAP_T, viz.REPEAT)
	comp_texture.wrap(viz.WRAP_S, viz.REPEAT)
	comp_pole.texture(comp_texture)
	
	## Adjustable pole
	adjustable_pole = vizshape.addCylinder(POLE_HEIGHT, POLE_RADIUS)
	adj_texture.wrap(viz.WRAP_T, viz.REPEAT)
	adj_texture.wrap(viz.WRAP_S, viz.REPEAT)
	adjustable_pole.texture(adj_texture)
	
	adjustable_pole.setPosition(2, 1, 5)
	comp_pole.setPosition(-2, 1, 5)


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


if __name__ == "__main__":
	main()