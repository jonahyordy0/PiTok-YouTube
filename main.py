import os

from pitok import TikVideo

import random
import datetime
import time
import shutil
import pickle
from uploader import upload
import datetime

posting_times = {
    0:[ # Monday
        [6,0],
        [10,0],
        [22,0]
    ],
    1:[ # Tuesday
        [2,0],
        [4,0],
        [9,0]

    ],
    2:[ # Wednesday
        [7,0],
        [8,0],
        [23,0]
    ],
    3:[ # Thursday
        [9,0],
        [12,0],
        [19,0]
    ],
    4:[ # Friday
        [5,0],
        [13,0],
        [15,0]
    ],
    5:[ # Saturday
        [11,0],
        [19,0],
        [20,0]
    ],
    6:[ #Sunday
        [7,0],
        [8,0],
        [16,0]
    ]
}

def video_exists():
    return len([each for each in os.listdir('.') if each.endswith('.mp4')]) > 0

def get_local_vid():
    return [each for each in os.listdir('.') if each.endswith('.mp4')][0]

while True:
    drives = os.listdir("/media/"+ os.getlogin() +"/")
    print(drives)
    if len(drives) == 0:
        print("No drives detected")


    elif drives[0] == "YOUTUBE":
        # Set constants for youtube account
        clip_len = 70

        videos_folder = os.listdir("/media/"+ os.getlogin() +"/"+drives[0]+"/videos")

        # Loop through all videos on drive
        while len(videos_folder) > 0:
            # Check if we are already editing a video
            if not video_exists():
                # Move new video from drive to local folder saved as name (vname)
                cur_file = videos_folder[0]
                shutil.move("/media/"+ os.getlogin() +"/"+drives[0]+"videos/" + cur_file, "./" + cur_file)
                
                # Reset pickle file
                with open("info.pkl", "wb") as f:
                    pickle.dump(0, f)

            # Init tik tok video object
            vname = get_local_vid()
            cur_video = TikVideo(vname)
            print(cur_video.start)
            
            # Continue posting clips until entire video is posted
            while not cur_video.is_over():
                # Get the current time to check if it is time to post
                time_now = datetime.datetime.now()
                print(time_now)

                if [time_now.hour, time_now.minute] in posting_times[time_now.weekday()]:
                    print("Posting...")
                    # Create next clip and upload
                    cname = cur_video.create_next_clip(clip_len)
                    upload(cname, 1)
                    # Set new start point for next clip
                    cur_video.update_info(cur_video.start)
                    #time.sleep(post_interval + random.randint(0, 600))
                time.sleep(15)

            # Delete local video file and destroy movie py objects to free up memory
            cur_video.destroy()
            videos_folder = os.listdir("/media/"+ os.getlogin() +"/"+drives[0]+"/videos")
            time.sleep(10)

    time.sleep(30)