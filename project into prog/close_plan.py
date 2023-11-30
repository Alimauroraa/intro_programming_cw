import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,filename='close_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')


#importing the csv file for plan
plan_df=pd.read_csv("plan.csv")

#class for closing plan
class ClosePlan:
    def __init__(self, plan_df):
        # drop csv file to python
        self.plan_df = plan_df

        #define plan id
        self.plan_id=self.plan_df['PlanID']

        # convert the closingDate column to datetime format
        self.plan_df['closingDate']=pd.to_datetime(self.plan_df['closingDate'], format="mixed") #%m/%d/%Y

        # state current date
        self.now=datetime.now()

    def close_plan(self):
        for i in self.plan_df['closingDate']:
            if i=='':
                pass
            elif (i<self.now):
                #updating the values in active column, set it to 0 if closingDate has passed
                self.plan_df.loc[self.plan_df['closingDate'] < self.now, 'active'] = 0

        inactive_plan = self.plan_df[self.plan_df['active'] == 0]['PlanID']  # find associated planID with active=0
        inactive_plan_id = inactive_plan.unique()
        for i in inactive_plan_id:
            print(i)
            logging.info(f"Plan {i} has been closed and is inactive")
        self.plan_df.to_csv("plan.csv", index=False)

#calling class and method
plan=ClosePlan(plan_df)
plan.close_plan()


