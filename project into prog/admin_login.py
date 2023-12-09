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

