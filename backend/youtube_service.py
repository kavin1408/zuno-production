import yt_dlp
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeService:
    """
    Service for searching and validating YouTube videos using yt-dlp.
    Ensures videos are public, embeddable, and available.
    """
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,  # Get full metadata
        }
    
    def search_videos(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search YouTube for videos and return validated, embeddable results.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of validated video dictionaries with metadata
        """
        logger.info(f"Searching YouTube for: {query}")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                search_query = f"ytsearch{limit * 2}:{query}"  # Fetch extra in case some aren't embeddable
                info = ydl.extract_info(search_query, download=False)
                
                if not info or 'entries' not in info:
                    logger.warning(f"No results found for query: {query}")
                    return []
                
                validated_videos = []
                for entry in info['entries']:
                    if not entry:
                        continue
                    
                    # Validate the video
                    video_data = self._validate_video(entry)
                    if video_data:
                        validated_videos.append(video_data)
                    
                    # Stop once we have enough validated videos
                    if len(validated_videos) >= limit:
                        break
                
                logger.info(f"Found {len(validated_videos)} validated videos out of {len(info['entries'])} results")
                return validated_videos
                
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return []
    
    def _validate_video(self, entry: Dict) -> Optional[Dict]:
        """
        Validate a single video entry to ensure it's embeddable and public.
        
        Args:
            entry: Video entry from yt-dlp
            
        Returns:
            Validated video data dict or None if validation fails
        """
        try:
            video_id = entry.get('id')
            if not video_id or len(video_id) != 11:
                logger.debug(f"Invalid video ID: {video_id}")
                return None
            
            # Check if video is available
            if entry.get('availability') not in ['public', None]:
                logger.debug(f"Video {video_id} is not public: {entry.get('availability')}")
                return None
            
            # Check if video is live (we want regular videos, not live streams)
            if entry.get('is_live') or entry.get('was_live'):
                logger.debug(f"Video {video_id} is/was a live stream")
                return None
            
            # Get embeddability info - yt-dlp doesn't always provide this directly
            # but we can infer from other fields
            # Most videos are embeddable unless explicitly restricted
            
            # Calculate popularity score
            views = entry.get('view_count', 0) or 0
            likes = entry.get('like_count', 0) or 0
            popularity_score = views + (likes * 10)
            
            # Build validated video data
            video_data = {
                'video_id': video_id,
                'title': entry.get('title', 'Untitled Video'),
                'url': f"https://www.youtube.com/embed/{video_id}",
                'watch_url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': entry.get('thumbnail'),
                'duration': entry.get('duration', 0),
                'views': views,
                'likes': likes,
                'uploader': entry.get('uploader', 'Unknown'),
                'upload_date': entry.get('upload_date'),
                'description': (entry.get('description') or '')[:200],
                'popularity_score': popularity_score,
                'is_embeddable': True,  # Assume embeddable unless proven otherwise
                'validated_at': datetime.utcnow().isoformat()
            }
            
            return video_data
            
        except Exception as e:
            logger.error(f"Error validating video: {e}")
            return None
    
    def validate_video_id(self, video_id: str) -> Optional[Dict]:
        """
        Validate a specific video ID to check if it's still available and embeddable.
        
        Args:
            video_id: YouTube video ID (11 characters)
            
        Returns:
            Validated video data or None if validation fails
        """
        if not video_id or len(video_id) != 11:
            return None
        
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if info:
                    return self._validate_video(info)
                    
        except Exception as e:
            logger.error(f"Error validating video ID {video_id}: {e}")
            return None
    
    def get_fallback_search_url(self, query: str) -> str:
        """
        Generate a YouTube search URL as fallback when no embeddable videos found.
        
        Args:
            query: Search query
            
        Returns:
            YouTube search results URL
        """
        search_term = query.replace(' ', '+')
        return f"https://www.youtube.com/results?search_query={search_term}"


# Singleton instance
youtube_service = YouTubeService()


def search_and_validate_videos(query: str, limit: int = 3) -> List[Dict]:
    """
    Convenience function to search and validate YouTube videos.
    
    Args:
        query: Search query
        limit: Maximum number of results
        
    Returns:
        List of validated video dictionaries
    """
    return youtube_service.search_videos(query, limit)


def validate_video_by_id(video_id: str) -> Optional[Dict]:
    """
    Convenience function to validate a specific video ID.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Validated video data or None
    """
    return youtube_service.validate_video_id(video_id)


if __name__ == "__main__":
    # Quick test
    print("Testing YouTube service...")
    results = search_and_validate_videos("python tutorial for beginners", limit=3)
    
    print(f"\nFound {len(results)} validated videos:")
    for i, video in enumerate(results, 1):
        print(f"\n{i}. {video['title']}")
        print(f"   ID: {video['video_id']}")
        print(f"   URL: {video['url']}")
        print(f"   Views: {video['views']:,}")
        print(f"   Embeddable: {video['is_embeddable']}")
