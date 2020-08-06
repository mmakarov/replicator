import audioread
import math

audio_filename = "voice.mp3"
video_filename = "medium.mp4"
silent_fin_filename = "silent_fin.mp4"
fin_filename = "youtube_ready.mp4"

with audioread.audio_open(audio_filename) as audio:
    audio_file_length = math.ceil(audio.duration)
    print("Длительность аудиофайла " + audio_filename + ": " + str(audio_file_length) + " секунд(ы)")

from moviepy.editor import VideoFileClip
video = VideoFileClip(video_filename)
video_file_length = math.ceil(video.duration)
print("Длительность видеофайла " + video_filename + ": " + str(video_file_length) + " секунд(ы)")
multiplier = audio_file_length / video_file_length
print("Видео потребуется повторить " + str(multiplier) + " раз")
multiplier = math.ceil(multiplier)
print("Округлим до " + str(multiplier))

import os
import subprocess
print("Работаем в папке " + os.getcwd())
os.chdir(os.getcwd())

loop = multiplier - 1
# Запускаем копирование промежуточного видео много раз
#ffmpeg -stream_loop 3 -i part.mp4 -c copy ffmpeg_stream_loop.mp4
print("Сохраняем большое видео, потребуется время...")
subprocess.call(['ffmpeg', '-stream_loop', str(loop), '-i', 'medium.mp4', '-c', 'copy', silent_fin_filename, '-hide_banner', '-loglevel', 'panic'])
print("Готово. Видео без звука находится в файле " + silent_fin_filename)

# Добавляем звуковую дорожку
#ffmpeg -i video.avi -i audio.mp3 -codec copy -shortest output.avi
print("Добавляем звуковую дорожку к файлу " + silent_fin_filename)
print("Может потребоваться время...")
subprocess.call(['ffmpeg', '-i', silent_fin_filename, '-i', audio_filename, '-codec', 'copy', '-shortest', fin_filename, '-hide_banner', '-loglevel', 'warning'])

print("Прибираемся...")
subprocess.call(['rm', silent_fin_filename])

print("Сделано! Видео для загрузки в Youtube в файле " + fin_filename)
print("Летайте Российскими авиалиниями :)")
print("")