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

    def DisplayVolunteers(csv):
        """This is a function which takes a csv and displays it - for the purpose of displaying the Volunteer credentials csv file """
        for index, row in csv.iterrows():
            print(row)

class HumanitarianPlan:
    def __init__(self, plan_id, description, geographical_area, start_date, closing_date=None):
        self.plan_id = plan_id
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.closing_date = closing_date
        self.camps = []  # List of Camps associated with this plan

class Camp:
    def __init__(self, camp_id, location, capacity):
        self.camp_id = camp_id
        self.location = location
        self.capacity = capacity
        self.volunteers = []  # List of Volunteers in this camp
        self.refugees = []    # List of Refugees in this camp

class Volunteer:
    def __init__(self, username, password, full_name, phone, availability, camp_id):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.phone = phone
        self.availability = availability
        self.camp_id = camp_id
        self.emergency_profiles = []  # List of EmergencyProfiles created by this volunteer

class EmergencyProfile:
    def __init__(self, profile_id, refugee_id, medical_condition, lead_family_member, number_of_relatives, timestamp):
        self.profile_id = profile_id
        self.refugee_id = refugee_id
        self.medical_condition = medical_condition
        self.lead_family_member = lead_family_member
        self.number_of_relatives = number_of_relatives
        self.timestamp = timestamp

        # test joe 22222
        # 1001 th test joe

        #1002 tets joe
        #1005 joe
        #1006 joe


        # 1003

        #1002 tets joe
        #1000

        #stella test 1



