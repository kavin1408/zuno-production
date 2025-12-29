import yt_dlp
import json

def test_yt_dlp_metrics(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False, # Get full info
        'force_generic_extractor': False,
        'playlist_items': '1,2,3', # Top 3
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f"ytsearch3:{query}"
        info = ydl.extract_info(search_query, download=False)
        results = []
        if 'entries' in info:
            for entry in info['entries']:
                res = {
                    'title': entry.get('title'),
                    'url': entry.get('webpage_url'),
                    'views': entry.get('view_count'),
                    'likes': entry.get('like_count'),
                    'duration': entry.get('duration'),
                    'uploader': entry.get('uploader')
                }
                results.append(res)
            print(json.dumps(results, indent=2))
        else:
            print("No entries found")

if __name__ == "__main__":
    test_yt_dlp_metrics("react tutorial")
