import pandas as pd
from datetime import datetime as dt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

class HumanitarianPlan:
    def __init__(self, admin_id, plan_name, description, geographical_area, start_date, number_camps):
        self.admin_id = admin_id
        self.plan_name = plan_name
        self.description = description
        self.geographical_area = geographical_area
        self.start_date = start_date
        self.number_camps = number_camps

        # Attempt to read plan.csv or create an empty DataFrame if the file does not exist
        try:
            self.plan_df = pd.read_csv("plan.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.plan_df = pd.DataFrame(columns=['PlanID', 'planName', 'startDate', 'closingDate',
                                                 'geographicalArea', 'planDesc', 'adminID',
                                                 'active', 'NumberOfCamps', 'campID'])
        self.set_plan_id()

    def set_plan_id(self):
        if not self.plan_df.empty:
            self.plan_id = self.plan_df['PlanID'].max() + 1
        else:
            self.plan_id = 1

    def create_plan(self):
        self.set_plan_id()
        self.active = 1
        self.camp_id = self.generate_camp_ids()

        # Create initial entries for these camps
        new_camps = self.create_initial_camp_entries()

        # Convert 'camp_id' to string for new camps
        new_camps['camp_id'] = new_camps['camp_id'].astype(str)

        # Read existing camps data
        existing_camps_df = self.read_existing_camps()

        # Convert 'camp_id' to string in existing camps if it's not already
        existing_camps_df['camp_id'] = existing_camps_df['camp_id'].astype(str)

        # Convert start_date to a datetime object if it's a string
        if isinstance(self.start_date, str):
            try:
                self.start_date = pd.to_datetime(self.start_date, format='%Y-%m-%d', errors='raise')
            except ValueError:
                logging.error("Invalid start date format. Expected yyyy-mm-dd.")
                raise ValueError("Invalid start date format. Please use yyyy-mm-dd format.")

        # Append new camp data to existing data
        combined_camps_df = pd.concat([existing_camps_df, new_camps], ignore_index=True)

        # Convert 'camp_id' to integer for sorting
        combined_camps_df['camp_id'] = combined_camps_df['camp_id'].astype(int)

        # Sort by 'camp_id'
        combined_camps_df.sort_values(by='camp_id', inplace=True)

        # Convert 'camp_id' back to string if needed
        combined_camps_df['camp_id'] = combined_camps_df['camp_id'].astype(str)

        # Save to CSV
        combined_camps_df.to_csv('camps.csv', index=False)

        # Add new plan to plan.csv
        self.add_plan_to_csv()

        self.plan_df = pd.read_csv("plan.csv")

        # Log the creation
        logging.info(f"Plan created with ID: {self.plan_id} and Camp IDs: {self.camp_id}")

        return self.camp_id.split(',')

    def generate_camp_ids(self):
        existing_camp_ids = self.get_existing_camp_ids()
        camp_ids = []
        last_camp_no = self.get_last_camp_no()

        for _ in range(int(self.number_camps)):
            last_camp_no += 1
            while last_camp_no in existing_camp_ids:
                last_camp_no += 1
            camp_ids.append(str(last_camp_no))

        return ','.join(camp_ids)

    def get_existing_camp_ids(self):
        try:
            existing_camps_df = pd.read_csv('camps.csv')
            existing_ids = set(existing_camps_df['camp_id'].astype(str))
        except (FileNotFoundError, pd.errors.EmptyDataError):
            existing_ids = set()
        return existing_ids

    def get_last_camp_no(self):
        try:
            existing_camps_df = pd.read_csv('camps.csv')
            if not existing_camps_df.empty:
                # Extract the last camp number from the camp IDs
                last_camp_ids = existing_camps_df['camp_id'].astype(str).str.split(',')
                # Flatten the list of lists and convert to integers
                last_camp_ids = [int(cid) for sublist in last_camp_ids for cid in sublist if cid.isdigit()]
                return max(last_camp_ids) if last_camp_ids else 0
            else:
                return 0
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return 0

    def create_initial_camp_entries(self):
        # Assuming max_capacity is set to 50 and initial refugees_number is 0
        max_capacity = 50
        refugees_number = 0

        # Calculate current_availability
        current_availability = max_capacity - refugees_number
        specific_needs = "X volunteers required (update via manage camp)"
        return pd.DataFrame([{'camp_id': cid, 'location': self.geographical_area,
                              'volunteers_number': '', 'refugees_number': refugees_number,
                              'plan_name': self.plan_name, 'current_availability': current_availability,
                              'max_capacity': max_capacity, 'specific_needs': specific_needs, 'allocated_resources': ''}
                             for cid in self.camp_id.split(',')])

    def read_existing_camps(self):
        try:
            return pd.read_csv('camps.csv')
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=['camp_id', 'location', 'volunteers_number',
                                         'refugees_number', 'plan_name', 'current_availability',
                                         'max_capacity', 'specific_needs', 'allocated_resources'])

    def add_plan_to_csv(self):
        # Convert start_date to a datetime object if it's a string
        if isinstance(self.start_date, str):
            try:
                self.start_date = pd.to_datetime(self.start_date, format='%Y-%m-%d', errors='coerce')
                if pd.isna(self.start_date):
                    # If conversion fails, log an error and use the original string
                    logging.error(f"Invalid start date format: {self.start_date}")
                    formatted_start_date = self.start_date  # Use the original string if conversion fails
                else:
                    formatted_start_date = self.start_date.strftime('%Y-%m-%d')
            except Exception as e:
                logging.error(f"Error converting start date: {e}")
                formatted_start_date = self.start_date  # Use the original string in case of exception
        else:
            # If start_date is not a string, use the original value
            logging.error(f"start_date is not a string: {self.start_date}")
            formatted_start_date = str(self.start_date)

        new_data = [[self.plan_id, self.plan_name, formatted_start_date, self.geographical_area,
                     self.description, self.admin_id, self.active, self.number_camps, self.camp_id]]
        added_df = pd.DataFrame(new_data, columns=['planID', 'planName', 'startDate',
                                                   'geographicalArea', 'planDesc', 'adminID',
                                                   'active', 'NumberOfCamps', 'campID'])
        added_df['closingDate'] = ''
        column_order = ['planID', 'planName', 'startDate', 'closingDate',
                        'geographicalArea', 'planDesc', 'adminID',
                        'active', 'NumberOfCamps', 'campID']
        added_df = added_df.reindex(columns=column_order)
        added_df.to_csv("plan.csv", mode='a', header=False, index=False)

    def terminate_plan(self, plan_id, closing_date=None):
        # Load existing plans
        try:
            plans_df = pd.read_csv('plan.csv')
        except FileNotFoundError:
            raise FileNotFoundError("The plan.csv file does not exist.")

        # Check if plan_id exists
        if plan_id not in plans_df['PlanID'].values:
            raise ValueError(f"No plan found with ID {plan_id}")

        # Set closing_date if not provided
        if closing_date is None:
            closing_date = pd.Timestamp.now().strftime('%m/%d/%Y')

        # Update the plan's status
        plans_df.loc[plans_df['PlanID'] == plan_id, 'active'] = 0
        plans_df.loc[plans_df['PlanID'] == plan_id, 'closingDate'] = closing_date

        # Save the updated DataFrame
        plans_df.to_csv('plan.csv', index=False)

        # Log the termination
        logging.info(f"Plan with ID {plan_id} terminated on {closing_date}")

# Example Usage
# new_plan = HumanitarianPlan(admin_id, plan_name, description, geographical_area, start_date, number_camps)
# new_plan.create_plan()





