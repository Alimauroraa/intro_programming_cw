import pandas as pd

def generate_camps_from_plan():
    plan_df = pd.read_csv("plan.csv")

    camp_ids = set()  # Using a set to ensure uniqueness
    for ids in plan_df['campID']:
        camp_ids.update(map(int, ids.split(',')))

    # Sort the camp IDs to maintain order
    sorted_camp_ids = sorted(camp_ids)

    # Create a DataFrame for camps.csv with the desired columns
    camps_df = pd.DataFrame(sorted_camp_ids, columns=['Camp ID'])
    camps_df['Volunteer ID'] = ''
    camps_df['Location'] = ''
    camps_df['Capacity'] = ''
    camps_df['Specific Needs'] = ''
    camps_df['Resources'] = ''

    # Write the DataFrame to camps.csv
    camps_df.to_csv("camps.csv", index=False)

    print("camps.csv created successfully with the following data:")
    print(camps_df)
if __name__ == "__main__":
    generate_camps_from_plan()