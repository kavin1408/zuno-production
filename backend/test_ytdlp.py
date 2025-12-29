import yt_dlp
import json

def test_yt_dlp_search(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search for top 3 videos
        search_query = f"ytsearch3:{query}"
        info = ydl.extract_info(search_query, download=False)
        if 'entries' in info:
            entries = info['entries']
            print(json.dumps(entries, indent=2))
        else:
            print("No entries found")

if __name__ == "__main__":
    test_yt_dlp_search("react tutorial")
