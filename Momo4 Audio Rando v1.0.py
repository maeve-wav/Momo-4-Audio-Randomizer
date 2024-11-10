import itertools
import shutil
import os
from random import shuffle


# Initialize variables and poll initial state of music directories
bPath = 'C:/Program Files (x86)/Steam/steamapps/common/Momodora RUtM'
mPath = bPath + '/music'
rPath = bPath + '/Randommusic'
vPath = bPath + '/Vanillamusic'

music = os.path.isdir(mPath)
random = os.path.isdir(rPath)
vanilla = os.path.isdir(vPath)


# THE SHUFFLER: Shuffles music names in Randommusic
# Establish filenames to shuffle
outNames = ['/boss.oggx', '/boss2.oggx', '/boss3.oggx', '/boss4.oggx', '/boss5.oggx', '/boss6.oggx', '/boss7.oggx', '/castle1.oggx', '/castle2.oggx', '/castle3.oggx', '/church.oggx', '/cinder.oggx', '/city_ambiance.oggx', '/ending.oggx', '/forest_ambiance.oggx', '/forest_ambiance2.oggx', '/garden.oggx', '/mausoleum_ambiance.oggx', '/momomusicbox.oggx', '/pinacotheca.oggx', '/pinacotheca2.oggx', '/title.oggx', '/title2.oggx', '/winter.oggx', '/xxxx.oggx']
# Establish filenames to start from
inNames = ['/boss.oggx', '/boss2.oggx', '/boss3.oggx', '/boss4.oggx', '/boss5.oggx', '/boss6.oggx', '/boss7.oggx', '/castle1.oggx', '/castle2.oggx', '/castle3.oggx', '/church.oggx', '/cinder.oggx', '/city_ambiance.oggx', '/ending.oggx', '/forest_ambiance.oggx', '/forest_ambiance2.oggx', '/garden.oggx', '/mausoleum_ambiance.oggx', '/momomusicbox.oggx', '/pinacotheca.oggx', '/pinacotheca2.oggx', '/title.oggx', '/title2.oggx', '/winter.oggx', '/xxxx.oggx']



def sHuffle(): # Re/shuffles random music folder
    shuffle(outNames)
    rPathLocal = rPath
    # Allow shuffle of random music when active
    if dirState == 5:
        rPathLocal = mPath
    # Obfuscate filenames to prevent duplicates while renaming (i know i'm misusing 'obfuscate' lol)
    for i in range(len(inNames)):
        rPathIn = rPathLocal + inNames[i]
        rPathNum = rPathLocal + str(i) + '.oggx'
        os.rename(rPathIn, rPathNum)
        #print('Obfuscated ', str(i+1), ' filenames')
    #print('Obfuscation complete\n')
    # Rename Randommusic/numberName[n] to outNames[n]
    for i in range(len(outNames)):
        rPathNum = rPathLocal + str(i) + '.oggx'
        rPathOut = rPathLocal + outNames[i]
        os.rename(rPathNum, rPathOut)
        print('Shuffled ', str(i+1), ' music file(s)')
    print('Randomization complete\n')


# Create list with n^3 boolean permutations
# This sets up an element integer for each music directory permutation
l = [False, True]
dirCompare = [list(i) for i in itertools.product(l, repeat=3)]

# This list will hold the current music dir state
dirActive = [0, 0, 0]
dirState = 8

# This function lets the program see the current music dir state
def isActive():
    music = os.path.isdir(mPath)
    random = os.path.isdir(rPath)
    vanilla = os.path.isdir(vPath)
    
    dirActive[0] = music
    dirActive[1] = random
    dirActive[2] = vanilla
    #print(dirActive) 

    # Find which element in dirCompare matches dirActive, telling us which integer state we're in
    global dirState
    dirState = dirCompare.index(dirActive)
    print('This is state', dirState, '\n')


# Test run of isActives, also informs user of the initial state
isActive()

# Define functions to deal with different states of the music files
def panic():
    print('Original music files not detected. Please verify files on Steam,\nor try to rename the randomized files if applicable')
    print('!!! If non-Steam user, set *bPath* in line 12 to your Momodora RutM program folder !!!\n')

def reset():
    shutil.rmtree(mPath, ignore_errors=True) # Deletes music dir if applicable
    # (it's a duplicate if Vanillamusic also exists)
    print('Deleted duplicate music directory (if applicable)')
    os.rename(vPath, mPath) # Renames Vanillamusic to music
    print('Enabled vanilla music\n')
    newAction() # Recursion of newAction ensures a standardized result

def setup():
    shutil.copytree(mPath, rPath) # Copy music, creating Randommusic
    print('Created random music directory\n')
    sHuffle() # Shuffles random music directory
    newAction() # Recursion of newAction ensures a standardized result

def enableRandom(): # Sets aside vanilla music, enables random music
    os.rename(mPath, vPath)
    print('Vanilla music backed up')
    os.rename(rPath, mPath)
    print('Randomized music enabled\n')

def disableRandom(): # Sets aside random music, enables vanilla music
    os.rename(mPath, rPath)
    print('Randomized music disabled')
    os.rename(vPath, mPath)
    print('Vanilla music reenabled\n')

def randomActive(): # Pretty self explanatory
    print('Randomized music is currently active')
    if input('Would you like to disable randomized music? (y/n) ') == 'y':
        disableRandom()

def vanillaActive(): # Just read the code lol
    print('Vanilla music is currently active')
    if input('Would you like to enable randomized music? (y/n) ') == 'y':
        enableRandom()

def noAction(): # This actually came up a few times in early debugging...
    print('This should not be possible...')


# Program startup
print('Welcome to the Momodora RutM Audio Randomizer!')
if dirState == 5 or dirState == 6:
    print('Your files are already set up\n')
else:
    print('Your files will be set up shortly.\n')


# Determining which function to run based on the state of the music folders
def newAction():
    isActive()
    if dirState == 0 or dirState == 2:
        panic()
    elif dirState == 1 or dirState == 3 or dirState == 7:
        reset()
    elif dirState == 4:
        setup()
    elif dirState == 5:
        randomActive()
    elif dirState == 6:
        vanillaActive()
    elif dirState == 8:
        noAction()


# Core program loop :)
while True:
    newAction()
    if dirState == 0 or dirState == 8:
        break
    if input('Would you like to reshuffle the random music? (y/n) ') == 'y':
        sHuffle()
    else:
        print('\nRandom music has not been reshuffled\n')
    if input('Continue running program? (y/n) ') == 'n':
        break