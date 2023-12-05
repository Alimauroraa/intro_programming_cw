import pandas as pd
from datetime import date as d, datetime as dt
import logging

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

#class for the plan
class HumanitarianPlan:
    def __init__(self, admin_id, plan_name,description, geographical_area, start_date,number_camps):
        self.admin_id=admin_id
        self.plan_name=plan_name
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        #self.closing_date = closing_date
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
        print(self.plan_df['camp_id'].iloc[-1])
        if ',' not in str(self.plan_df['camp_id'].iloc[-1]):
            self.last_camp_no = int(self.plan_df['camp_id'].iloc[-1])

        else:
            #access last element in last row (since if there are multiple elements we add with ,)
            self.last_camp_no=int(self.plan_df['camp_id'].iloc[-1].split(',')[-1])
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
        new_data=[[self.plan_id,self.plan_name,self.start_date.strftime('%m/%d/%Y'),self.geographical_area,
                   self.description, self.admin_id, self.active, self.number_camps,self.camp_id]]


        added_df = pd.DataFrame(new_data,columns=['planID', 'planName', 'startDate',
                                                    'geographicalArea','planDesc', 'adminID',
                                                    'active', 'NumberOfCamps', 'campID'])
        added_df['closingDate'] = ''
        column_order=['planID', 'planName', 'startDate', 'closingDate',
                        'geographicalArea','planDesc', 'adminID',
                        'active', 'NumberOfCamps', 'campID']
        added_df=added_df.reindex(columns=column_order)
        added_df.to_csv("plan.csv", mode='a',header=False, index=False)

        
        # Log the creation
        logging.info(f"Plan created with ID: {self.plan_id} and Camp IDs: {self.camp_id}")

        # Return the camp_ids for further processing
        return self.camp_id.split(',')

    def generate_camps_from_plan(self, camp_ids):
        try:
            # Read existing plans to get geographical areas
            plans_df = pd.read_csv('plan.csv')

            # Read existing camps
            try:
                existing_camps_df = pd.read_csv('camps.csv')
            except (FileNotFoundError, pd.errors.EmptyDataError):
                existing_camps_df = pd.DataFrame(
                    columns=['camp_id', 'location', 'volunteers_number', 'refugees_number', 'plan_name',
                             'current_availability', 'max_capacity' 'specific_needs', 'allocated_resources'])

            # Create DataFrame for new camps with inherited locations
            new_camps_data = []
            for camp_id in camp_ids:
                # Find the plan associated with this camp
                plan = plans_df[plans_df['camp_id'].astype(str).str.contains(camp_id)]
                geographical_area = plan['geographicalArea'].iloc[0] if not plan.empty else ''

                new_camps_data.append({
                    'camp_id': camp_id,
                    'location': geographical_area,
                    'volunteers_number': "",
                    'refugees_number': "",
                    'plan_name': "",
                    'current_availability': "",
                    'max_capacity': "",
                    'specific_needs': "",
                    'allocated_resources': ""
                })

            new_camps_df = pd.DataFrame(new_camps_data)

            # Append new camp data to existing data
            combined_camps_df = pd.concat([existing_camps_df, new_camps_df], ignore_index=True)
            combined_camps_df.to_csv('camps.csv', index=False)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Handle the case where plan.csv is missing or empty
            pass

    def generate_missing_camps_from_plans(self):
        try:
            plans_df = pd.read_csv('plan.csv')
            if not plans_df.empty and 'camp_id' in plans_df.columns:
                camp_ids = set()  # A set to store unique camp IDs
                for ids in plans_df['camp_id']:
                    camp_ids.update(str(ids).split(','))

                try:
                    existing_camps_df = pd.read_csv('camps.csv')
                except (FileNotFoundError, pd.errors.EmptyDataError):
                    existing_camps_df = pd.DataFrame(
                        columns=['camp_id', 'location', 'volunteers_number', 'refugees_number', 'plan_name',
                                 'current_availability', 'max_capacity' 'specific_needs', 'allocated_resources'])

                # Identify missing camp IDs
                missing_camps = [cid for cid in camp_ids if cid not in existing_camps_df['camp_id'].astype(str).tolist()]

                # Create DataFrame for missing camps
                if missing_camps:
                    missing_camps_df = pd.DataFrame(missing_camps, columns=['camp_id'])
                    missing_camps_df['location'] = ''
                    missing_camps_df['volunteers_number'] = ''
                    missing_camps_df['refugees_number'] = ''
                    missing_camps_df['plan_name'] = ''
                    missing_camps_df['current_availability'] = ''
                    missing_camps_df['max_capacity'] = ''
                    missing_camps_df['specific_needs'] = ''
                    missing_camps_df['allocated_resources'] = ''

                    # Append missing camps to existing camps and save
                    combined_camps_df = pd.concat([existing_camps_df, missing_camps_df], ignore_index=True)
                    combined_camps_df.to_csv('camps.csv', index=False)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Handle the case where plan.csv is missing or empty
            pass

    # def close_plan(self):
    #     now = d.now()
    #     current_date = now.strftime("$y-%m-%d")
    #     print(current_date)









