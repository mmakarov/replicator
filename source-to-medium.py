#!/usr/bin/env python

from moviepy.editor import *
import os
import pathlib
import re
from natsort import natsorted

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


print("С текстом разобрались. Спасибо!")

L =[]

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):

    #files.sort()
    files = natsorted(files)
    for file in files:
        #if os.path.splitext(file)[1] == '.mp4':
        path = pathlib.Path(file)
        if (path.stem.find("source") == 0) and (os.path.splitext(file)[1] == '.mp4'):
            print('Найден файл: ' + file)
            filePath = os.path.join(root, file)
            print("Берем исходное видео...")
            video = VideoFileClip(filePath, audio=False, target_resolution=(720, 1280))
            print("Добавляем оверлей...")
            overlay = (ImageClip("overlay.png")).set_duration(video.duration)
            print("Наносим надписи...")
            heading_text_clip = (TextClip(heading_text,font="Helvetica", fontsize=68,color='white', method='label').set_duration(video.duration).set_position(("center",150)))
            name_part1_clip = (TextClip(name_part1,font="Helvetica-Bold", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",250)))
            name_part2_clip = (TextClip(name_part2,font="Helvetica", fontsize=42,color='white', method='label').set_duration(video.duration).set_position(("center",300)))
            date_text_clip = (TextClip(date_text,font="Helvetica", fontsize=36,color='white', method='label').set_duration(video.duration).set_position(("center",400)))
            readyclip = CompositeVideoClip([video, overlay, heading_text_clip, name_part1_clip, name_part2_clip, date_text_clip])
            L.append(readyclip) #video
print("Соединяем все вместе...")
final_clip = concatenate_videoclips(L, method='compose')
print("Сохраняем видео...")
final_clip.write_videofile("medium.mp4", fps=24, remove_temp=True, preset='fast', audio=False)