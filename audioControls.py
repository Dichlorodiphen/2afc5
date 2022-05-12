### Audio Helper Methods ###
#This script is a set of the two basic audioControl methods that are run most frequently in VENLab experiments
#The script should be imported at the top of any code that wishes to make use of them
#The purpose of having these methods instead of the traditional .play() calls on audio files
#Is that these allow you to queue up audio to be played in order making overlapping instructions a thing of the past
#and allowing instructions to be more customized to the individual experiment 
#(ie 'go to the well', and 'find the well') can have the same 'well' audio file so that different objects can be inserted
#to minimize the number of audio files needed and to lower the amount of variance between instructions
audioToPlay = False
audioPlayBackQueue = []
import viz

#The addAudio method adds the audioFile passed to it to the back of the audioPlayBackQueue
#If it is the only element in the queue it starts playing this audio file
def addAudio(audioToAdd):
	global audioPlayBackQueue
	global audioToPlay
	audioPlayBackQueue += [audioToAdd] #combines the audioPlayBackList and a one element list of the audio file to add
	if audioToPlay != True:
		#If no audio is curently playing start playing the first element of the queue
		audioPlayBackQueue[0].play()
		audioToPlay = True

#The audioFinishedCheck is called during the main loop of the program to see whether it is time to start playing
#the next audio file.
#When importing this script the line audioControls.audioFinishedCheck() should be one of the first things in the masterLoop
#This then goes through and checks to see if any audio has finished playing and if so it will 
def audioFinishedCheck():
	global audioPlayBackQueue
	global audioToPlay
	if  audioToPlay and (audioPlayBackQueue[0].getState() == viz.MEDIA_STOPPED):
		#If the sound file that was playing has completed, remove that file from the front of the queue
		audioPlayBackQueue = audioPlayBackQueue[1:]
		if (len(audioPlayBackQueue) == 0):
			#if there are no elements in the list, then set audioToPlay to False
			audioToPlay = False
		else:
			#if there are elements in the list, then start playing the new front element
			audioPlayBackQueue[0].play()

# This function should do a simple check to see if there is audio to play or currently playing
def audioPlaying():
	global audioPlayBackQueue
	global audioToPlay
	
	if audioPlayBackQueue or audioToPlay:
		return True
	return False