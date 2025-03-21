from flet import Page, SnackBar, Text
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



def login_or_register(e, email, password, BASE_URL, page, loader):
    show_loader(page, loader)
    action = e.control.data  # login or register
    #print(action)
    url = f"{BASE_URL}custom_login/"  # allauth login URL
    user_data={
                    "email":email,
                    "password": password
                    
                }
    if action == "signup":
        url = f"{BASE_URL}custom_signup/"  # allauth login and register urls
        user_timezone="UTC"
        try:
            from tzlocal import get_localzone  # Import tzlocal

            # Detect time zone using tzlocal
            local_timezone = str(get_localzone())
            timezone = local_timezone  # Add timezone to user_data
        except:
            pass
        user_data={
                    "email":email,
                    "password1": password,
                    "password2": password,
                    "timezone":timezone
                }
    try:
        with httpx.Client() as client:
            # Get CSRF token
            csrf_response = client.get(f"{BASE_URL}accounts/login/")
            if action=="Register":
                csrf_response = client.get(f"{BASE_URL}accounts/signup/")
            #print(csrf_response.cookies) #check cookies.
            csrf_token = csrf_response.cookies.get("csrftoken")
            if csrf_token: #check if csrf_token is not None.
                headers = {"X-CSRFToken": csrf_token}
            else:
                print("CSRF token not found.")
                return #or raise an exception.
            client.cookies.update(csrf_response.cookies) #update the clients cookies.
            user_data["csrfmiddlewaretoken"]=csrf_token
            response = client.post(
                url,
                data=user_data,
                headers=headers
            )
            #response.raise_for_status()
            # Check for redirect (successful login/registration)
            hide_loader(page, loader)
            if response.status_code == 200:
                print(f"{action.capitalize()} successful!")
                if action=="login":
                    data=response.json()
                    token = data["api_key"]
                    page.client_storage.set("burnison.me.user.token", token)
                    page.go("/bills")
                else:
                    page.open(SnackBar(Text(f"Registration successful!  You can now log in.")))
            elif response.status_code == 400:
                #print(response)
                data=response.json()
                if "errors" in data:
                    print(data["errors"])
                    try:
                        django_response = data["errors"]
                        if "non_field_errors" in django_response:
                            error_message = django_response["non_field_errors"]
                            print(f"{action.capitalize()} failed: {error_message[0]}")
                            page.open(SnackBar(Text(f"{error_message[0]}")))
                        elif "email" in django_response:
                            error_message = django_response["email"]
                            print(f"{action.capitalize()} failed: {error_message[0]}")
                            page.open(SnackBar(Text(f"{error_message[0]}")))
                        else:
                            print(f"{action.capitalize()} failed.")
                            page.open(SnackBar(Text(f"{action.capitalize()} failed.")))
                        
                    except json.JSONDecodeError as e:
                        print(f"{action.capitalize()} failed. Unexpected server response: {e}")
                    page.update()
        
    except httpx.RequestError as err:
        hide_loader(page, loader)
        print(f"Error communicating with server: {err}")
        print(f"Server error: {err}")
        page.open(SnackBar(Text(f"Error communicating with server: {err}")))
        page.update()
    except httpx.HTTPStatusError as err:
        hide_loader(page, loader)
        print(f"HTTP Error: {err}")
        print(f"Server error: {err}")
        page.open(SnackBar(Text(f"HTTP Error: {err}")))
        page.update()
    except httpx.TimeoutException as err:
        hide_loader(page, loader)
        print(f"Timeout Error: {err}")
        print(f"Server error: {err}")
        page.open(SnackBar(Text(f"Timeout Error: {err}")))
        page.update()
    except Exception as err:
        hide_loader(page, loader)
        print(f"General Error: {err}")
        print(f"Server error: {err}")
        page.open(SnackBar(Text(f"General Error: {err}")))
        page.update()

