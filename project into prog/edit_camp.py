import pandas as pd


class Camp:
    def __init__(self, file_path):
        self.file_path = file_path
        self.camp_df = pd.read_csv(file_path)

    def update_camp(self, camp_id, updated_info):
        try:
            camp_id = int(camp_id)
        except ValueError:
            return False  # Return False if camp_id is not a valid integer

        if camp_id in self.camp_df['Camp ID'].values:
            for key, value in updated_info.items():
                self.camp_df.loc[self.camp_df['Camp ID'] == camp_id, key] = value
            self.camp_df.to_csv(self.file_path, index=False)
            return True
        return False

    def get_resources(self, camp_id):
        try:
            camp_id = int(camp_id)
        except ValueError:
            return "Invalid Camp ID"

        if camp_id in self.camp_df['Camp ID'].values:
            resources = self.camp_df.loc[self.camp_df['Camp ID'] == camp_id, 'Resources'].values[0]
            return resources if resources else "No resources listed"
        return "Camp ID not found"

    def get_camp_info(self, camp_id):
        try:
            camp_id = int(camp_id)
        except ValueError:
            return None  # Return None if camp_id is not a valid integer

        if camp_id in self.camp_df['Camp ID'].values:
            camp_info = self.camp_df.loc[self.camp_df['Camp ID'] == camp_id]
            return camp_info.iloc[0].to_dict()  # Convert the row to a dictionary
        return None