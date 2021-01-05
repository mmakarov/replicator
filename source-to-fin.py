#!/usr/bin/env python

from moviepy.editor import *
import os
import pathlib
import re
from natsort import natsorted
import proglog

heading_text = input(u'Введите заголовок (20 зн.): ')
if len(heading_text) > 20:
    print("Слишком длинный текст заголовка!")
    sys.exit()
if len(heading_text) == 0:
    heading_text = u'#ЗАГОЛОВОК'.encode('utf-8')
name_part1 = input(u'Введите имя (20 зн.): ')
if len(name_part1) > 20:
    print("Слишком длинный текст имени!")
    sys.exit()
if len(name_part1) == 0:
    name_part1 = u'Имя'.encode('utf-8')
name_part2 = input(u'Введите дополнительный текст (20 зн.): ')
if len(name_part2) > 20:
    print("Слишком длинный дополнительный текст!")
    sys.exit()
if len(name_part2) == 0:
    name_part2 = u'Страна'.encode('utf-8')
date_text  = input(u'Введите дату (20 зн.): ')
if len(date_text) > 20:
    print("Слишком длинный текст даты!")
    sys.exit()
if len(date_text) == 0:
    date_text = u'Дата мероприятия'.encode('utf-8')

L =[]

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):

    #files.sort()
    files = natsorted(files)
    for file in files:
        #if os.path.splitext(file)[1] == '.mp4':
        path = pathlib.Path('video/'+file)
        if (path.stem.find("source") == 0) and (os.path.splitext(file)[1] == '.mp4'):
            print('Найден файл: ' + file)
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath, audio=False, target_resolution=(720, 1280))
            overlay = (ImageClip("overlay.png")).set_duration(video.duration)
            heading_text_clip = (TextClip(heading_text,font="Helvetica", fontsize=68,color='white', method='label').set_duration(video.duration).set_position(("center",150)))
            name_part1_clip = (TextClip(name_part1,font="Helvetica-Bold", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",250)))
            name_part2_clip = (TextClip(name_part2,font="Helvetica", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",300)))
            date_text_clip = (TextClip(date_text,font="Helvetica", fontsize=36,color='white', method='label').set_duration(video.duration).set_position(("center",400)))
            readyclip = CompositeVideoClip([video, overlay, heading_text_clip, name_part1_clip, name_part2_clip, date_text_clip])
            L.append(readyclip) #video
print("Соединяем все вместе...")
final_clip = concatenate_videoclips(L, method='compose')
print("Сохраняем видео...")
final_clip.write_videofile("medium.mp4", fps=24, remove_temp=True, preset='fast', audio=False, logger=proglog.TqdmProgressBarLogger(print_messages=False))


#========= final steps ==========

import audioread
import math

audio_filename = "voice.mp3"
video_filename = "medium.mp4"
silent_fin_filename = "silent_fin.mp4"
fin_filename = "youtube_ready.mp4"

with audioread.audio_open('audio/'+audio_filename) as audio:
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
subprocess.call(['ffmpeg', '-stream_loop', str(loop), '-i', video_filename, '-c', 'copy', silent_fin_filename, '-hide_banner', '-y', '-loglevel', 'panic'])
print("Готово. Видео без звука находится в файле " + silent_fin_filename)

# Добавляем звуковую дорожку
#ffmpeg -i video.avi -i audio.mp3 -codec copy -shortest output.avi
print("Добавляем звуковую дорожку к файлу " + silent_fin_filename)
print("Может потребоваться время...")
subprocess.call(['ffmpeg', '-i', silent_fin_filename, '-i', audio_filename, '-map', '0:v', '-map', '1:a', '-vcodec', 'copy', '-acodec', 'aac', '-loglevel', 'panic', '-shortest', '-y', fin_filename])

print("Прибираемся...")
subprocess.call(['rm', silent_fin_filename])
subprocess.call(['rm', video_filename])

print("Сделано! Видео для загрузки в Youtube в файле " + fin_filename)
print("Летайте Российскими авиалиниями :)")
print("")