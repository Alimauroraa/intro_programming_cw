import pandas as pd
from data_model import Admin
# Read the CSV file into a DataFrame
admin_df = pd.read_csv('admin_credentials.csv')
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

def AdminLogIn(username,password):
    user = admin_df[(admin_df['username'] == username) & (admin_df['password'] == password)]
    if not user.empty:
        print("Access granted",username,"!")
    else:
        print("The username or password you have entered is wrong.")

AdminLogIn("admin",111)

def DisplayVolunteers(csv):
    """This is a function which takes a csv and displays it - for the purpose of displaying the Volunteer credentials csv file """
    for index, row in csv.iterrows():
        print(row)

DisplayVolunteers(admin_df)


