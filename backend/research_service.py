import yt_dlp
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_youtube_resources(query, limit=5):
    """
    Searches YouTube for resources and returns metadata including views and likes.
    """
    logger.info(f"Searching YouTube for: {query}")
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'playlist_items': f'1-{limit}',
    }
    
    results = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch{limit}:{query}"
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info:
                for entry in info['entries']:
                    if not entry:
                        continue
                    
                    # Calculate a simple popularity score
                    views = entry.get('view_count', 0) or 0
                    likes = entry.get('like_count', 0) or 0
                    
                    # Heuristic: Combined metric (views + likes * 10)
                    # This can be refined
                    popularity_score = views + (likes * 10)
                    
                    res = {
                        'title': entry.get('title'),
                        'url': entry.get('webpage_url'),
                        'views': views,
                        'likes': likes,
                        'uploader': entry.get('uploader'),
                        'duration': entry.get('duration'),
                        'description': entry.get('description')[:200] if entry.get('description') else "",
                        'popularity_score': popularity_score
                    }
                    results.append(res)
        
        # Sort by popularity score descending
        results.sort(key=lambda x: x['popularity_score'], reverse=True)
        return results
        
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return []

if __name__ == "__main__":
    # Quick test
    test_results = search_youtube_resources("react hooks tutorial", limit=3)
    for i, r in enumerate(test_results):
        print(f"{i+1}. {r['title']} - Views: {r['views']}, Likes: {r['likes']}, Score: {r['popularity_score']}")
