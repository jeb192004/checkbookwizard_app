from flet import Page
import httpx
import json

def login(page: Page, code: str, BASE_URL: str):
        # Send the login code to your server to retrieve the user ID
        response = httpx.post(f"{BASE_URL}data/temp_code", json={"code": code})
        if response.status_code == 200:
            try:
                user_data = response.json()
                user = user_data["user"][0]
                user_id = user["userId"]
                page.client_storage.set("burnison.me.user.id", user_id)
                # Process user ID and update Flet app UI
                print(f"Welcome, user {user_id}")
                page.go("/")
                
            except (KeyError, json.JSONDecodeError):
                # Handle error parsing the response
                print("Error: Invalid response from server")
        else:
            # Handle failed login attempt
            print(f"Error: {response.status_code}")