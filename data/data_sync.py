from flet import Page, dropdown
import httpx
import json
import asyncio
from datetime import datetime

def updateData(page: Page):
     isUpdate = False
     update_frequency = page.client_storage.get("update_frequency") if page.client_storage.get("update_frequency") is not None else  "Once a day(default)"
     last_updated = page.client_storage.get("last_updated").split(".")[0] if page.client_storage.get("last_updated") is not None else None
     if last_updated is None:
          print("last updated is None")
          page.client_storage.set("last_updated", str(datetime.now()))
          isUpdate = True
     elif update_frequency == "Once a day(default)":
          print("once a day")
          if datetime.now().day != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").day:
               isUpdate = True
     elif update_frequency == "Once a week":
          print("once a week")
          if datetime.now().isocalendar()[1] != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").isocalendar()[1]:
               isUpdate = True
     elif update_frequency == "Once a month":
          print("once a month")
          if datetime.now().month != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").month:
               isUpdate = True
     else:
          print("else statement")
          isUpdate = True
     return isUpdate
     
async def get_bills(page: Page, user_id: str, BASE_URL: str):
     my_data=page.client_storage.get("my_bills")
     my_profile_pic=page.client_storage.get("profile_pic")
     
     if my_data is None or my_data == "" or updateData(page):
          data = {"userId": user_id}  # Include user ID in the request data
          response = httpx.post(f"{BASE_URL}flet_login", json=data)
          if response.status_code == 200:
                 try: 
                    print("successfully fetched user and bills data") 
                    user_bills_data = response.json()  
                    user_data = user_bills_data['user']  
                    if user_data == "no bills":
                         return {"error": "no bills"}
                    else:
                         user_pay_hours = []
                         profile = user_data[0]
                         profile_pic = profile['image_url']
                         avg_pay = profile['avg_pay']
                         forty_hours = profile['forty_hour']
                         other_hours = profile['other_hours']
                         other_hours = json.loads(other_hours)
                         if forty_hours != None:
                              forty_hours = forty_hours.replace('$', '')
                              user_pay_hours.append(dropdown.Option(f"40 Hours: ${forty_hours}"),)
                         if avg_pay != None:
                              avg_pay = avg_pay.replace('$', '')
                              user_pay_hours.append(dropdown.Option(f"Average Pay: ${avg_pay}"),)
                         if other_hours != None:
                              if len(other_hours) > 0:
                                   for pay_detail in other_hours:
                                        user_pay_hours.append(dropdown.Option(f"{pay_detail['hours']} Hours: {pay_detail['amount']}"),)
                        
                         my_bills = user_data[1]
                         unpaid_bills = user_data[2] if len(user_data) > 2 else []

                         print("from server")
                         page.client_storage.set("my_bills",{"my_bills":my_bills, "unpaid_bills":unpaid_bills})
                         page.client_storage.set("profile_pic", profile_pic)
                         return dict(profile_pic=profile_pic, my_bills=my_bills, unpaid_bills=unpaid_bills, error="")
                 except (KeyError, json.JSONDecodeError):
                    # Handle error parsing the response
                    print("Error: Invalid response from server")
          else:
            # Handle failed login attempt
            print(f"Error: {response.status_code}")
     else:
          #user_pay_hours=user_pay_hours, my_bills=my_bills, unpaid_bills=unpaid_bills
          print("from storage")
          return dict(profile_pic=my_profile_pic, my_bills=my_data["my_bills"], unpaid_bills=my_data["unpaid_bills"], error="")
                 

def save_unpaid_bills(page: Page, unpaid_bills, BASE_URL: str):
     response = httpx.post(f"{BASE_URL}add_unpaid", json={"unpaid": unpaid_bills})
     return response

def remove_unpaid_bills(page: Page, unpaid_bills, BASE_URL: str):         
     response = httpx.post(f"{BASE_URL}remove_past_due", json={"past_due": unpaid_bills})
     print(response)

def add_update_bills(page: Page, BASE_URL: str, data):
     
     response = httpx.post(f"{BASE_URL}data/add_bill", json=data)
     if response.status_code == 200:
          print(response)
          return "success"
     else:
          return "error"
     
def remove_bill_item(page: Page, BASE_URL: str, data):
     
     response = httpx.post(f"{BASE_URL}data/remove_bill", json=data)
     if response.status_code == 200:
          print(response)
          return "success"
     else:
          return "error"
     
def add_update_earnings(page: Page, BASE_URL: str, data):
     
     response = httpx.post(f"{BASE_URL}data/earnings", json=data)
     if response.status_code == 200:
          print(response)
          return dict(data=response, error=None)
     else:
          return dict(data=None, error=f"HTTP Error: {response.status_code}")
     
async def get_earnings(page:Page, BASE_URL:str, user_id:str):
     async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}data/earnings/{user_id}")
        if response.status_code == 200:
            return dict(data=response.json(), error=None)
        else:
            return dict(data=None, error=f"HTTP Error: {response.status_code}")

async def delete_earning(BASE_URL: str, id, user_id):
     async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}data/earnings/{id}/{user_id}")
        if response.status_code == 200:
            return dict(data=response.json(), error=None)
        else:
            return dict(data=None, error=f"HTTP Error: {response.status_code}")