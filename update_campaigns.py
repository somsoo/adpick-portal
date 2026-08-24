import os
import requests
import json
from datetime import datetime

API_URL = "https://adpick.co.kr/apis/offers.php?affid=7440c8"

CATEGORY_MAP = {
    "1": "게임",
    "2": "쇼핑",
    "3": "교육",
    "4": "생활",
    "5": "웹툰"
}

def fetch_adpick_campaigns():
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        
        # Some PHP APIs return empty string or non-JSON if no data, let's be safe
        text_data = response.text.strip()
        if not text_data:
            return []
            
        data = response.json()
        
        campaigns = []
        for item in data:
            cat_code = str(item.get("apCategory", ""))
            cat_name = CATEGORY_MAP.get(cat_code, "기타")
            
            # Prefer wide banners, fallback to icon
            images = item.get("apImages", {})
            image_url = (
                images.get("banner1024x500") or 
                images.get("banner640x640") or 
                images.get("banner640x960") or 
                images.get("icon256") or 
                images.get("icon", "")
            )
            
            campaign = {
                "id": item.get("apOffer", ""),
                "title": item.get("apAppTitle", "제목 없음"),
                "description": item.get("apHeadline", ""),
                "image_url": image_url,
                "category": cat_name,
                "click_url": item.get("apTrackingLink", "#")
            }
            campaigns.append(campaign)
        
        return campaigns
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return []

def main():
    campaigns = fetch_adpick_campaigns()
    
    if campaigns:
        with open('campaigns.json', 'w', encoding='utf-8') as f:
            json.dump(campaigns, f, ensure_ascii=False, indent=4)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully updated campaigns.json with {len(campaigns)} campaigns.")
    else:
        print("No campaigns fetched or API returned empty.")

if __name__ == "__main__":
    main()
