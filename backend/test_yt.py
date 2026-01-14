from youtubesearchpython import VideosSearch
import json

def test_search(query):
    videosSearch = VideosSearch(query, limit = 5)
    results = videosSearch.result()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    test_search("react tutorial for beginners")
