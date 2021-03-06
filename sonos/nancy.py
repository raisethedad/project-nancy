from gtts import gTTS
#import os
import subprocess
import sys

class Nancy:
    def __init__(self,location,volume="40"):
        self.location=location.strip()
        self.volume=volume

    def read_text(self,mytext):
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("temp.mp3")
        old_vol = str(subprocess.run(["sonos", "Living Room", "volume"], stdout=subprocess.PIPE).stdout.decode('utf-8')).strip()
        print("Original Volume: "+old_vol)
        subprocess.run(["sonos", "Living Room", "volume", self.volume])
        print("Vol "+self.volume+", Playing: "+mytext)
        subprocess.run(["sonos", "Living Room", "play_file", "temp.mp3"])
        print("Setting Volume to: "+old_vol)
        subprocess.run(["sonos", "Living Room", "volume", old_vol])
        
