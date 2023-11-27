import pandas as pd
from datetime import date as d, datetime as dt
import logging

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

#class for the plan
class HumanitarianPlan:
    def __init__(self, admin_id, plan_name,description, geographical_area,  start_date,
                 closing_date,number_camps):
        self.admin_id=admin_id
        self.plan_name=plan_name
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.closing_date = closing_date
        self.number_camps=number_camps
        self.plan_df = pd.read_csv("plan.csv")                          #drop csv file to python
        self.plan_id = self.plan_df['PlanID'].iloc[-1] + 1
        logging.info(f"New plan is created. Plan id: {self.plan_id}")
        self.camp_id=''                                                 #empty string for camp_id at first

    def create_plan(self):
        # Check if plan.csv is not empty and set plan_id accordingly
        if not self.plan_df.empty:
            self.plan_id = self.plan_df['PlanID'].max() + 1
        else:
            self.plan_id = 1  # Start from 1 if the file is empty
        self.active = 1
        self.camp_id=''
        print(self.plan_df['campID'].iloc[-1])
        if ',' not in str(self.plan_df['campID'].iloc[-1]):
            self.last_camp_no = int(self.plan_df['campID'].iloc[-1])

        else:
            #access last element in last row (since if there are multiple elements we add with ,)
            self.last_camp_no=int(self.plan_df['campID'].iloc[-1].split(',')[-1])
            print(self.last_camp_no)

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

        # Log the creation
        logging.info(f"Plan created with ID: {self.plan_id} and Camp IDs: {self.camp_id}")

        # Return the camp_ids for further processing
        return self.camp_id.split(',')

    def generate_camps_from_plan(self, camp_ids):
        # Create a DataFrame for the new camps
        new_camps_df = pd.DataFrame(camp_ids, columns=['CampID'])
        new_camps_df['Location'] = ''
        new_camps_df['Capacity'] = ''
        new_camps_df['SpecificNeeds'] = ''
        new_camps_df['Volunteers'] = ''
        new_camps_df['Refugees'] = ''
        new_camps_df['ResourcesAllocated'] = ''

        try:
            # Try to read existing camps from 'camps.csv'
            existing_camps_df = pd.read_csv('camps.csv')
            # Check if the DataFrame is empty
            if existing_camps_df.empty:
                combined_camps_df = new_camps_df
            else:
                # Append new camp data to existing data
                combined_camps_df = pd.concat([existing_camps_df, new_camps_df], ignore_index=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file doesn't exist or is empty, use new camps data as the entire dataset
            combined_camps_df = new_camps_df

        # Write the combined DataFrame to 'camps.csv'
        combined_camps_df.to_csv('camps.csv', index=False)

    # def close_plan(self):
    #     now = d.now()
    #     current_date = now.strftime("$y-%m-%d")
    #     print(current_date)








