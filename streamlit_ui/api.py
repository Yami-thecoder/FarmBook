import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("FARMBOOK_API_URL", "http://127.0.0.1:5000")

def register_user(username, email, password):
    response = requests.post(f"{API_URL}/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    return response.json(), response.status_code

def login_user(email, password):
    response = requests.post(f"{API_URL}/login", json={
        "email": email,
        "password": password
    })
    return response.json(), response.status_code

def fetch_profit_trend(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/analytics/profit-trend", headers=headers)
    return response.json() if response.status_code == 200 else None

def fetch_crop_comparison(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/analytics/crop-comparison", headers=headers)
    return response.json() if response.status_code == 200 else None

def fetch_cost_breakdown(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/analytics/cost-breakdown", headers=headers)
    return response.json() if response.status_code == 200 else None

def export_pdf_report(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/export/pdf", headers=headers)
    return response.content if response.status_code == 200 else None

def fetch_journal_entries(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/journal", headers=headers)
    return response.json() if response.status_code == 200 else None

def add_journal_entry(jwt_token, crop_name, season, farm_location, sowing_date, harvest_date, yield_amount, sold_amount, unit_price, expenses, notes):
    headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
    data = {
        "crop_name": crop_name,
        "season": season,
        "farm_location": farm_location,
        "sowing_date": str(sowing_date),
        "harvest_date": str(harvest_date),
        "yield_amount": yield_amount,
        "sold_amount": sold_amount,
        "unit_price": unit_price,
        "expenses": expenses,
        "notes": notes
    }
    response = requests.post(f"{API_URL}/journal", json=data, headers=headers)

    try:
        response_json = response.json()  # Ensure response is valid JSON
    except requests.exceptions.JSONDecodeError:
        return False, {"error": "Invalid JSON response from API"}

    return response.status_code == 201, response_json  # Return status & data




def update_journal_entry(jwt_token, entry_id, crop_name, season, farm_location, sowing_date, harvest_date, yield_amount, sold_amount, unit_price, expenses, notes):
    headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
    data = {
        "crop_name": crop_name,
        "season": season,
        "farm_location": farm_location,
        "sowing_date": str(sowing_date),
        "harvest_date": str(harvest_date),
        "yield_amount": yield_amount,
        "sold_amount": sold_amount,
        "unit_price": unit_price,
        "expenses": expenses,
        "notes": notes
    }
    response = requests.put(f"{API_URL}/journal/{entry_id}", json=data, headers=headers)
    return response.status_code == 200


def delete_journal_entry(jwt_token, entry_id):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.delete(f"{API_URL}/journal/{entry_id}", headers=headers)
    return response.status_code == 200


# Fetch Posts
def fetch_posts(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{API_URL}/posts", headers=headers)
    return response.json() if response.status_code == 200 else None

# Fetch text file content
def fetch_text_file(file_url):
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        return f"⚠️ Error loading file: {e}"
    return None

# Create Post
def create_post(jwt_token, title, description, file):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {"title": title.strip(), "description": description.strip()}

    if description:
        word_count = len(description.split())
        if word_count > 200:
            return {"error": "Description exceeds 200 words"}, 400  # ✅ Server-side validation

    files = {"file": (file.name, file.getvalue())} if file else None  
    response = requests.post(f"{API_URL}/posts", headers=headers, data=data, files=files)
    
    return response.json() if response.status_code == 201 else None


# Like a Post
def like_post(jwt_token, post_id):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.post(f"{API_URL}/posts/{post_id}/like", headers=headers)
    return response.status_code == 200

# Comment on a Post
def comment_on_post(jwt_token, post_id, content):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.post(f"{API_URL}/posts/{post_id}/comment", headers=headers, json={"content": content})
    return response.status_code == 201
