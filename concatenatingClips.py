from moviepy.editor import VideoFileClip, concatenate_videoclips
from downloadingTwitchClips import downloadingVideos
import threading
import time
import os 
# ranged = '24hr', '7d', '30d', 'all'
# games = 'Overwatch', 'Fortnite', 'Valorant'
def grabbingLinks():
    grabbing_and_downloading = downloadingVideos('Overwatch', '7d')
    grabbing_and_downloading.allFunctions()

def creatingVideo():
    print('Creating video, go grab a coffee or go for a walk')
    Allclips = []
    for file in os.listdir('./videos'):
        if(file != '.DS_Store'):  
            Allclips.insert(0, VideoFileClip('./videos/' + file).resize((1920,1080)).set_fps(60))

    final_clip = concatenate_videoclips(Allclips)
    final_clip.write_videofile("./output/both_videos.mp4",remove_temp=True, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    grabbingLinks()
    creatingVideo()