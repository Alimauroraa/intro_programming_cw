import pandas as pd


# Path to the CSV file
csv_filename = '../camps_information.csv'
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
camps_df = pd.read_csv(csv_filename)

# Display the DataFrame
print(camps_df)


def append_to_csv(file_name):
    # Prompt user for new camp information
    camp_id = input("Enter the new camp's ID: ")
    volunteer_id = input("Enter the new Volunteer's ID: ")
    location = input("Enter the new camp's location: ")
    capacity = input("Enter the new camp's capacity: ")
    specific_needs = input("Enter the new camp's specific needs: ")
    resources = input("Enter the new camp's resources: ")

    # Create a new DataFrame with the user's input
    new_data = pd.DataFrame({
        'Camp ID': [camp_id],
        'Volunteer ID': [volunteer_id],
        'Location': [location],
        'Capacity': [capacity],
        'Specific Needs': [specific_needs],
        'Resources': [resources]
    })

    # Read the existing data and append the new data
    try:
        existing_data = pd.read_csv(file_name)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    except pd.errors.EmptyDataError:
        updated_data = new_data

    # Write the updated DataFrame back to the CSV
    updated_data.to_csv(file_name, index=False)
    print(f"New camp information appended to {file_name}.")


# Run this in your local Python environment to append new data to the CSV file
append_to_csv(csv_filename)
# Read the CSV file into a DataFrame
camps_df = pd.read_csv(csv_filename)

# Display the DataFrame
print(camps_df)


def delete_camp(file_name):
    # Prompt user for the Camp ID of the camp to be deleted
    camp_id = input("Enter the Camp ID of the camp to delete: ")

    # Load the CSV file into a DataFrame
    try:
        camps_df = pd.read_csv(file_name)

        # Check if the Camp ID exists in the DataFrame
        if camp_id in camps_df['Camp ID'].values:
            # Delete the row with the specified Camp ID
            camps_df = camps_df[camps_df['Camp ID'] != camp_id]

            # Save the modified DataFrame back to the CSV file
            camps_df.to_csv(file_name, index=False)
            print(f"Camp with ID {camp_id} has been deleted.")
        else:
            print(f"No camp found with ID {camp_id}.")

    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")

    except FileNotFoundError:
        print(f"No file found with the name {file_name}.")


delete_camp(csv_filename)
# Read the CSV file into a DataFrame
camps_df = pd.read_csv(csv_filename)

# Display the DataFrame
print(camps_df)