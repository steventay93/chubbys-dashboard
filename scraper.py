import requests
import streamlit as st
import time

APIFY_API_KEY = st.secrets.get("APIFY_API_KEY", "")

COMPETITOR_ACCOUNTS = [
    {"name": "Howlin' Ray's", "handle": "howlinrays"},
    {"name": "Angry Chickz", "handle": "theangrychickz"},
    {"name": "Dave's Hot Chicken", "handle": "daveshotchicken"},
    {"name": "Hattie B's", "handle": "hattiebshot"},
    {"name": "Legend Hot Chicken", "handle": "legendhotchicken"},
]

def run_apify_actor(actor_id, run_input, timeout=120):
    """Run an Apify actor and return results."""
    if not APIFY_API_KEY:
        return None, "No API key configured"

    # Start the actor run
    url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_API_KEY}"
    response = requests.post(url, json=run_input, timeout=30)

    if response.status_code not in [200, 201]:
        return None, f"Failed to start actor: {response.status_code} {response.text}"

    run_data = response.json()
    run_id = run_data.get("data", {}).get("id")
    if not run_id:
        return None, "No run ID returned"

    # Poll for completion
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_API_KEY}"
    start_time = time.time()

    while time.time() - start_time < timeout:
        status_resp = requests.get(status_url, timeout=10)
        status = status_resp.json().get("data", {}).get("status", "")
        if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
            break
        time.sleep(3)

    if status != "SUCCEEDED":
        return None, f"Actor run ended with status: {status}"

    # Get results
    dataset_id = status_resp.json().get("data", {}).get("defaultDatasetId")
    results_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_API_KEY}&limit=50"
    results_resp = requests.get(results_url, timeout=30)
    return results_resp.json(), None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_competitor_reels(handles: list):
    """Fetch recent posts from competitor accounts using Apify Instagram Post Scraper."""
    all_reels = []

    for handle in handles:
        run_input = {
            "username": [handle],
            "resultsLimit": 4,
        }

        results, error = run_apify_actor("apify~instagram-post-scraper", run_input, timeout=180)

        if error:
            continue  # skip failed accounts, try next

        for item in (results or []):
            reels = {
                "id": item.get("id", ""),
                "shortcode": item.get("shortCode", ""),
                "owner": item.get("ownerUsername", handle),
                "caption": (item.get("caption") or "")[:120],
                "likes": item.get("likesCount", 0),
                "comments": item.get("commentsCount", 0),
                "plays": item.get("videoViewCount", 0),
                "timestamp": item.get("timestamp", ""),
                "thumbnail": item.get("displayUrl", ""),
                "url": f"https://www.instagram.com/p/{item.get('shortCode', '')}/",
                "is_video": item.get("isVideo", False),
                "type": item.get("type", ""),
            }
            all_reels.append(reels)

    # Sort by plays/likes descending
    all_reels.sort(key=lambda x: (x["plays"] or 0) + (x["likes"] or 0) * 10, reverse=True)
    return all_reels, None


@st.cache_data(ttl=3600)
def fetch_chubbys_posts():
    """Fetch Chubby's own posts for analytics."""
    run_input = {
        "username": ["chubbyschicken"],
        "resultsLimit": 12,
    }

    results, error = run_apify_actor("apify~instagram-post-scraper", run_input, timeout=180)
    if error:
        return [], error

    posts = []
    for item in (results or []):
        posts.append({
            "shortcode": item.get("shortCode", ""),
            "caption": (item.get("caption") or "")[:100],
            "likes": item.get("likesCount", 0),
            "comments": item.get("commentsCount", 0),
            "plays": item.get("videoViewCount", 0),
            "timestamp": item.get("timestamp", ""),
            "thumbnail": item.get("displayUrl", ""),
            "url": f"https://www.instagram.com/p/{item.get('shortCode', '')}/",
            "is_video": item.get("isVideo", False),
        })

    return posts, None
