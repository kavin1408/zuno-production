import json
from main import validate_youtube_url

def test_youtube_validation():
    print("\nTesting YouTube URL Validation...")
    
    # Valid embed URL
    valid_url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    print(f"Checking valid URL: {valid_url}")
    assert validate_youtube_url(valid_url) == True
    
    # Invalid ID length
    invalid_id = "https://www.youtube.com/embed/short"
    print(f"Checking invalid ID (short): {invalid_id}")
    assert validate_youtube_url(invalid_id) == False
    
    # Not an embed URL
    watch_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"Checking watch URL: {watch_url}")
    assert validate_youtube_url(watch_url) == False
    
    print("YouTube URL Validation Tests Passed!")

def test_fallback_logic_simulation():
    print("\nSimulating Fallback Logic...")
    
    # Mock resources data from AI
    resources_data = [
        {
            "title": "Python Tutorial",
            "url": "https://www.youtube.com/embed/invalid_id",
            "platform": "YouTube",
            "resource_type": "video",
            "video_confidence": "high"
        }
    ]
    
    task_topic = "Python Basics"
    
    # Simulate the logic in main.py
    for res in resources_data:
        url = res.get("url", "")
        confidence = res.get("video_confidence", "fallback")
        validated = False
        fallback_used = False

        if confidence == "high" and "youtube.com/embed/" in url:
            if validate_youtube_url(url):
                validated = True
            else:
                # Downgrade to fallback search
                search_term = res.get("title", task_topic).replace(" ", "+")
                url = f"https://www.youtube.com/results?search_query={search_term}"
                confidence = "fallback"
                fallback_used = True
        
        print(f"Result - URL: {url}, Confidence: {confidence}, Fallback Used: {fallback_used}")
        assert confidence == "fallback"
        assert fallback_used == True
        assert "results?search_query=" in url

    print("Fallback Logic Simulation Passed!")

if __name__ == "__main__":
    try:
        test_youtube_validation()
        test_fallback_logic_simulation()
        print("\nAll Backend YouTube Strategy tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
