import math
from decimal import Decimal, ROUND_HALF_UP

DELIM = ';'

#This method takes in 4 values repesenting two point (x,y) and (a,b) and returns the distance between the points on a cartesian plane
def distance(x,y,a,b):
	return ((x-a)**2+(y-b)**2)**.5

def distanceLocs(loc1, loc2):
	return distance(loc1[0],loc1[2],loc2[0],loc2[2])

#This method takes in two poadsitions in [x,y,z] form and then returns true if the distance between them is less than the radius given
def inRadius(pos, center, radius):
	if pos == '' or center == '' or radius == '':
		return False
	return (distance(pos[0],pos[2],center[0],center[2]) <= radius)
	
# return the scaled vector
def scaleVector(vec, scale):
	return [scale*x for x in vec]

# return the dot product of two vectors
def dotProduct(u, v):
	assert len(u) == len(v)
	return sum([u[i]*v[i] for i in range(len(u))])

# return the magnitude of the given vector
def vectorMagnitude(u):
	return dotProduct(u,u)**.5	

# return the normalized vector
def getNormalized(vec):
	mag = vectorMagnitude(vec)
	if mag:
		return [x/mag for x in vec]
	else:
		print('vector has zero-magnitude')
		return vec

# return u + v
def vectorAdd(u, v):
	assert len(u) == len(v)
	return [u[i]+v[i] for i in range(len(u))]

# return u - v
def vectorSubtract(u, v):
	assert len(u) == len(v)
	return [u[i]-v[i] for i in range(len(u))]

# return the reflection of u across v (u and v point originate at the same point)
def vectorReflect(u,v):
	# normalize line of reflection vector
	v = [x/vectorMagnitude(v) for x in v]
	u_dot_v = dotProduct(u,v)
	return vectorSubtract([2*u_dot_v*x for x in v], u)

# returns the perpendicular distance from a given point to a vector, 
# also returns True if the perpendicular intersection is outside the length of the given vector (treated as a line segment)
# based on A(dot)B = ||A|*||B||*cos(theta)
def perpDistanceToVector(point, vector, vector_origin):
	# make sure all vectors have the same dimensionality
	assert len(point) == len(vector) and len(point) == len(vector_origin)
	assert vectorMagnitude(vector) > 0
	B = vector # vector from vector_origin
	A = [point[i]-vector_origin[i] for i in range(len(point))] # to point from vector_origin
	A_dot_B = dotProduct(A, B)
	perp_distance = (dotProduct(A,A) - ((A_dot_B**2)/dotProduct(B,B)))**.5 # D^2 = (||A||^2 - (A(dot)B/||B||)^2)
	parallel_distance = A_dot_B/(vectorMagnitude(B))
	return perp_distance, parallel_distance > vectorMagnitude(B) or parallel_distance < 0

# returns true if 'position' is within 'threshold' distance (m) of 'path,' false otherwise, also returns closest_index
# position is a 3-element coordinate list ie. [x,y,z], path is a list of coordinate lists
# close_loop is a bool that designates if the first and last elements of the path are connected
def checkPathProximity(position, path, threshold, close_loop):
	
	closest_dist = 1000000
	closest_index = 0
	#find the index of the closest node
	for i in range(len(path)):
		temp_dist = distanceLocs(path[i], position)
		if temp_dist < closest_dist:
			closest_dist = temp_dist
			closest_index = i
	
	# if the position is within the threshold distance of a path node
	if closest_dist <= threshold:
		return True, closest_index
		
	else: # find perpendicular distance to line between closest node and each of its neighbors, if line exists
		next_index = (closest_index+1)%len(path)
		previous_index = (closest_index-1)%len(path)	

		# set default perpendicular distance values
		perp_closest_next = -1
		perp_closest_previous = -1

		# get perpendicular distance between position and vector between closest and next
		if close_loop or closest_index != len(path)-1:
			closest_to_next = vectorSubtract(path[next_index], path[closest_index])
			temp_dist, invalid = perpDistanceToVector(position, closest_to_next, path[closest_index])
			if not invalid:
				perp_closest_next = temp_dist
		
		# get perpendicular distance between position and vector between closest and previous
		if close_loop or closest_index != 0:
			closest_to_previous = vectorSubtract(path[previous_index], path[closest_index])
			temp_dist, invalid = perpDistanceToVector(position, closest_to_previous, path[closest_index])
			if not invalid:
				perp_closest_previous = temp_dist
		
		# if either perpendicular distance is within the threshold
		if (perp_closest_next >= 0 and perp_closest_next < threshold) \
		or (perp_closest_previous >= 0 and perp_closest_previous < threshold):
			return True, closest_index
		else:
			return False, closest_index
		

