import logging
import urllib.parse
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_youtube_resources(query: str, limit: int = 5) -> List[Dict]:
    """
    Searches YouTube for resources with robust error handling and fallback.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        List of video metadata dictionaries
    """
    logger.info(f"Searching YouTube for: {query}")
    
    # Try yt-dlp first with timeout protection
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'playlist_items': f'1-{limit}',
            'socket_timeout': 10,  # 10 second timeout
            'retries': 2,
            'fragment_retries': 2,
        }
        
        results = []
        
        # Use timeout to prevent hanging
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch{limit}:{query}"
                info = ydl.extract_info(search_query, download=False)
                
                if 'entries' in info and info['entries']:
                    for entry in info['entries']:
                        if not entry:
                            continue
                        
                        # Calculate popularity score
                        views = entry.get('view_count', 0) or 0
                        likes = entry.get('like_count', 0) or 0
                        popularity_score = views + (likes * 10)
                        
                        # Extract description safely
                        description = entry.get('description', '') or ''
                        if description:
                            description = description[:200]
                        
                        res = {
                            'title': entry.get('title', 'Untitled Video'),
                            'url': entry.get('webpage_url', ''),
                            'views': views,
                            'likes': likes,
                            'uploader': entry.get('uploader', 'Unknown'),
                            'duration': entry.get('duration', 0),
                            'description': description,
                            'popularity_score': popularity_score
                        }
                        results.append(res)
            
            # Sort by popularity
            if results:
                results.sort(key=lambda x: x['popularity_score'], reverse=True)
                logger.info(f"Successfully found {len(results)} YouTube videos")
                return results
            else:
                logger.warning("yt-dlp returned no results, using fallback")
                
        except Exception as yt_error:
            logger.error(f"yt-dlp extraction error: {yt_error}")
            
    except ImportError:
        logger.error("yt-dlp not installed, using fallback")
    except Exception as e:
        logger.error(f"Unexpected error with yt-dlp: {e}")
    
    # Fallback: Return curated search URL with mock data
    logger.info("Using fallback: generating YouTube search URL")
    return generate_fallback_results(query, limit)

def generate_fallback_results(query: str, limit: int = 5) -> List[Dict]:
    """
    Generates fallback results when YouTube search fails.
    Returns a single result pointing to YouTube search.
    """
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    # Return a helpful fallback result
    return [{
        'title': f"Search YouTube: {query}",
        'url': search_url,
        'views': 0,
        'likes': 0,
        'uploader': 'YouTube',
        'duration': 0,
        'description': f"Click to search YouTube for '{query}'. The automated video search is temporarily unavailable, but this link will take you directly to relevant results.",
        'popularity_score': 0
    }]

def get_curated_resource(subject: str, level: str = "Beginner") -> Optional[Dict]:
    """
    Returns curated, high-quality resources for common subjects.
    This serves as a backup when automated search fails.
    """
    # Curated resources for common subjects
    curated = {
        "python": {
            "Beginner": {
                'title': "Python for Beginners - Full Course",
                'url': "https://www.youtube.com/watch?v=rfscVS0vtbw",
                'uploader': "freeCodeCamp.org",
                'description': "Learn Python basics in this comprehensive beginner-friendly tutorial."
            },
            "Intermediate": {
                'title': "Intermediate Python Programming Course",
                'url': "https://www.youtube.com/watch?v=HGOBQPFzWKo",
                'uploader': "freeCodeCamp.org",
                'description': "Take your Python skills to the next level with intermediate concepts."
            }
        },
        "javascript": {
            "Beginner": {
                'title': "JavaScript Tutorial for Beginners",
                'url': "https://www.youtube.com/watch?v=W6NZfCO5SIk",
                'uploader': "Programming with Mosh",
                'description': "Learn JavaScript fundamentals in this complete beginner course."
            }
        },
        "react": {
            "Beginner": {
                'title': "React Course - Beginner's Tutorial",
                'url': "https://www.youtube.com/watch?v=bMknfKXIFA8",
                'uploader': "freeCodeCamp.org",
                'description': "Learn React from scratch in this comprehensive tutorial."
            }
        }
    }
    
    subject_lower = subject.lower()
    if subject_lower in curated and level in curated[subject_lower]:
        resource = curated[subject_lower][level]
        resource['views'] = 1000000  # Mock high views
        resource['likes'] = 50000
        resource['duration'] = 3600
        resource['popularity_score'] = 1500000
        return resource
    
    return None

if __name__ == "__main__":
    # Quick test
    test_results = search_youtube_resources("react hooks tutorial", limit=3)
    for i, r in enumerate(test_results):
        print(f"{i+1}. {r['title']} - Views: {r['views']}, URL: {r['url']}")
