from downloadingTwitchClips import downloadingVideos
from unittest import TestCase
import unittest
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

        downloadingVideosClass.initializingDriver(False)
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


if __name__ == "__main__":
    
    unittest.main()