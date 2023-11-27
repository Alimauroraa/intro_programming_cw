import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from datetime import date as d, datetime as dt
import logging
from create_plan import HumanitarianPlan
import admin_home_frame

logging.basicConfig(level=logging.INFO,filename='create_plan_logging.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

admin_df = pd.read_csv("admin_credentials.csv")

def back(create_plan_frame):
    create_plan_frame.grid_forget()
    #admin_home_frame.home_frame.tkraise()

def clear():
    admin_entry.set('')
    name.set('')
    desc_entry.delete(1.0,tk.END)
    geo.set('')
    start.set('')
    end.set('')
    camps_entry.set('')

def validate_input(admin_id, plan_name, description,geographical_area, start_date,closing_date,number_camps):
    #validate admin id
    if len(admin_id)==0:
        messagebox.showerror("Error", "Required. Please select the admin id")
        return False        #by returning False, this will prevent us from adding it to csv

    #validate plan name
    if len(plan_name)==0:
        messagebox.showerror("Error", "Required. Please enter the plan name")
        return False
    elif not all(char.isalpha() or char.isspace() for char in plan_name) and 1 < len(plan_name) < 200:
        messagebox.showerror("Error", "Please enter a valid plan name, alphabetical character only")
        return False
    else:
        logging.info(f"Plan name: {plan_name}")

    #validate description
    if len(description)==1:
        messagebox.showerror("Error", "Required. Please enter the description")
        return False

    elif not all(char==',' or char.isalpha() or char.isspace() or char.isdigit() for char in description) and 1 < len(description) < 500:
        messagebox.showerror("Error", "Please enter a valid description")
        return False

    #validate geographical area
    if len(geographical_area)==0:
        messagebox.showerror("Error", "Required. Please enter the geographical area")
        return False
    elif not all(char==',' or char.isalpha() or char.isspace() for char in geographical_area) and 1 < len(geographical_area) < 200:
        messagebox.showerror("Error", "Please enter a valid geographical area, alphabetical character only")
        return False

    #validate start date
    if len(start_date)==0:
        messagebox.showerror("Error", "Required. Please enter a start date")
        return False
    else:
        try:
            start = d.fromisoformat(start_date)
            if start > dt.now().date():
                print(start)
            else:
                messagebox.showerror("Error", "Start date should be later than current date")
                return False
        except ValueError as e:
            messagebox.showerror("Error", "Required. Please enter a start date in YYYY-MM-DD format")
            return False

    # validate end date
    if len(closing_date) == 0:
        messagebox.showerror("Error", "Required. Please enter a closing date")
        return False
    else:
        try:
            end = d.fromisoformat(closing_date)
            if end > dt.now().date() and end > start:
                print(end)
            else:
                messagebox.showerror("Error", "Closing date should be later than current and start date")
                return False
        except ValueError as e:
            messagebox.showerror("Error", "Required. Please enter a start date in YYYY-MM-DD format")
            return False

    # validate number of camps
    if len(number_camps) == 0:
        messagebox.showerror("Error", "Required. Please select of camps")
        return False
    messagebox.showinfo("Success","Plan is created")
    return True                                 #if all checks are ok, it'll return True

def submit_plan():
    # Retrieve the entry
    admin_id = admin_entry.get()
    plan_name = name_entry.get()
    description = desc_entry.get(1.0, tk.END)
    geographical_area = geo_entry.get()
    start_date = start_entry.get()
    closing_date = end_entry.get()
    number_camps = camps_entry.get()

    if validate_input(admin_id, plan_name, description, geographical_area, start_date, closing_date, number_camps):
        # Create the plan
        new_plan = HumanitarianPlan(admin_id, plan_name, description, geographical_area, start_date, closing_date, number_camps)
        camp_ids = new_plan.create_plan()  # Assume this method now returns the camp_ids

        # Generate camps based on the created plan
        new_plan.generate_camps_from_plan(camp_ids)

        # Inform the user that the plan and camps have been created
        messagebox.showinfo("Success", "Plan and associated camps created successfully.")

def plan_creator_frame(parent):
    # initializing
    create_plan_frame=tk.Frame(parent,width=600, height=600, bg='#021631')

    #heading
    tk.Label(create_plan_frame, text="Create new humanitarian plan", font="calibri 16",bg="#021631", fg="#fff").place(x=20,y=20)

    #label
    tk.Label(create_plan_frame, text="Admin id", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=100)
    tk.Label(create_plan_frame, text="Plan name", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=150)
    tk.Label(create_plan_frame, text="Description", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=200)
    tk.Label(create_plan_frame, text="Geographical Area", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=300)
    tk.Label(create_plan_frame, text="Start date (YYYY-MM-DD)", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=350)
    tk.Label(create_plan_frame, text="Closing date (YYYY-MM-DD)", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=400)
    tk.Label(create_plan_frame, text="Number of camps", font="calibri 12", bg="#021631",fg="#fff").place(x=45,y=450)

    #Entry
    global name
    global geo
    global start
    global end
    name=tk.StringVar()
    geo=tk.StringVar()
    start=tk.StringVar()
    end=tk.StringVar()

    #defining the entries as global variable
    global admin_entry
    global name_entry
    global desc_entry
    global geo_entry
    global start_entry
    global end_entry
    global camps_entry

    admin_entry=ttk.Combobox(create_plan_frame, values= [i for i in map(str,admin_df['user_id'].tolist())], width=48)
    name_entry=tk.Entry(create_plan_frame, textvariable=name, width=43, bd=2, font="calibri 10")
    desc_entry=tk.Text(create_plan_frame, font="calibri 10",width=43,height=4, bd=4)
    geo_entry=tk.Entry(create_plan_frame, textvariable=geo, width=43, bd=2, font="calibri 10")
    start_entry=tk.Entry(create_plan_frame, textvariable=start, width=43, bd=2, font="calibri 10")
    end_entry=tk.Entry(create_plan_frame, textvariable=end, width=43, bd=2, font="calibri 10")
    camps_entry= ttk.Combobox(create_plan_frame, values=[i for i in range(1,21)], width=48)

    admin_entry.place(x=250,y=100)
    name_entry.place(x=250,y=150)
    desc_entry.place(x=250,y=200)
    geo_entry.place(x=250,y=300)
    start_entry.place(x=250,y=350)
    end_entry.place(x=250,y=400)
    camps_entry.place(x=250, y=452)

    #button
    tk.Button(create_plan_frame,text="Back", bg="#FFFFFF", fg="black", width=10, height=1,command=lambda:back(create_plan_frame)).place(x=170, y=550)
    tk.Button(create_plan_frame,text="Clear", bg="#FFFFFF", fg="black", width=10, height=1, command=clear).place(x=270, y=550)
    tk.Button(create_plan_frame,text="Submit", bg="#FFFFFF", fg="black", width=10, height=1, command=submit_plan).place(x=370, y=550)

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