# replicator
Python script to merge a few video files, transparent overlay, text areas with mp3 audio track. Final video will be exact same length as your audio track. Lenght of your video will be calculated automatically.

[![Resulting video](http://img.youtube.com/vi/4Uu1hS3-eQM/0.jpg)](http://www.youtube.com/watch?v=4Uu1hS3-eQM "Replicator script example video")

I've made this script in a try to merge any video sequence files with PNG transparent overlay, adding text areas on video, with mp3 audio track. The resulting video file is ready to upload on Youtube or any other video hosting service.

You can change it to your taste.

How to use it: 

Open the terminal and enter: git clone https://github.com/mmakarov/replicator.git

Put your video files to the 'video' directory as 'source1.mp4', 'source2.mp4', etc

Put your PNG transparent image to the project directory as 'overlay.png'

Put your MP3 file to the 'audio' directory as 'voice.mp3'
in terminal run: python3 source-to-fin.py or python source-to-fin-win.py for Windows

Finally, you've got the "youtube_ready.mp4" file

Warning: Russian comments in sources!
