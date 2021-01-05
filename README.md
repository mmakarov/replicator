# replicator
Python script to merge a few video files, transparent overlay, text areas with mp3 audio track. Final video will be exact same length as your audio track. Lenght of your video will be calculated automatically.

[![Resulting video](http://img.youtube.com/vi/4Uu1hS3-eQM/0.jpg)](http://www.youtube.com/watch?v=4Uu1hS3-eQM "Replicator script example video")

I've make this script in a try to merge any video sequence files with PNG transparent overlay, adding text areas on video, with mp3 audio track. Resulting video file are ready to upload on Youtube or any other video hosting services.

You can change it on your taste.

How to use it:
0. Open terminal and enter: git clone https://github.com/mmakarov/replicator.git
1. Put your video files to 'video' directory as 'source1.mp4', 'source2.mp4', etc
2. Put your PNG transparent image to project directory as 'overlay.png'
3. Put your MP3 file to 'audio' directory as 'voice.mp3'
4. in terminal run: python3 source-to-fin.py
	or python source-to-fin-win.py for Windows
7. Finally you've got youtube_ready.mp4 file

Warning: russian comments in sources!
