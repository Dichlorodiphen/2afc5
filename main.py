import viz
import vizact
import vizshape
import vizmat
import os

def generateTerrain():
	# Sky
	viz.clearcolor(0, 0.4, 1.0)

	# Make concrete surface
	WALL_SCALE = [200, 400, 1]
	concrete = viz.addTexQuad()
	concrete.setPosition([-100, 0.148,0])
	concrete.setEuler([0,90,0])
	concrete.setScale(WALL_SCALE)
	
	# Concrete texture
	C = 1
	TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C*.8, WALL_SCALE[2]]
	matrix = vizmat.Transform()
	matrix.setScale(TEXT_SCALE)
	concrete.texmat(matrix )
	concreteImage = viz.addTexture('./textures/concrete2.jpg')
	concreteImage.wrap(viz.WRAP_T, viz.MIRROR)
	concreteImage.wrap(viz.WRAP_S, viz.REPEAT)
	concrete.texture(concreteImage)
	
	# Make sand surface
	WALL_SCALE = [200, 400, 1]
	beach = viz.addTexQuad()
	beach.setPosition( [100, 0.148,0] )
	beach.setEuler([0,90,0])
	beach.setScale(WALL_SCALE)
	
	# Sand texture
	C = 5
	TEXT_SCALE = [WALL_SCALE[0]/C, WALL_SCALE[1]/C, WALL_SCALE[2]]
	matrix = vizmat.Transform()
	matrix.setScale(TEXT_SCALE)
	beach.texmat( matrix )
	sand = viz.addTexture('./textures/sand.jpg')
	sand.wrap(viz.WRAP_T, viz.MIRROR)
	sand.wrap(viz.WRAP_S, viz.REPEAT)
	beach.texture(sand)
	

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
	
	# LOAD MODELS/TEXTURES
	generateTerrain()


if __name__ == "__main__":
	main()