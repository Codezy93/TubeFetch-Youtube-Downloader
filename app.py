from pytubefix import YouTube, Playlist, exceptions, Channel
from datetime import timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for
import string
import random
import pytubefix.exceptions as PytubeException

app = Flask(__name__)

def format_number(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num/1000:.1f}K"
    elif num < 1000000000:
        return f"{num/1000000:.1f}M"
    else:
        return f"{num/1000000000:.1f}B"

def format_duration(duration):
    """Converts seconds to HH:MM:SS format."""
    return str(timedelta(seconds=duration))

def get_video_info(url):
    yt = YouTube(url, 'WEB_CREATOR')
    title = str(yt.title).strip()
    video_download_urls = {}
    for resolution in ['1080p', '720p', '480p', '360p', '240p', '144p']:
        stream = yt.streams.filter(res=resolution, progressive=True).first()
        if stream is None:
            stream = yt.streams.filter(res=resolution, only_video=True).first()
        if stream is not None:
            video_download_urls[resolution] = stream.url
    audio_download_url = yt.streams.filter(only_audio=True).first().url
    return {
        'title': title,
        'views': str(format_number(int(yt.views))).strip(),
        'duration': format_duration(yt.length),
        'thumbnailURL': str(yt.thumbnail_url).strip(),
        'author': str(yt.author).strip(),
        'Video Download URLs': video_download_urls,
        'Audio Download URL': audio_download_url
    }

def get_playlist_info(url):
    p = Playlist(url)
    playlist_title = p.title
    total_duration = sum([YouTube(video_url).length for video_url in p.video_urls])
    vids = p.video_urls
    video_urls = []
    for vid in vids:
        video_urls.append(get_video_info(vid))
    thumbnail = video_urls[0]['thumbnailURL']
    return {
        'title': playlist_title,
        'duration': format_duration(total_duration),
        'thumbnailURL': thumbnail,
        'videoURLs': video_urls    
    }

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/contact')
def contactpage():
    return render_template('contact.html')

@app.route('/video', methods=['POST', 'GET'])
def videopage():
    if request.method == "POST":
        url = request.form['link']
        data = get_video_info(url)
        return render_template('video.html', data=data)
    return render_template('video.html')

@app.route('/playlist')
def playlistpage():
    if request.method == "POST":
        url = request.form['link']
        data = get_playlist_info(url)
        return render_template('video.html', data=data)
    return render_template('playlist.html')

if __name__ == "__main__":
    app.run(debug=True)
    # print(get_video_info('https://www.youtube.com/watch?v=GHRXqyt6yzk'))