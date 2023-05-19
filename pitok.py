import random
import os
import time
import pickle
import textwrap

from moviepy.editor import *
from moviepy.video.fx.all import crop

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import numpy as np

def create_image(text, s, pos):

    font = ImageFont.truetype("font.ttf", size=s)
    w, h = font.getsize(text)

    img = Image.new('RGB', (720, 437), (0, 0, 0))
    d = ImageDraw.Draw(img)
    W, H = img.size
    d.text((W/2,H/pos), text, fill=(255, 255, 255), font=font, anchor="mm", align='center')

    return np.asarray(img)

class TikVideo:
    def __init__(self, loc):
        self.loc = loc
        with open('info.pkl', 'rb') as f:
            i = pickle.load(f)
            self.start = i[0]
            self.part = i[1]
        self.clip = VideoFileClip(self.loc)
        self.duration = self.clip.duration

    def create_next_clip(self, clip_len):
        filename = os.path.splitext(os.path.basename(self.loc))[0].split("@")
        video_name = filename[0]
        clip_name = filename[1]
        clip_len += random.randint(0,20)
        
        # Check if clip is nearing end so last clip isn't only a few seconds long
        if self.duration < (self.start + clip_len + 20):
            clip = self.clip.subclip(self.start, self.duration)
        else:
            clip = self.clip.subclip(self.start, self.start + clip_len)
        
        clip = clip.resize(width=720).margin(top=437, bottom=438)

        # Load PIL Part Image
        wrapper = textwrap.TextWrapper(width=15)
        video_title = wrapper.wrap(text=video_name.split("@")[0])
        top_image = ImageClip(create_image("\n".join(video_title), 100 - len(video_title) * 10, 1.75), duration=clip.duration)
        bottom_image = ImageClip(create_image(f"Part {self.part}", 90, 3), duration=clip.duration)


        # Build our main clip
        video = CompositeVideoClip([clip, top_image.set_position("top"),  bottom_image.set_position("bottom")])
        self.start += video.duration
        self.part += 1
        
        # Save as new clip overwritting last one
        video.write_videofile(clip_name + ".mp4", preset="ultrafast", fps=30)

        # Close moviepy VideoClip objects to free up memory
        video.close()
        clip.close()

    
    def update_info(self):
        # Save new start and part value
        with open('info.pkl', 'wb') as f:
            pickle.dump([self.start, self.part], f)

    def is_over(self):
        # Check if the current video is over
        return self.start >= self.duration
    
    def destroy(self):
        # Clear up memory
        os.remove(self.loc)
        self.clip.close()
        with open('info.pkl', 'wb') as f:
            pickle.dump([0,1], f)
