import pandas as pd
# import GUItest as gi
def login(username, password):

    user_df = pd.read_csv('volunteers_file.csv')


    user = user_df[(user_df['username'] == username) & (user_df['user_password'] == password)]

    if not user.empty:
        full_name = user.iloc[0]["first_name"] + " " + user.iloc[0]["last_name"]

        print(f"Welcome, {full_name}! User type: Volunteer")
        return user.index[0]
    else:
        print("Invalid username or password.")
        return None
#

def add_volunteer(username, password, first_name, last_name,birthday, phone, address1, address2, city,acc_type,email,gender,active,availbility,):
    global user_df
    new_user_id = user_df['user_id'].max() + 1
    new_volunteer = pd.DataFrame({
        "user_id": [new_user_id],
        "username": [username],
        "user_password": [password],
        "first_name": [first_name],
        "last_name": [last_name],
        'dob':[birthday],
        "contact_number": [int(phone)],  # Convert phone number to integer
        "address1": [address1],
        "address2": [address2],
        "city": [city],
        "acc_type":[acc_type],
        "user_email": [email],
        'gender':[gender],
        'active':[active],
        'availbility':[availbility],
    })
    user_df = pd.concat([user_df, new_volunteer], ignore_index=True)
    print(f"Volunteer {first_name} {last_name} added successfully.")

def input_new_volunteer_info():
    username = input("Enter username: ")
    user_password = input("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    contact_number = int(input("Enter phone number: "))
    address1 = input("Enter address line 1: ")
    address2 = input("Enter address line 2: ")
    city = input("Enter city: ")
    acc_type = input("Enter account type: ")
    dob = input("Enter birthday: ")
    gender = input("Enter gender: ")
    active = input("Enter active: ")
    availbility = input("Enter availbility: ")
    user_email = input("Enter email: ")
    return {
        "username": username,
        "password": user_password,
        "first_name": first_name,
        "last_name": last_name,
        "phone": contact_number,
        "address1": address1,
        "address2": address2,
        "city": city,
        "birthday": dob,
        "active": active,
        "availbility": availbility,
        "gender": gender,
        "email": user_email,
        "acc_type":acc_type,
    }

def update_information(user_index, field_to_update, new_value,user_df):
    valid_fields = ["contact_number", "address1", "address2", "city", "user_email"]

    if field_to_update in valid_fields:
        if field_to_update == "phone":
            new_value = int(new_value)
        user_df.loc[user_index, field_to_update] = new_value
        print(f"{field_to_update} updated successfully.")
    else:
        print("Invalid field to update. Valid fields are:", valid_fields)

user_df = pd.read_csv('volunteers_file.csv')


def display_user_row(user_index, user_df):
    user_row = user_df.loc[[user_index]]
    print("\nUser Information:")
    print(user_row.to_string(index=False))

username=input('Type the Username: ')
password=int(input('Type the Password: '))
user_index=login(username,password)



while True:
    if user_index is not None:
            print("Options: Update/Create volunteer account/Display/Quit")
            operation = input("Enter the operation you want to perform: ").lower()
            if operation == "display":
                display_user_row(user_index, user_df)
            if operation == "create volunteer account":
                new_volunteer_info = input_new_volunteer_info()
                add_volunteer(**new_volunteer_info)
                user_df.to_csv('volunteers.csv', index=False)
            elif operation == "update":
                print("Fields to update: contact_number, address1, address2, city, user_email")
                field_to_update = input("Enter the field you want to update: ")
                new_value = input("Enter the new value: ")
                update_information(user_index, field_to_update, new_value, user_df)
                user_df.to_csv('volunteers.csv', index=False)
            elif operation=='quit':
                print('Thanks for your editing!')
                break
            else:
                print("Invalid operation.")
            # print(user_df.to_string())