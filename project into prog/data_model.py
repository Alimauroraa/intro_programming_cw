class Users:
    def __init__(self, user_id, username, user_password, first_name, last_name,
                 dob, user_email, contact_number, address1, address2, city, acc_type,
                 availability, gender, active):
        self.user_id=user_id
        self.username=username
        self.user_password=user_password
        self.first_name=first_name
        self.last_name=last_name
        self.dob=dob
        self.user_email=user_email
        self.contact_number=contact_number
        self.address1=address1
        self.address2=address2
        self.city=city
        self.acc_type=acc_type
        self.availability=availability
        self.gender=gender
        self.active=active

class Admin(Users):
    def __init__(self, user_id, username, user_password, first_name, last_name,
                 dob, user_email, contact_number, address1, address2, city, acc_type,
                 availability, gender, active):
        super().__init__(user_id, username, user_password, first_name, last_name,
                 dob, user_email, contact_number, address1, address2, city, acc_type,
                 availability, gender, active)

        self.created_plans = []  # List of HumanitarianPlans created by this admin

class HumanitarianPlan:
    def __init__(self, plan_id, admin_id, plan_name,description, geographical_area, active, start_date, closing_date=None):
        self.plan_id = plan_id
        self.admin_id=admin_id
        self.plan_name=plan_name
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.closing_date = closing_date
        self.active=active
        self.camps = []  # List of Camps associated with this plan

class Donation:
    def __init__(self,donation_id, volunteer_id, amount, plan_id):
        self.donation_id=donation_id
        self.volunteer_id=volunteer_id
        self.amount=amount
        self.plan_id=plan_id

class Refugee:
    def __init__(self, refugee_id, camp_id, refugee_first_name, refugee_last_name, refugee_gender):
        self.refugee_id=refugee_id
        self.camp_id=camp_id
        self.refugee_first_name=refugee_first_name
        self.refugee_last_name=refugee_last_name
        self.refugee_gender=refugee_gender

class Camp:
    def __init__(self, camp_id, volunteer_id, location, capacity, specific_needs,allocatedresources):
        self.camp_id = camp_id
        self.volunteer_id=volunteer_id
        self.location = location
        self.capacity = capacity
        self.specific_needs=specific_needs
        self.allocatedresources=0
        self.volunteers = []  # List of Volunteers in this camp
        self.refugees = []    # List of Refugees in this camp

class Volunteer(Users):
    def __init__(self, user_id, username, user_password, first_name, last_name,
                 dob, user_email, contact_number, address1, address2, city, acc_type,
                 availability, gender, active, camp_id,):
        super().__init__(user_id, username, user_password, first_name, last_name,
                 dob, user_email, contact_number, address1, address2, city, acc_type,
                 availability, gender, active,)
        self.camp_id = camp_id
        self.emergency_profiles = []  # List of EmergencyProfiles created by this volunteer

class EmergencyProfile:
    def __init__(self, volunteer_id, profile_id, refugee_id, medical_condition,
                 lead_family_member, lead_phone_number, number_of_relatives, timestamp):
        self.volunteer_id=volunteer_id
        self.profile_id = profile_id
        self.refugee_id = refugee_id
        self.medical_condition = medical_condition
        self.lead_family_member = lead_family_member
        self.lead_phone_number=lead_phone_number
        self.number_of_relatives = number_of_relatives
        self.timestamp = timestamp

class Inventory:
    def __init__(self, inventory_id, admin_id, inventory_name, quantity):
        self.inventory_id=inventory_id
        self.admin_id=admin_id
        self.inventory_name=inventory_name
        self.quantity=quantity
