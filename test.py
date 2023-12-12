from threading import Thread
 
import pvporcupine
from pvrecorder import PvRecorder
 
import logic
import speech_synthesis

import secret
KEYWORDS = [
    'alexa', 'americano', 'blueberry', 'bumblebee', 'computer', 'grapefruit', 'grasshopper', 'hey google', 'hey siri',
    'jarvis', 'picovoice', 'porcupine'
]
 
ACCESS_KEY = secret.ACCESS_KEY  # Replace with your Picovoice access key
AUDIO_DEVICE_INDEX = secret.AUDIO_DEVICE_INDEX # Set to the desired audio device index or -1 for the default audio device
KEYWORD_FILE_PATH = secret.KEYWORD_FILE_PATH
 
class PorcupineThread():
    def __init__(self):
        self._detected_keyword = None
        self._is_ready = False
        self._stop = False
        self._is_stopped = False
 
    def run(self):
        ppn = None
        recorder = None
 
        try:
            
            ppn = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=['./Hey-Click-share_en_mac_v3_0_0.ppn'])

            # ppn = pvporcupine.create(access_key=ACCESS_KEY, keywords=KEYWORDS, sensitivities=[0.75] * len(KEYWORDS))
 
            recorder = PvRecorder(device_index=AUDIO_DEVICE_INDEX, frame_length=ppn.frame_length)
            recorder.start()
 
            self._is_ready = True
 
            while not self._stop:
                pcm = recorder.read()
                keyword_index = ppn.process(pcm)
                
                # print(keyword_index)
                if keyword_index >= 0:
                    self._detected_keyword = "Hey ClickShare"
                    recorder.stop()
                    
                    print(f"Wake word detected: {self._detected_keyword}")
                    logic.main()
                    # speech_synthesis.play_text("Hello there ")
                    recorder.start()
        finally:
            if recorder is not None:
                recorder.delete()
 
            if ppn is not None:
                ppn.delete()
 
        self._is_stopped = True
 
    def is_ready(self):
        return self._is_ready
    

    def stop(self):
        self._stop = True
    
    def is_stopped(self):
        return self._is_stopped
        

 
def main():
    porcupine_thread = PorcupineThread()
 
    porcupine_thread.run()
    # while not porcupine_thread.is_ready():
    #     pass
 
    # try:
    #     while True:
    #         pass  # Keep the script running
    # except KeyboardInterrupt:
    #     porcupine_thread.stop()
    #     while not porcupine_thread.is_stopped():
    #         pass
 
 
if __name__ == '__main__':
    main()