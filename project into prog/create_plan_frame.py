import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from datetime import date as d, datetime as dt
import logging
from create_plan import HumanitarianPlan
import admin_login_gui

# from admin_home_frame import admin_home

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

admin_df = pd.read_csv("admin_credentials.csv")
plan_df= pd.read_csv('plan.csv')

def back(create_plan_frame):
    create_plan_frame.grid_forget()

def clear():
    admin_entry.set('')
    name_entry.delete(1.0,tk.END)
    desc_entry.delete(1.0,tk.END)
    geo_entry.set('')
    start_entry.delete(0,tk.END)
    camps_entry.set('')

def validate_input(plan_name, description, geographical_area, start_date, number_camps):
    # Validate plan name
    if len(plan_name) < 1:
        messagebox.showerror("Error", "Required. Please enter the plan name")
        return False
    elif not all(char.isalnum() or char.isspace() for char in plan_name):
        messagebox.showerror("Error", "Please enter a valid plan name, alphanumeric characters only")
        return False
    elif len(plan_name) > 200:
        messagebox.showerror("Error", "Maximum 200 characters are allowed for plan name")
        return False

    # Validate description
    if len(description) < 1:
        messagebox.showerror("Error", "Required. Please enter the description")
        return False
    elif not all(char in [',', '.'] or char.isalpha() or char.isspace() or char.isdigit() for char in description):
        messagebox.showerror("Error", "Please enter a valid description")
        return False
    elif len(description) > 500:
        messagebox.showerror("Error", "Maximum 500 characters are allowed for description")
        return False

    # Validate geographical area
    if len(geographical_area) == 0:
        messagebox.showerror("Error", "Required. Please select the country")
        return False

    # Validate start date
    start = None  # Initialize start to None
    if len(start_date) == 0:
        messagebox.showerror("Error", "Required. Please enter a start date")
        return False, None
    else:
        try:
            start = dt.fromisoformat(start_date).date()
            if start < dt.now().date():  # Changed to allow today's date
                messagebox.showerror("Error", "Start date should be today or later")
                return False, None
        except ValueError:
            messagebox.showerror("Error", "Required. Please enter a start date in YYYY-MM-DD format")
            return False, None

    # Validate number of camps
    if len(number_camps) == 0:
        messagebox.showerror("Error", "Required. Please enter the number of camps")
        return False
    else:
        try:
            num_camps = int(number_camps)
            if num_camps <= 0:
                messagebox.showerror("Error", "Number of camps must be a positive integer")
                return False
        except ValueError:
            messagebox.showerror("Error", "Incorrect number of camps. Please enter a valid integer")
            return False

    logging.info(f"Plan name: {plan_name}, is created")
    return True, start


def submit_plan():
    # Retrieve the entry
    admin_id = admin_entry.get()
    plan_name = name_entry.get(1.0, tk.END).strip()  # Added strip() to remove trailing newlines
    description = desc_entry.get(1.0, tk.END).strip()  # Added strip() to remove trailing newlines
    geographical_area = geo_entry.get()
    start_date = start_entry.get()
    number_camps = camps_entry.get()

    # Validate input and capture the start date
    validation_result, start = validate_input(plan_name, description, geographical_area, start_date, number_camps)

    if validation_result:
        # Use the captured start date
        new_plan = HumanitarianPlan(admin_id, plan_name, description, geographical_area, start, number_camps)
        camp_ids = new_plan.create_plan()  # This method now handles plan and camp creation

        # Inform the user that the plan and camps have been created
        messagebox.showinfo("Success", "Plan and associated camps created successfully.")


