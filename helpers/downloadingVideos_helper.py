import random
import os
import time
from helpers.allCategories import game_dict

def getChannelName(string):
        channel = ''
        for char in range(len(string)-1):
            curChar = string[char]
            if char > 0:
                if curChar == '/':
                    return channel
                else:
                    channel += curChar

def gettingLinks(linkValue, func, game):
    allChannels = game_dict[game]['approved_channels']
    link = ""
    for char in range(len(linkValue)-1):
        if char > 5:
            curChar = linkValue[char]
            nextChar = linkValue[char + 1]
            prevChar = linkValue[char - 1]

            if(prevChar == '"'):
                link += curChar
            elif(nextChar == '"'):
                link += curChar
                if func == 1:
                    print(link)
                    channel = getChannelName(link)
                    #Checking to see if channel is in approved channels
                    if channel in allChannels:
                        return link
                    else:
                        print('NOT APPROVED!')
                        return False
                elif func == 2:
                    return 'https://' + link[2:len(link)]
            else:
                link += curChar
        
def randomizeVideoName():
    return str(random.randint(0,1000))

def downloadingVideo(link):
    os.system(f'cd videos;curl -O {link}')
    time.sleep(3)
    return ''


    