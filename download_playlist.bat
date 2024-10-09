@echo off
REM Change directory to where yt-dlp.exe is located.
cd C:\Users\roitb\Downloads

REM Download the YouTube playlist, convert to MP3, and embed thumbnail as album art
yt-dlp.exe -x --audio-format mp3 --embed-thumbnail --add-metadata --ffmpeg-location C:\Users\roitb\Downloads\ffmpeg-n7.0-latest-win64-gpl-7.0\ffmpeg-n7.0-latest-win64-gpl-7.0\bin\ https://youtube.com/playlist?list=PLeCpuN-qM8IZiscl5qozLcCJv_dGUsWg-&si=9f3VCeQhYgNwluBv

pause