def make_file_path(filePath):
	"""Take a file path string (e.g. 'A/B/C.txt'), generate the path to that file.
	"""
	filePath = filePath.replace('\\','/')
	dirsAndFile = filePath.split('/')
	dirs = filePath[:-1]
	dirPath = '/'.join(dirs)
	mkDirPath(dirPath)

def make_dir_path(dirPath):
	"""Take a directory path string (e.g. 'A/B/C/' (or 'A/B/C')), generate the path to that directory.
	"""
	import os
	filePath = dirPath.replace('\\','/')
	dirs = dirPath.split('/')
	tempPath = ''
	for dir in dirs:
		tempPath += dir + '/'
		try:
			os.mkdir(tempPath)
		except:
			pass

def facing(lookingObjectPosn, lookedAtObjectPosn, lookingObjectYaw, thresholdTheta):
	"""lookingObjectPosn: position of object that is looking
	lookedAtObjectPosn: position of object looked at
	lookingObjectYaw: yaw of the object that is looking (degrees)
	thresholdTheta: viewing angle must be +/- this amount in order to be considered 'looking at' the object. degrees

	return: bool, whether the looking object is facing the looked-at object
	>>> universals.facing([0,0,0],[1,0,5],0,20)
	True
	>>> universals.facing([3,0,3],[1,0,0],210,20)
	True
	"""
	degRelOrientation = 180.0/math.pi*relativeOrientation(lookingObjectPosn, lookedAtObjectPosn) #radians
	degRelOrientation = (degRelOrientation+180)%360-180
	return math.fabs(degRelOrientation-lookingObjectYaw)<thresholdTheta

#This helper method will round the inputed val to the 4th decimal place and return the value as a string
#def round(val):
#	return float(Decimal(str(val)).quantize(Decimal(".0001"),ROUND_HALF_UP))

#This method takes in the path to the file name, the array of data to be recorded, and the timestamp of the data to be recorded
#It then appends to the file the data array truncated to 4 decimal places and the timestamp also to 4 decimal places
def writeArrayFile(fileName, data, time):
	toWrite = []
	for t in data:
		toWrite.append(round(t,4))
	file = open(fileName, 'a')
	file.write(str(toWrite)+' '+str(round(time,4))+'\n')
	
def writeCSVFile(fileName, data, time):
	strData = [str(round(t,4)) for t in data+[time]]
	file = open(fileName, 'a')
	file.write(DELIM.join(strData)+'\n')
	file.close()

def writeCSVFile_header(fileName, data, time): #Adds a header to the csv file
	strData = [str(round(t,4)) for t in data+[time]]
	file = open(fileName, 'a')
	#file.writelines ('test' + '\n')
	file.write(DELIM.join(strData)+'\n')
	file.close()

	
def writeCSVFile2(fileName, *args):
	strData = [str(t) for t in args]
	file = open(fileName, 'a')
	file.write(DELIM.join(strData)+'\n')
	file.close()

#Takes a positon in [x,y,z] from and rotates the position in the xz plane by degrees degrees
#so the position [1,0,0] rotated 90 would return [0,0,1]
def rotate(position, degrees):
	d = distanceLocs([0, 0, 0], position)
	theta = math.atan2(position[2], position[0])
	thetaNew = (theta + degrees*math.pi/180.0)
	positionNew = [d * math.cos(thetaNew), position[1], d * math.sin(thetaNew)]
	return positionNew
	
#Takes in two positions and returns the relative orientation of pos2 from pos1 (aka the theta of pos2 assuming pos1 is the origin)
def relativeOrientation(pos1, pos2):
	xrel = round(pos2[0]-pos1[0],4)
	zrel = round(pos2[2]-pos1[2],4)
	theta = 0
	if zrel == 0.0 and xrel > 0:
		theta = math.pi/2
	elif zrel == 0.0:
		theta = math.pi/2*3
	else:
		theta = math.atan(round(xrel,4)/round(zrel,4))
		if zrel < 0:
			theta += math.pi
		if zrel > 0 and xrel < 0:
			theta += math.pi*2
	return theta

#takes a val in radians and returns its degree equivalent
def radToDeg(val):
	return val*(180.0/math.pi)

#takes a val in degrees and returns its radian equivalent
def degToRad(val):
	return val*(math.pi/180.0)

def slope(y1, y2, x1, x2):
	if (x1 - x2 == 0.0):
		return 9999
	else:
		return (y1 - y2)/(x1 - x2)

def project_vector(p1, p2, dist):
	projection_vector = [b-a for a, b in zip(p1, p2)]
	norm_pv = sum([t**2 for t in projection_vector])**0.5
	projected_vector = [dist*t/norm_pv for t in projection_vector]
	return projected_vector	

