import pyautogui as pg
import time
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

class WriteSong():
    def __init__(self):
        self.picturePath = "instructions/pictures/"
        self.templatePath = "instructions/pictures/template.png"

    def load_image(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        assert img is not None, f"file {filename} could not be read, check with os.path.exists()"
        return img

    def save_screenshot(self):
        pg.screenshot().save(self.templatePath)

    def match_template(self, img, template):
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust this threshold as necessary

        _, binary_res = cv2.threshold(res, threshold, 1, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours((binary_res * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("No matches found")

        # Find the rightmost match
        rightmost_contour = max(contours, key=lambda c: cv2.boundingRect(c)[0])
        x, y, w, h = cv2.boundingRect(rightmost_contour)
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        
        print(f"Detected point coordinates: top_left = {top_left}, bottom_right = {bottom_right}")
        return top_left, bottom_right

    def display_match(self, img, res, top_left, bottom_right):
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle('cv2.TM_CCOEFF_NORMED')
        plt.show()

    def write_song(self, song_name, isLiked=True):
        pg.FAILSAFE = False

        # Load appropriate search bar image
        search_bar_img = "searchBar.png" if not isLiked else "likesBar.png"
        img = self.load_image(os.path.join(self.picturePath, search_bar_img))
        
        # Save and load the screenshot
        self.save_screenshot()
        template = self.load_image(self.templatePath)
        
        # Perform template matching
        top_left, bottom_right = self.match_template(img, template)
        
        # Click on detected point with an offset
        click_offset = (20, 20) if isLiked else (70, 30)
        pg.click(top_left[0] + click_offset[0], top_left[1] + click_offset[1])
        
        # If liked, perform additional steps
        if isLiked:
            img = self.load_image(os.path.join(self.picturePath, "likesSearchBar.png"))
            self.save_screenshot()
            template = self.load_image(self.templatePath)
            top_left, bottom_right = self.match_template(img, template)
            pg.click(top_left[0] + 20, top_left[1] + 20)
        
        # Display the match result
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        # self.display_match(img, res, top_left, bottom_right)

        # Type the song name
        pg.write(song_name)