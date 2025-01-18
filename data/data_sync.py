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
          isUpdate = True
     elif update_frequency == "Once a day(default)":
          print("once a day", datetime.now().day, datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").day)
          if datetime.now().day != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").day:
               isUpdate = True
     elif update_frequency == "Once a week":
          print("once a week", datetime.now().isocalendar()[1], datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").isocalendar()[1])
          if datetime.now().isocalendar()[1] != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").isocalendar()[1]:
               isUpdate = True
     elif update_frequency == "Once a month":
          print("once a month", datetime.now().month, datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").month)
          if datetime.now().month != datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S").month:
               isUpdate = True
     else:
          print("else statement")
          isUpdate = True
     return True#isUpdate

class DataSync():
     def __init__(self, page:Page, BASE_URL, user_id):
          self.page = page
          self.BASE_URL = BASE_URL
          self.user_id = user_id
          self.my_bills=page.client_storage.get("my_bills")
          self.unpaid_bills=page.client_storage.get("unpaid_bills")
          self.profile_pic=page.client_storage.get("profile_pic")
          self.day_of_week=5
          
     async def get_bills(self):
     
     
          if self.my_bills is None or self.my_bills == "" or updateData(self.page):
               data = {"userId": self.user_id}  # Include user ID in the request data
               response = httpx.post(f"{self.BASE_URL}flet_login", json=data)
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
                              self.profile_pic = profile['image_url']
                              self.day_of_week = profile["day_of_week"]
                              self.my_bills = user_data[1]
                              self.unpaid_bills = user_data[2] if len(user_data) > 2 else []
                              
                              #print("from server")
                              self.page.client_storage.set("my_bills", self.my_bills)
                              self.page.client_storage.set("unpaid_bills", self.unpaid_bills)
                              self.page.client_storage.set("profile_pic", self.profile_pic if self.profile_pic is not None else "")
                              self.page.client_storage.set("last_updated", str(datetime.now()))
                              return dict(profile_pic=self.profile_pic, day_of_week=self.day_of_week, my_bills=self.my_bills, unpaid_bills=self.unpaid_bills, error="")
                    except (KeyError, json.JSONDecodeError):
                         print("Error: Invalid response from server")
               else:
                    print(f"Error: {response.status_code}")
          else:
               #user_pay_hours=user_pay_hours, my_bills=my_bills, unpaid_bills=unpaid_bills
               #print("from storage")
               return dict(profile_pic=self.profile_pic, day_of_week=self.day_of_week, my_bills=self.my_bills, unpaid_bills=self.unpaid_bills, error="")
                 

     def save_unpaid_bills(self, unpaid_bills):
          response = httpx.post(f"{self.BASE_URL}add_unpaid", json={"unpaid": unpaid_bills})
          return response, self.unpaid_bills

     def remove_unpaid_bills(self, unpaid_bills):         
          response = httpx.post(f"{self.BASE_URL}remove_past_due", json={"past_due": unpaid_bills})
          print(response)

     def add_update_bills(self, data):
          response = httpx.post(f"{self.BASE_URL}data/add_bill", json=data)
          if response.status_code == 200:
               print(response)
               return "success"
          else:
               return "error"
     
     def remove_bill_item(self, data):
     
          response = httpx.post(f"{self.BASE_URL}data/remove_bill", json=data)
          if response.status_code == 200:
               print(response)
               return "success"
          else:
               return "error"
     
     def add_update_earnings(self, data):
     
          response = httpx.post(f"{self.BASE_URL}data/earnings", json=data)
          if response.status_code == 200:
               print(response)
               return dict(data=response, error=None)
          else:
               return dict(data=None, error=f"HTTP Error: {response.status_code}")
     
     async def get_earnings(self):
          async with httpx.AsyncClient() as client:
               response = await client.get(f"{self.BASE_URL}data/earnings/{self.user_id}")
               if response.status_code == 200:
                    return dict(data=response.json(), error=None)
               else:
                    return dict(data=None, error=f"HTTP Error: {response.status_code}")

     async def delete_earning(self, id):
          async with httpx.AsyncClient() as client:
               response = await client.delete(f"{self.BASE_URL}data/earnings/{id}/{self.user_id}")
               if response.status_code == 200:
                    return dict(data=response.json(), error=None)
               else:
                    return dict(data=None, error=f"HTTP Error: {response.status_code}")
               
     def update_payday(self, data):
     
          response = httpx.post(f"{self.BASE_URL}data/day_of_week", json=data)
          if response.status_code == 200:
               print(response)
               return dict(data=response, error=None)
          else:
               return dict(data=None, error=f"HTTP Error: {response.status_code}")
     
     def logout(self):
          self.user_id = None
          self.my_bills=None
          self.unpaid_bills=None
          self.profile_pic=None
          self.day_of_week=5
          self.page.client_storage.remove("burnison.me.user.id")
          self.page.client_storage.remove("my_bills")
          self.page.client_storage.remove("unpaid_bills")
          self.page.client_storage.remove("profile_pic")
          self.page.go("/login")