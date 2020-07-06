from moviepy.editor import VideoFileClip, concatenate_videoclips
from downloadingTwitchClips import downloadingVideos
from helpers.allCategories import game_dict
import threading
import time
import os 

# ranged = '24hr', '7d', '30d', 'all'
# games = 'Overwatch', 'Fortnite', 'Valorant'
def gettingAllGames():
    print(game_dict.keys())
    for key in game_dict.keys():
        # downloadingVideos('game', 'range', [links])
        downloadingVideosClass = downloadingVideos(key, '7d', None)
        grabbingLinks(downloadingVideosClass)

        # delete previous videos 
        clearVideos()

    return 'finished'

def grabbingLinks(grabbing_and_downloading):
    grabbing_and_downloading.allFunctions()
    creatingVideo(grabbing_and_downloading)
    return True

def clearVideos():
    os.system('rm videos/*')

def creatingVideo(twitchClipsClass):
    game = twitchClipsClass.game
    print('Creating video, go grab a coffee or go for a walk')
    Allclips = []
    for file in os.listdir('./videos'):
        if(file != '.DS_Store'):  
            Allclips.insert(0, VideoFileClip('./videos/' + file).resize((1920,1080)).set_fps(60))

    final_clip = concatenate_videoclips(Allclips)
    final_clip.write_videofile(f"./output/{game}.mp4",remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    gettingAllGames()
    