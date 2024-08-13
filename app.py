from pytube import YouTube, Playlist
from datetime import timedelta

def format_duration(duration):
    """Converts seconds to HH:MM:SS format."""
    return str(timedelta(seconds=duration))

def get_youtube_info(url):
    is_playlist = 'list=' in url
    try:
        if is_playlist:
            p = Playlist(url)
            # Fetch playlist title correctly
            playlist_title = p.title
            total_duration = sum([YouTube(video_url).length for video_url in p.video_urls])
            return {
                'Title': playlist_title,
                'Duration': format_duration(total_duration),
                'Thumbnail URL': p.video_urls[0] if p.video_urls else 'No videos in playlist',
                'Video URLs in Playlist': p.video_urls
            }
        else:
            yt = YouTube(url)
            return {
                'Title': yt.title,
                'Views': yt.views,
                'Duration': format_duration(yt.length),
                'Thumbnail URL': yt.thumbnail_url,
                'Author Name': yt.author,
                'Download URLs': [yt.streams.get_by_resolution()]
            }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example URL (change as needed)
url = 'https://www.youtube.com/watch?v=s2-WLE2trA8'
info = get_youtube_info(url)
if info:
    print(info)
else:
    print("Failed to retrieve information.")