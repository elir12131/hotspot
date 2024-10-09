from flask import Flask, request, jsonify, send_file
import os
import yt_dlp as ytdlp
import shutil

app = Flask(__name__)

# Directory where files will be stored
DOWNLOAD_DIR = 'downloads'
FFMPEG_PATH = 'C:\\Users\\roitb\\Downloads\\ffmpeg-n7.0-latest-win64-gpl-7.0\\ffmpeg-n7.0-latest-win64-gpl-7.0\\bin\\ffmpeg.exe'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return '''
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="Enter playlist URL" required>
            <button type="submit">Download Playlist</button>
        </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

    # Download and convert to MP3 with thumbnail
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-id3v2_version', '3',
            '-metadata', 'title=%(title)s',
            '-metadata', 'artist=%(artist)s'
        ],
        'ffmpeg_location': FFMPEG_PATH,
        'writethumbnail': True,
    }

    with ytdlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Return the downloaded file (for simplicity, we're just showing the first file)
    files = os.listdir(DOWNLOAD_DIR)
    if files:
        return send_file(os.path.join(DOWNLOAD_DIR, files[0]), as_attachment=True)

    return 'No files downloaded.'

if __name__ == '__main__':
    app.run(debug=True)
