from pytube import YouTube, Playlist, exceptions, Channel
from datetime import timedelta
from flask import Flask, request, jsonify
import string
import random
import pytube.exceptions as PytubeException
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/trending": {"origins": "http://127.0.0.1:5500"}})


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
    yt = YouTube(url)
    title = str(yt.title).strip()
    return {
        'title': title,
        'views': str(format_number(int(yt.views))).strip(),
        'duration': format_duration(yt.length),
        'thumbnailURL': str(yt.thumbnail_url).strip(),
        'author': str(yt.author).strip(),
        #'Download URLs': [yt.streams.get_by_resolution()]
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

@app.route('/get_info', methods=['POST'])
def main():
    data = request.json
    url = data.get('url', '')
    if "watch?v=" in url:
        return get_video_info(url)
    elif "playlist?list=" in url:
        return get_playlist_info(url)
    else:
        "error"

@app.route('/trending', methods=['POST'])
def trending():
    try:
        channel = Channel('https://www.youtube.com/feed/trending')
        videos = list(channel.videos)
        first_eight_videos = videos[:8]
        return first_eight_videos
    except:
        videos = [
            'https://www.youtube.com/watch?v=9p5Tokd-93k',
            'https://www.youtube.com/watch?v=sjkrrmBnpGE',
            'https://www.youtube.com/watch?v=MYPVQccHhAQ',
            'https://www.youtube.com/watch?v=s2-WLE2trA8',
            'https://www.youtube.com/watch?v=zhDwjnYZiCo',
            'https://www.youtube.com/watch?v=xDih5SwFs_c',
            'https://www.youtube.com/watch?v=O5p2ZX7UU9w',
            'https://www.youtube.com/watch?v=s_otoFg8qGY',
        ]
        trends = []
        for i in videos:
            info = get_video_info(i)
            info['url'] = i
            title = info['title']
            if len(title) > 33:
                title = title[0:33]
                title = f"{title} ......"
            info['title'] = title
            trends.append(info)
        return {'trending': trends}

if __name__ == "__main__":
    app.run(debug=True)