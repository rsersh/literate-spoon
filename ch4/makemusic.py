#! /usr/bin/python3

# The code contained within this program is directly 
# from Python Playground, Ch. 4  by Manesh Venkitachalam

# NOT YET WORKING
# --display is not showing the graph and piano hangs, 
#    doing nothing


import sys, os
import time, random
import wave, argparse 
import pygame
from pygame.locals import *
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

# show plot of algorith in action?
gShowPlot = False

# notes of a Pentatonic Minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4':262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}

# write out WAV file
def writeWAVE(filename, data):
    # WAV file parameters
    nChannels = 1
    sampleWidth = 1
    frameRate = 44100
    nFrames = 44100

    # open file - Here code was adjusted using 'with' statement
    # for best practices with file.open
    with wave.open(filename, 'wb') as fd:
        # set parameters
        fd.setparams((nChannels, sampleWidth, frameRate, nFrames,'NONE', 'noncompressed'))
        fd.writeframes(data)


# generate note of given frequency
def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    # initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    # plot of flag set
    if gShowPlot:
        axline, = plt.plot(buf)
    # initialize samples buffer
    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        #if i == 0:
         #   print("Debug statement - printing buf[0] & buf[1]: %s %s ", buf[0], buf[1])
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        #print("Debug statement - appending avg %s to buf: ", avg)
        buf.popleft()
        #print("Debug statement - popping from the left: ", avg)
        # plot of flag set
        #print("Debug statement - Printing value of gShowPlot & i: %s, %d", gShowPlot, i)
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                # needed to assign to fig so could call the canvas.draw() attributes
                fig.canvas.draw()

    # convert samples to 16-bit values and then to a string
    # the maximum value is 32767 for 16-bit
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

# play a WAV file
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # dictionary of notes
        self.notes = {}
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # play a note
    def play(self, fileName):
        try:
            #print(notes[fileName]) 
            #note = list(self.notes.values())[fileName]
            #note.play() 
            self.notes[fileName].play()
        except:
            print (fileName + ' not found!')
    def playRandom(self):
        """play a random note"""
        index = random.randint(0, len(self.notes)-1)
        try: 
            note = list(self.notes.values())[index]
            # Debug statement below
            # print(type(note))
            note.play()
        except KeyboardInterrupt:
            exit()
           

# main() function
def main():
    # declare global var
    global gShowPlot
    global fig
    desc =  "Generating sounds with Karplus String Algorithm"
    parser = argparse.ArgumentParser(description=desc) 
    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()

    # show plot if flag set
    # line 117 doesn't seem to be executing

    if args.display:
        gShowPlot = True
        plt.ion()
        # needed to add below assignment to call later to update
        fig = plt.figure()
    
    # create note player
    nplayer = NotePlayer()
    
    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print('creating ' + fileName + '...')
            writeWAVE(fileName, data)
        else:
            print('fileName already created. skipping...')
        # add note to player
        nplayer.add(fileName)

        # Debug statement below
        # print(nplayer)    
        # play note if display flag is set
        if args.display:
            nplayer.play(name + '.wav')
            time.sleep(0.5)
            #plt.show()
        
        # play a random tune - this works
    if args.play:
        while True:
            try:
                nplayer.playRandom()
                # rest - 1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                sys.exit()
                
    # random piano mode
    if args.piano:
        WINDOW_WIDTH = 400
        WINDOW_HEIGHT = 400
        while True:
            game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            for event in pygame.event.get():
                # print(event)    
                # looks like i need to remove the pygame
                #if (event.type == pygame.KEYUP):
                #if (event.type == KEYUP): 
                #if event.type == KEYUP:
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        print("key pressed")    
                        # try:
                        nplayer.playRandom()
                        time.sleep(0.5)
                        pygame.display.update()
    pygame.quit()
    sys.exit()
# call main
if __name__ == '__main__':
    main()
