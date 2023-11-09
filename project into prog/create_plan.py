import pandas as pd
from datetime import date as d
import logging

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')


#importing the csv file for plan
plan_df=pd.read_csv("plan.csv")

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

    def close_plan(self):
        now = d.now()
        current_date = now.strftime("$y-%m-%d")
        print(current_date)




#------------------INPUT------------------#
input_admin_id = input("Enter admin id:")
input_plan_name = input("Enter plan name:")
logging.info(f"Plan name: {input_plan_name}")
input_description = input("Enter description:")
input_geographical_area = input("Enter geographical area:")
logging.info(f"Plan location: {input_geographical_area}")
input_start_date = input("Enter start date (YYYY-MM-DD):")
input_closing_date = input("Enter closing date (YYYY-MM-DD):")
try:
    start_date = d.fromisoformat(input_start_date)
    closing_date = d.fromisoformat(input_closing_date)
except ValueError as e:
    print ("Not in correct format")
input_active = 1
input_number_camps=input("Enter number of camps:")

add_plan=HumanitarianPlan(input_admin_id,input_plan_name,input_description,input_geographical_area,
                          input_active,start_date,closing_date,input_number_camps)
add_plan.create_plan()


