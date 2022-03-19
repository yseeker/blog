---
#author: "Hugo Authors"
title: "ffmpeg"
date: "2022-03-17"
description: "cv2.setNumThreads(0)＆マルチプロセスをやめる"
tags:
  [
    "multithreading",
    "並列化",
    "高速化",
    "マルチスレッド",
    "マルチプロセス",
    "openCV",
    "ThreadPoolExecuter",
    "cv2.setNumThreads",
    "ProcessPoolExecuter",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: true
---

ffmpeg \
 -loop 1 \
 -r 30000/1001 \
 -i input_picture.png -i input_audio.mp3 \
 -vcodec libx264 \
 -acodec aac -strict experimental -ab 320k -ac 2 -ar 48000 \
 -pix_fmt yuv420p \
 -shortest \
 output.mp4

ffmpeg -loop 1 -i ima.jpg -i audio.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out.mp4

ffmpeg -i _.mp4 -i _.wav -c:v copy -c:a aac -strict experimental -map 0:v -map 1:a output.mp4
ffmpeg -i "video.mp4" -i "audio.mp3" -vcodec copy -acodec copy "my_video.mp4"
ffmpeg -i INPUT_FILE.mp4 -i AUDIO.wav -c:v copy -c:a aac OUTPUT_FILE.mp4


https://dev.classmethod.jp/articles/ffmpeg-create-movie-by-audio/
https://superuser.com/questions/1137612/ffmpeg-replace-audio-in-video
https://moriyoshi.hatenablog.com/entry/2015/12/17/224127