def project_point(p1, p2, dist):
	dist_pv = project_vector(p1, p2, dist)
	projected_point = [a+b for a, b in zip(p1, dist_pv)]
	return projected_point	
	 
def between(e1, e2, val):
	if e1 > e2:
		return between (e2, e1, val)
	else:
		return ((e1 <= val) and (e2 >= val))

def make_experiment_data_file(file_path, trial_list, file_name = 'trials.txt', practice_trial_list = []):
	file_path = file_path.strip('/')
	file_name = file_name.strip('/')
	if file_name.find('.')==-1:
		file_name = file_name+'.txt'
	output_file_path = '/'.join([file_path,file_name])
	f = open(output_file_path,'w')
	f.write('File Path\n')
	f.write(output_file_path+'\n')
	f.write('Practice Trials\n')
	f.write(str(practice_trial_list)+'\n')
	f.write('Real Trials\n')
	f.write(str(trial_list)+'\n')
	f.flush()
	f.close()

def make_trial_file(file_name, trial_list, key_order):
	f = open(file_name,'w')
	print('Writing',len(trial_list),'trials to',file_name)
	f.write(str(len(trial_list))+'\n')
	for k in key_order:
		f.write(k+DELIM)
	f.write('\n')
	for t in trial_list:
		for k in key_order:
			if k in t:
				f.write(str(t[k])+DELIM)
				del t[k]
			else:
				f.write(DELIM)
		if t:
			print('Warning! Not saving information from trial:',t)
		f.write('\n')
	f.flush()
	f.close()

def read_trial_file(file_name):
	f = open(file_name)
	nt = int(f.readline().strip(DELIM+' \n'))
	print('Reading',nt,'trials from',file_name)
	t = [{} for z in range(nt)]
	keys = f.readline().strip(DELIM+' \n').split(DELIM)
	nk = len(keys)
	i=0
	while i<nt:
		l = f.readline().strip(DELIM+' \n').split(DELIM)
		for j in range(nk):
			d = eval(l[j])
			t[i][keys[j]] = eval(l[j])
		i+=1
	f.close()
	return t

def open_experiment_data_file(file_path):
	inputInfo = open(file_path)
	lineNum=0
	for l in inputInfo:
		if lineNum==0 and l.startswith('File Path'):
			lineNum+=1
		elif lineNum==2 and l.startswith('Practice Trials'):
			lineNum+=1
		elif lineNum==4 and l.startswith('Real Trials'):
			lineNum+=1
		elif lineNum==1:
			path=l.rstrip()
			lineNum+=1
		elif lineNum==3:
			practiceTrialList=eval(l)
			lineNum+=1
		elif lineNum==5:
			trialList=eval(l)
			break
	return trialList, practiceTrialList

if __name__=='__main__':
	print('Running universals.py unit tests.')
	print([0, 0, 3],project_point([0, 0, 0], [0, 0, 5], 3))
	print([2, 0, 0],project_point([5, 0, 0], [0, 0, 0], 3))
	print([2, 0, -2],project_point([-2, 0, 1], [2, 0, -2], 5))
	
	print('\nvector operations unit tests')
	print([-1,-4,-9], vectorSubtract([1, 0, -1],[2, 4, 8]))
	print([3,5,7], vectorSubtract([3,4,5],[0,-1,-2]))
	
	print(12, dotProduct([1,1,1],[3,4,5]))
	print(26, dotProduct([-1,4,0],[2,7,-3]))
	
	print([-1,0,1], vectorReflect([1,0,1],[0,0,-1]))
	
	print('\nperpDistanceToVector unit tests')
	print('(3,True)', perpDistanceToVector([-1,0,3],[4,0,0],[0,0,0]))
	print('(4,True)', perpDistanceToVector([5,0,-4],[4,0,0],[0,0,0]))
	print('(0,False)', perpDistanceToVector([2,0,0],[4,0,0],[0,0,0]))

	print('\ncheckPathProximity unit tests')
	temp_path = [[1,0,1],[1,0,8],[8,0,12],[15,0,1]]
	print(True, checkPathProximity([10,0,2],temp_path, 2, True))
	print(False, checkPathProximity([10,0,2],temp_path, 2, False))
	print(False, checkPathProximity([10,0,3],temp_path, 2, True))
	
	temp_path = [[1,0,1],[1,0,8],[8,0,12],[15,0,1],[1,0,1]]
	print(True, checkPathProximity([2,0,0],temp_path, 2, True))
	print(True, checkPathProximity([2,0,0],temp_path, 2, False))