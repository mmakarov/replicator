#!/usr/bin/env python

from moviepy.editor import *
import os
import pathlib
import re
from natsort import natsorted
import proglog

heading_text = input(u'‚  (20 .): ')
if len(heading_text) > 20:
    print("ˆ ‹ ‚‚ !")
    sys.exit()
if len(heading_text) == 0:
    heading_text = u'#'.encode('utf-8')
name_part1 = input(u'‚  (20 .): ')
if len(name_part1) > 20:
    print("ˆ ‹ ‚‚ !")
    sys.exit()
if len(name_part1) == 0:
    name_part1 = u''.encode('utf-8')
name_part2 = input(u'‚ ‚Œ‹ ‚‚ (20 .): ')
if len(name_part2) > 20:
    print("ˆ ‹ ‚Œ‹ ‚‚!")
    sys.exit()
if len(name_part2) == 0:
    name_part2 = u'‚€'.encode('utf-8')
date_text  = input(u'‚ ‚ƒ (20 .): ')
if len(date_text) > 20:
    print("ˆ ‹ ‚‚ ‚‹!")
    sys.exit()
if len(date_text) == 0:
    date_text = u'‚ €€‚'.encode('utf-8')

L =[]

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):

    #files.sort()
    files = natsorted(files)
    for file in files:
        #if os.path.splitext(file)[1] == '.mp4':
        path = pathlib.Path(os.path.join('video',file))
        if (path.stem.find("source") == 0) and (os.path.splitext(file)[1] == '.mp4'):
            print(' „: ' + file)
            filePath = os.path.join(root, file)
            print(filePath+"\n")
            video = VideoFileClip(filePath, audio=False, target_resolution=(720, 1280))
            overlay = (ImageClip("overlay.png")).set_duration(video.duration)
            heading_text_clip = (TextClip(heading_text,font="Arial", fontsize=68,color='white', method='label').set_duration(video.duration).set_position(("center",150)))
            name_part1_clip = (TextClip(name_part1,font="Arial", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",250)))
            name_part2_clip = (TextClip(name_part2,font="Arial", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",300)))
            date_text_clip = (TextClip(date_text,font="Arial", fontsize=36,color='white', method='label').set_duration(video.duration).set_position(("center",400)))
            readyclip = CompositeVideoClip([video, overlay, heading_text_clip, name_part1_clip, name_part2_clip, date_text_clip])
            L.append(readyclip) #video
print("  ‚...")
final_clip = concatenate_videoclips(L, method='compose')
print("…€ ...")
final_clip.write_videofile("medium.mp4", fps=24, remove_temp=True, preset='fast', audio=False, logger=proglog.TqdmProgressBarLogger(print_messages=False))


#========= final steps ==========

import audioread
import math

audio_filename = "voice.mp3"
video_filename = "medium.mp4"
silent_fin_filename = "silent_fin.mp4"
fin_filename = "youtube_ready.mp4"

with audioread.audio_open(os.path.join('audio',audio_filename)) as audio:
    audio_file_length = math.ceil(audio.duration)
    print("‚Œ‚Œ ƒ„ " + audio_filename + ": " + str(audio_file_length) + " ƒ(‹)")

from moviepy.editor import VideoFileClip
video = VideoFileClip(video_filename)
video_file_length = math.ceil(video.duration)
print("‚Œ‚Œ „ " + video_filename + ": " + str(video_file_length) + " ƒ(‹)")
multiplier = audio_file_length / video_file_length
print(" ‚€ƒ‚ ‚€‚Œ " + str(multiplier) + " €")
multiplier = math.ceil(multiplier)
print("€ƒ  " + str(multiplier))

import os
import subprocess
print("‚   " + os.getcwd())
os.chdir(os.getcwd())

loop = multiplier - 1
# ƒ € €ƒ‚‡   €
#ffmpeg -stream_loop 3 -i part.mp4 -c copy ffmpeg_stream_loop.mp4
print("…€ Œˆ , ‚€ƒ‚ €...")
subprocess.call(['ffmpeg', '-stream_loop', str(loop), '-i', video_filename, '-c', 'copy', silent_fin_filename, '-hide_banner', '-y', '-loglevel', 'panic'])
print("‚.   ƒ …‚  „ " + silent_fin_filename)

#  ƒƒŽ €ƒ
#ffmpeg -i video.avi -i audio.mp3 -codec copy -shortest output.avi
print(" ƒƒŽ €ƒ  „ƒ " + silent_fin_filename)
print("‚ ‚€‚Œ €...")
subprocess.call(['ffmpeg', '-i', silent_fin_filename, '-i', os.path.join('audio',audio_filename), '-map', '0:v', '-map', '1:a', '-vcodec', 'copy', '-acodec', 'aac', '-loglevel', 'panic', '-shortest', '-y', fin_filename])

print("€€...")
if os.path.exists(os.path.join(os.getcwd(),silent_fin_filename)):
    os.remove(os.path.join(os.getcwd(),silent_fin_filename))
    print(" „ " + os.path.join(os.getcwd(),silent_fin_filename))

#print(" " + os.path.join(os.getcwd(),video_filename))
#if os.path.exists(os.path.join(os.getcwd(),video_filename)):
#    os.remove(os.path.join(os.getcwd(),video_filename))
#    print(" „ " + os.path.join(os.getcwd(),video_filename))

print("!   €ƒ  Youtube  „ " + os.path.join(os.getcwd(),fin_filename))
print("‚‚   :)")
print("")