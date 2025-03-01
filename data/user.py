from flet import Page
import httpx
import json
from ui.alert import show_loader, hide_loader

def login(page: Page, code: str, BASE_URL: str, loader):
        show_loader(page, loader)
        # Send the login code to your server to retrieve the user ID
        response = httpx.post(f"{BASE_URL}data/temp_code/", json={"code": code})
        if response.status_code == 200:
            try:
                user_data = response.json()
                print(user_data)
                user_id = user_data["user_id"]
                token = user_data['token']
                page.client_storage.set("burnison.me.user.id", user_id)
                page.client_storage.set("burnison.me.user.token", token)
                # Process user ID and update Flet app UI
                print(f"Welcome, user {user_id}")
                page.go("/bills")
                
            except (KeyError, json.JSONDecodeError):
                # Handle error parsing the response
                print("Error: Invalid response from server")
        else:
            # Handle failed login attempt
            print(f"Error: {response.status_code}")
            hide_loader(page, loader)