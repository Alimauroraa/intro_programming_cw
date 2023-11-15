import pandas as pd
from datetime import date as d, datetime as dt
import logging

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

#class for the plan
class HumanitarianPlan:
    def __init__(self, admin_id, plan_name,description, geographical_area, active, start_date,
                 closing_date,number_camps):
        self.admin_id=admin_id
        self.plan_name=plan_name
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.closing_date = closing_date
        self.active=active
        self.number_camps=number_camps
        self.plan_df = pd.read_csv("plan.csv")                          #drop csv file to python
        self.plan_id = self.plan_df['PlanID'].iloc[-1] + 1
        logging.info(f"New plan is created. Plan id: {self.plan_id}")
        self.camp_id=''                                                 #empty string for camp_id at first

    def create_plan(self):
        self.camp_id=''
        print(self.plan_df['campID'].iloc[-1])
        if ',' not in str(self.plan_df['campID'].iloc[-1]):
            self.last_camp_no = int(self.plan_df['campID'].iloc[-1])

        else:
            #access last element in last row (since if there are multiple elements we add with ,)
            self.last_camp_no=int(self.plan_df['campID'].iloc[-1].split(',')[-1])
            print(self.last_camp_no)
            #self.plan_df['campID']=self.plan_df['campID'].iloc[-1].str.split(',') #the above will give [1,2]
            #self.last_camp_no = int(self.plan_df['campID'][-1]) #this will give 2

        if int(self.number_camps)==1:
            self.camp_id=''
            self.camp_id+=str(self.last_camp_no+1)
            print(self.camp_id,'i')
            self.camp_id=self.camp_id
            logging.info(f"Associated camp no: {self.camp_id}")

        else:
            i=0
            j=1
            while i<(int(self.number_camps)):
            #for i in range(1,int(self.number_camps)+1):
                self.camp_id+=str(self.last_camp_no+j)
                self.camp_id += ','
                i+=1
                j+=1
            self.camp_id=self.camp_id[:-1]
            logging.info(f"Associated camp no: {self.camp_id}")

        print(f"camp id: {self.camp_id}")
        new_data=[[self.plan_id,self.plan_name,self.start_date,self.closing_date,self.geographical_area,
                   self.description, self.admin_id, self.active, self.number_camps,self.camp_id]]

        added_df = pd.DataFrame(new_data,columns=['planID', 'planName', 'startDate', 'closingDate',
                                                    'geographicalArea','planDesc', 'adminID',
                                                    'active', 'NumberOfCamps', 'campID'])
        added_df.to_csv("plan.csv", mode='a',header=False, index=False)

    # def close_plan(self):
    #     now = d.now()
    #     current_date = now.strftime("$y-%m-%d")
    #     print(current_date)



#importing the csv file for plan
plan_df=pd.read_csv("plan.csv")
admin_df=pd.read_csv("admin_credentials.csv")
print(plan_df.to_string()) #display the whole table for plan_df by putting to_string()
print(admin_df.to_string())
print(admin_df['user_id'].tolist())

#-----------------------------------------------INPUT------------------------------------------------------------#

while True:     #condition is true by default and we need to
    input_admin_id = input("Enter admin id:")
    if input_admin_id.isdigit() and input_admin_id in map(str,admin_df['user_id'].tolist()):    #this will check whether the value exists in rows within user_id column
        #map(str,..) converts the row into string so it can be compared with the input
        logging.info(f"Admin id: {input_admin_id}")
        break
    elif not input_admin_id.isdigit():
        print("Invalid input. Please enter a numeric value.")
    else:
        print("Admin id not found. Please try again.")

while True:
    input_plan_name = input("Enter plan name:")
    if all(char.isalpha() or char.isspace() for char in input_plan_name) and 1< len(input_plan_name) < 200:
        logging.info(f"Plan name: {input_plan_name}")
        break
    elif not all(char.isalpha() or char.isspace() for char in input_plan_name):
        print("Please enter only alphabetical character.")

    elif len(input_plan_name) > 200:
        print("200 characters only.")
    elif len(input_plan_name) == 1:
        print("Invalid input. Please try again")

while True:
    input_description = input("Enter description:")
    if 1<len(input_description)<500:
        break
    elif len(input_description)>500:
        print("500 characters only")
    if len(input_description)==1:
        print("Invalid input. Please try again")

while True:
    input_geographical_area = input("Enter geographical area:")
    if all(char.isalpha() or char.isspace() for char in input_geographical_area) and 1<len(input_geographical_area)<200:
        logging.info(f"Plan location: {input_geographical_area}")
        break
    elif not all(char.isalpha() or char.isspace() for char in input_geographical_area):
        print("Please enter only alphabetical character.")
    elif len(input_geographical_area)>200:
        print("200 characters only")

while True:
    input_start_date = input("Enter start date (YYYY-MM-DD):")
    try:
        start_date = d.fromisoformat(input_start_date)
        if start_date >= dt.now().date():
            break
        else:
            print("Invalid start date. Please enter again.")
    except ValueError as e:
        print("Invalid date format. Please enter in format YYYY-MM-DD")

while True:
    input_closing_date = input("Enter closing date (YYYY-MM-DD):")
    try:
        closing_date = d.fromisoformat(input_closing_date)
        if closing_date > dt.now().date() and closing_date > start_date:
            break
        else:
            print("Invalid closing date. Please enter again.")

    except ValueError as e:
        print("Invalid date format. Please enter in format YYYY-MM-DD")

input_active = 1    #by default the plan is active upon creation

while True:
    input_number_camps=input("Enter number of camps:")
    if input_number_camps.isdigit():
        break
    else:
        print("Invalid input. Please enter a numeric value.")


#calling class and method
add_plan=HumanitarianPlan(input_admin_id,input_plan_name,input_description,input_geographical_area,
                          input_active,start_date,closing_date,input_number_camps)
add_plan.create_plan()


