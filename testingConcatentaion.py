from downloadingTwitchClips import downloadingVideos
from concatenatingClips import creatingVideo
from unittest import TestCase
import unittest
import os
downloadingVideosClass = downloadingVideos('Overwatch', '7d', None)

class testing(TestCase):
    # Without having test as first word this func will run after everytime the test is run
    def setup(self):
        downloadingVideosClass.close_driver()

    def test_should_create_class(self):
        game = downloadingVideosClass.game
        ranged = downloadingVideosClass.ranged
        
        propsExist = ((game == 'Overwatch') == True) == ((ranged == '7d') == True)

        self.assertEqual(propsExist, True)
        
    def test_finding_links(self):
        links = downloadingVideosClass.clipLinks
        downloadingVideosClass.initializingDriver()
        downloadingVideosClass.getAllClipLinks()

        self.assertEqual(len(links) > 1, True)

    def test_with_inserted_links(self):
        downloadingVideosClass = downloadingVideos('Overwatch', '7d', ['', ''])
        links = downloadingVideosClass.clipLinks

        self.assertEqual(len(links) > 1, True)

    def test_with_one_video(self):
        downloadingVideosClass = downloadingVideos('Overwatch', '7d', [''])
        output = downloadingVideosClass.allFunctions()
        boolean = output == 'Please enter more than one video'  

        self.assertEqual(boolean, True)

    def test_video_creation_Wlinks(self):
        downloadingVideosClass = downloadingVideos('Overwatch', '7d', ['https://www.twitch.tv/bugha/clip/PrettyBelovedBananaWholeWheat', 'https://www.twitch.tv/bugha/clip/CoweringSmokyWolfPeteZaroll'])
        downloadingVideosClass.allFunctions()
        creatingVideo(downloadingVideosClass)
        found = True if 'Overwatch.mp4' in os.listdir('./output') else False
        os.system("rm videos/*; rm output/*")
        
        self.assertEqual(found, True)




if __name__ == "__main__":
    
    unittest.main()