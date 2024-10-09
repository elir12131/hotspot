from flask import Flask, request, render_template_string
from yt_dlp import YoutubeDL
import threading
import webbrowser
import time

app = Flask(__name__)

# HTML template for the web interface
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>YouTube Playlist Downloader</title>
  </head>
  <body>
    <h1>YouTube Playlist Downloader</h1>
    <form action="/download" method="post">
      <label for="url">YouTube Playlist URL:</label>
      <input type="text" id="url" name="url" required>
      <input type="submit" value="Download">
    </form>
    {% if message %}
    <p>{{ message }}</p>
    {% endif %}
  </body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'embedthumbnail': True,
        'addmetadata': True,
        'ffmpeg_location': 'ffmpeg'  # Adjust this path if necessary
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        message = 'Playlist downloaded successfully!'
    except Exception as e:
        message = f'An error occurred: {e}'
    
    return render_template_string(html_template, message=message)

def run_app():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    threading.Thread(target=run_app).start()
    
    # Give the server a moment to start
    time.sleep(2)
    
    # Open the URL in the default web browser
    webbrowser.open('http://127.0.0.1:80')
