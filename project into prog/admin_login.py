
# Read the CSV file into a DataFrame

# class InvalidLogin(Exception):
#     """This is an exception handling class that rejects incorrect usernames. Made by stella 06/11/23"""
#     pass
# try:
#     matching_credentials = admin_df[(admin_df['username'] == username) & (admin_df['password'] == password)]
#     if not matching_credentials.empty:
#         pass
#     else:
#         raise InvalidLogin
# except:
#     print("Exception occurred: the username or password you have entered is wrong.")



import pandas as pd

admin_df = pd.read_csv('admin_credentials.csv')

class Admin:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.created_plans = []  # List of HumanitarianPlans created by this admin

    def AdminLogIn(self):
        while True:
            user = admin_df[(admin_df['username'] == self.username) & (admin_df['user_password'] == self.password)]
            if not user.empty:
                print("Access granted", self.username, "!")
                break
            else:
                print("The username or password you have entered is wrong.")
                self.username = input("Please re-enter your username: ")
                self.password = int(input("Please re-enter your password: "))

