import audioread
import math

audio_filename = "voice.mp3"
video_filename = "medium.mp4"
silent_fin_filename = "silent_fin.mp4"
fin_filename = "youtube_ready.mp4"

with audioread.audio_open(audio_filename) as audio:
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
subprocess.call(['ffmpeg', '-stream_loop', str(loop), '-i', 'medium.mp4', '-c', 'copy', silent_fin_filename, '-hide_banner', '-loglevel', 'panic'])
print("‚.   ƒ …‚  „ " + silent_fin_filename)

#  ƒƒŽ €ƒ
#ffmpeg -i video.avi -i audio.mp3 -codec copy -shortest output.avi
print(" ƒƒŽ €ƒ  „ƒ " + silent_fin_filename)
print("‚ ‚€‚Œ €...")
subprocess.call(['ffmpeg', '-i', silent_fin_filename, '-i', audio_filename, '-codec', 'copy', '-shortest', fin_filename, '-hide_banner', '-loglevel', 'warning'])

print("€€...")
subprocess.call(['rm', silent_fin_filename])

print("!   €ƒ  Youtube  „ " + fin_filename)
print("‚‚   :)")
print("")