def plan_creator_frame(parent):
    # initializing
    create_plan_frame=tk.Frame(parent, bg='#021631')

    #heading
    tk.Label(create_plan_frame, text="Create new humanitarian plan", font="calibri 16",bg="#021631", fg="#fff").place(x=50,y=50)

    #label
    tk.Label(create_plan_frame, text="Admin id", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=150)
    tk.Label(create_plan_frame, text="Plan name", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=200)
    tk.Label(create_plan_frame, text="Description", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=250)
    tk.Label(create_plan_frame, text="Country", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=350)
    tk.Label(create_plan_frame, text="Start date (YYYY-MM-DD)", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=400)
    #tk.Label(create_plan_frame, text="Closing date (YYYY-MM-DD)", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=400)
    tk.Label(create_plan_frame, text="Number of camps", font="calibri 12", bg="#021631",fg="#fff").place(x=60,y=450)

    #Entry
    global name
    global geo
    global start
    global end
    # name=tk.StringVar()
    # geo=tk.StringVar()
    # start=tk.StringVar()
    # end=tk.StringVar()

    #defining the entries as global variable
    global admin_entry
    global name_entry
    global desc_entry
    global geo_entry
    global start_entry
    #global end_entry
    global camps_entry

    # admin_entry=ttk.Combobox(create_plan_frame, values= [i for i in map(str,admin_df['user_id'].tolist())], width=48)
    # name_entry=tk.Text(create_plan_frame, width=43, bd=2, font="calibri 10")
    # desc_entry=tk.Text(create_plan_frame, font="calibri 10",width=43,height=4, bd=4)
    # geo_entry=tk.Text(create_plan_frame, width=43, bd=2, font="calibri 10")
    # start_entry=tk.Text(create_plan_frame, width=43, bd=2, font="calibri 10")
    # end_entry=tk.Text(create_plan_frame, width=43, bd=2, font="calibri 10")
    # camps_entry= ttk.Combobox(create_plan_frame, values=[i for i in range(1,21)], width=48)

    global country
    country = ['United States',
               'Afghanistan',
               'Albania',
               'Algeria',
               'American Samoa',
               'Andorra',
               'Angola',
               'Anguilla',
               'Antarctica',
               'Antigua And Barbuda',
               'Argentina',
               'Armenia',
               'Aruba',
               'Australia',
               'Austria',
               'Azerbaijan',
               'Bahamas',
               'Bahrain',
               'Bangladesh',
               'Barbados',
               'Belarus',
               'Belgium',
               'Belize',
               'Benin',
               'Bermuda',
               'Bhutan',
               'Bolivia',
               'Bosnia And Herzegowina',
               'Botswana',
               'Bouvet Island',
               'Brazil',
               'Brunei Darussalam',
               'Bulgaria',
               'Burkina Faso',
               'Burundi',
               'Cambodia',
               'Cameroon',
               'Canada',
               'Cape Verde',
               'Cayman Islands',
               'Central African Rep',
               'Chad',
               'Chile',
               'China',
               'Christmas Island',
               'Cocos Islands',
               'Colombia',
               'Comoros',
               'Congo',
               'Cook Islands',
               'Costa Rica',
               'Cote D`ivoire',
               'Croatia',
               'Cuba',
               'Cyprus',
               'Czech Republic',
               'Denmark',
               'Djibouti',
               'Dominica',
               'Dominican Republic',
               'East Timor',
               'Ecuador',
               'Egypt',
               'El Salvador',
               'Equatorial Guinea',
               'Eritrea',
               'Estonia',
               'Ethiopia',
               'Falkland Islands (Malvinas)',
               'Faroe Islands',
               'Fiji',
               'Finland',
               'France',
               'French Guiana',
               'French Polynesia',
               'French S. Territories',
               'Gabon',
               'Gambia',
               'Georgia',
               'Germany',
               'Ghana',
               'Gibraltar',
               'Greece',
               'Greenland',
               'Grenada',
               'Guadeloupe',
               'Guam',
               'Guatemala',
               'Guinea',
               'Guinea-bissau',
               'Guyana',
               'Haiti',
               'Honduras',
               'Hong Kong',
               'Hungary',
               'Iceland',
               'India',
               'Indonesia',
               'Iran',
               'Iraq',
               'Ireland',
               'Israel',
               'Italy',
               'Jamaica',
               'Japan',
               'Jordan',
               'Kazakhstan',
               'Kenya',
               'Kiribati',
               'Korea (North)',
               'Korea (South)',
               'Kuwait',
               'Kyrgyzstan',
               'Laos',
               'Latvia',
               'Lebanon',
               'Lesotho',
               'Liberia',
               'Libya',
               'Liechtenstein',
               'Lithuania',
               'Luxembourg',
               'Macau',
               'Macedonia',
               'Madagascar',
               'Malawi',
               'Malaysia',
               'Maldives',
               'Mali',
               'Malta',
               'Marshall Islands',
               'Martinique',
               'Mauritania',
               'Mauritius',
               'Mayotte',
               'Mexico',
               'Micronesia',
               'Moldova',
               'Monaco',
               'Mongolia',
               'Montserrat',
               'Morocco',
               'Mozambique',
               'Myanmar',
               'Namibia',
               'Nauru',
               'Nepal',
               'Netherlands',
               'Netherlands Antilles',
               'New Caledonia',
               'New Zealand',
               'Nicaragua',
               'Niger',
               'Nigeria',
               'Niue',
               'Norfolk Island',
               'Northern Mariana Islands',
               'Norway',
               'Oman',
               'Pakistan',
               'Palau',
               'Panama',
               'Papua New Guinea',
               'Paraguay',
               'Peru',
               'Philippines',
               'Pitcairn',
               'Poland',
               'Portugal',
               'Puerto Rico',
               'Qatar',
               'Reunion',
               'Romania',
               'Russian Federation',
               'Rwanda',
               'Saint Kitts And Nevis',
               'Saint Lucia',
               'St Vincent/Grenadines',
               'Samoa',
               'San Marino',
               'Sao Tome',
               'Saudi Arabia',
               'Senegal',
               'Seychelles',
               'Sierra Leone',
               'Singapore',
               'Slovakia',
               'Slovenia',
               'Solomon Islands',
               'Somalia',
               'South Africa',
               'Spain',
               'Sri Lanka',
               'St. Helena',
               'St.Pierre',
               'Sudan',
               'Suriname',
               'Swaziland',
               'Sweden',
               'Switzerland',
               'Syrian Arab Republic',
               'Taiwan',
               'Tajikistan',
               'Tanzania',
               'Thailand',
               'Togo',
               'Tokelau',
               'Tonga',
               'Trinidad And Tobago',
               'Tunisia',
               'Turkey',
               'Turkmenistan',
               'Tuvalu',
               'Uganda',
               'Ukraine',
               'United Arab Emirates',
               'United Kingdom',
               'Uruguay',
               'Uzbekistan',
               'Vanuatu',
               'Vatican City State',
               'Venezuela',
               'Viet Nam',
               'Virgin Islands (British)',
               'Virgin Islands (U.S.)',
               'Western Sahara',
               'Yemen',
               'Yugoslavia',
               'Zaire',
               'Zambia',
               'Zimbabwe']

    #admin_entry = ttk.Combobox(create_plan_frame, values=[i for i in map(str, admin_df['user_id'].tolist())], width=50)
    admin_entry=tk.Entry(create_plan_frame,width=45, bd=2, font="calibri 10")
    admin_entry.insert(0,'1')
    admin_entry.config(state='readonly')
    # admin_id= admin_df.loc[admin_df['username']==entered_username, 'user_id'].tolist()
    # admin_entry= ttk.Combobox(create_plan_frame, values= admin_id, width=50)
    name_entry = tk.Text(create_plan_frame, width=45, height=1, bd=2, font="calibri 10")
    desc_entry = tk.Text(create_plan_frame, font="calibri 10", width=45, height=4, bd=4)
    # geo_entry = tk.Text(create_plan_frame, width=43, height=1, bd=2, font="calibri 10")
    geo_entry = ttk.Combobox(create_plan_frame, values=[i for i in country], width=50)
    #start_entry = tk.Text(create_plan_frame, width=43, height=1, bd=2, font="calibri 10")
    start_entry = tk.Entry(create_plan_frame, width=45, bd=2, font="calibri 10")
    #end_entry = tk.Text(create_plan_frame, width=43, height=1,  bd=2, font="calibri 10")
    camps_entry = ttk.Combobox(create_plan_frame, values=[i for i in range(1, 21)], width=50)

    admin_entry.place(x=300,y=150)
    name_entry.place(x=300,y=200)
    desc_entry.place(x=300,y=250)
    geo_entry.place(x=300,y=350)
    start_entry.place(x=300,y=400)
    #end_entry.place(x=250,y=400)
    camps_entry.place(x=300, y=450)

    #button
    tk.Button(create_plan_frame,text="Back", bg="#FFFFFF", fg="black", width=10, height=1,command=lambda:back(create_plan_frame)).place(x=220, y=650)
    tk.Button(create_plan_frame,text="Clear", bg="#FFFFFF", fg="black", width=10, height=1, command=clear).place(x=320, y=650)
    tk.Button(create_plan_frame,text="Submit", bg="#FFFFFF", fg="black", width=10, height=1, command=submit_plan).place(x=420, y=650)

    create_plan_frame.grid(row=0,column=0, sticky="nsew")
    return create_plan_frame

if __name__ == '__main__':
    plan_creator_frame(tk.Tk())        #will only execute in this file, for testing purposes only
    root.mainloop()





#Not used: but i'll save it here for info
# root = tk.Tk()
# root.title("Create new plan")  # --Can change this later, only for demo
# root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
# root.geometry("600x600")
# root['bg'] = '#021631'