import os
import time
import pyautogui as pg
import cv2
from instructions.image import WriteSong

class SpotifyBot:
    def __init__(self):
        self.write_song = WriteSong()
    
    def open_spotify(self):
        os.system("start spotify")
        pg.getWindowsWithTitle("Spotify")[0].activate()
        time.sleep(3)
        self.write_song.write_song(song_name="Outflow")

if __name__ == "__main__":
    bot = SpotifyBot()
    bot.open_spotify()