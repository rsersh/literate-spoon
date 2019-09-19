
# code from Python Playground by Mahesh Venkitachalam
# updates for python 3.7 by Rachel Hunt
#  * plist.readPlist(file) => plistlib.load(file) 
#  * added 'with' statement to modify/read files 
#      instead of direct calls to file 
#  * added 'b' when opening file to write in binary
#      in findCommonTracks()
#  * str.encode("UTF-8") =>  str.encode() 
#      might work as is with 'b' added at open
#  * cannot locate 'Album Rating' in author's music list 
#      using 'Play Count' instead

import sys
import plistlib
import numpy as np
from matplotlib import pyplot
import re, argparse

def getPlist(filename):
    with open(filename, 'rb') as fp:
        plist = plistlib.load(fp)
    return plist

def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' % fileName)
    # grab/load a plist 
    plist = getPlist(fileName) 
    # get the tracks from the Tracks dictionary
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                # if a name and duration match, increment the count
                # round the track length to the nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dictionary entry as tuple (duration, count)
                trackNames[name] = (duration, 1)
        except:
            pass

    # store duplicates as (name, count) tuples
    dups = []
    for k,v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save duplicates to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dups.txt" % len(dups))
        try:
            f = open("dups.txt", "w")
            for val in dups:
                f.write("[%d] %s\n" % (val[0], val[1]))
        finally:
            f.close()
    else: 
        print("No duplicates tracks found!")

def findCommonTracks(fileNames):
    # a list of sets of track names
    trackNamesSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        plist = getPlist(fileName)
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                pass
        # add to list
            trackNamesSets.append(trackNames)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNamesSets)
    # write to file
    if len(commonTracks) > 0:
        with open("common.txt", "wb") as fd:
            for val in commonTracks: 
                s = "%s\n" % val
                fd.write(s.encode())
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    # read in a playlist
    plist = getPlist(fileName)
    # get the tracks from the playlist
    tracks = plist['Tracks']
    # create lists of song ratings and track durations
    plays = []
    durations = []
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            plays.append(track['Play Count'])
            durations.append(track['Total Time'])
        except:
            pass
    # ensure valid data was collected
    if plays == [] or durations == []:
        print("No valid Play Count/Total Time data in %s." % fileName)
        return

    # scatter plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(plays, np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x,y,'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track plays')
    
    # plot histogram
    pyplot.subplot(2,1,2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # print plot to png file
    pyplot.savefig('test.png', bbox_inches="tight")

def main():
    # create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()
    # add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()
    
    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

# main method
if __name__ == '__main__':
    main()

'''
hismusic = "/home/chouchou/PyPlate/testmusic.xml"
mymusic = "/home/chouchou/PyPlate/music.xml"
allmusiclists = [hismusic, mymusic]

findDuplicates(hismusic)
findCommonTracks(allmusiclists)
plotStats(mymusic)
'''
