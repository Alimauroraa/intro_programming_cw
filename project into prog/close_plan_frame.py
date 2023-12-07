import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from datetime import date as d, datetime as dt
import logging
import create_plan_frame

plan_df=pd.read_csv('plan.csv')
def back(close_plan_frame):
    close_plan_frame.grid_forget()

def clear():
    plan_id_entry.set('')
    end_entry.delete(0,tk.END)

def validate_date(plan_id, closing_date):
    # validate end date
    if len(closing_date) == 0:
        messagebox.showerror("Error", "Required. Please enter a closing date")
        return False
    else:
        try:
            matching_row = plan_df.loc[plan_df['PlanID'] == int(plan_id)]
            if len(matching_row) > 0:
                # Handle potential NaT in startDate
                if pd.isna(matching_row['startDate'].iloc[0]):
                    messagebox.showerror("Error", "Cannot terminate the plan as the start date is not set.")
                    return False
                start = pd.to_datetime(matching_row['startDate']).dt.date.iloc[0]
                end = dt.strptime(closing_date, '%Y-%m-%d').date()
                if end >= dt.now().date() and end > start:
                    return True
                else:
                    messagebox.showerror("Error", "Closing date should be later than current and start date")
                    return False
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}. Please enter the date in YYYY-MM-DD format")
            return False
    return True

def date_parser(x):
    formats = ['%Y-%m-%d', '%m-%d-%Y', '%m/%d/%Y', '%Y/%m/%d' ]  # Add more formats as needed
    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except ValueError:
            pass
    return pd.NaT

def update_active_flag():
    today_date = dt.now().date()
    df = pd.read_csv('plan.csv', parse_dates=['startDate', 'closingDate'], date_parser=date_parser)

    # Check if the 'startDate' matches the current date and update 'active' column accordingly
    df.loc[df['closingDate'].dt.date >= today_date, 'active'] = 0

    # Save the updated dataframe back to the CSV file
    df.to_csv('plan.csv', index=False)

def display_plan(close_plan_frame):
    df = pd.read_csv('plan.csv', parse_dates=['startDate', 'closingDate'], date_parser=date_parser)

    # Convert the dates to the desired format
    df['startDate'] = df['startDate'].dt.strftime('%m/%d/%Y')
    df['closingDate'] = df['closingDate'].dt.strftime('%m/%d/%Y')

    new_window=tk.Toplevel(close_plan_frame)
    new_window.title('Plans Table')

    #create treeview to display table
    tree=ttk.Treeview(new_window, show='headings')
    tree['columns']=list(df.columns)

    #display columns
    for col in df.columns:
        tree.column(col, anchor='center')
        tree.heading(col, text=col, anchor='center')

    for i, row in df.iterrows():
        #formatted_row=[str(val).replace('-','/') if isinstance(val,pd.Timestamp) else val for val in row]
        tree.insert('','end', values=list(row))

    #adding scrollbar
    scrollbar= ttk.Scrollbar(new_window, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    tree.pack(expand=True, fill='both')

def submit_date():
    global plan_df
    plan_id= plan_id_entry.get()
    closing_date = end_entry.get()
    if validate_date(plan_id, closing_date):
        try:
            plan_df = pd.read_csv('plan.csv')  # Read the latest plan data
            if int(plan_id) in plan_df['PlanID'].values:
                plan_df.loc[plan_df['PlanID'] == int(plan_id), 'closingDate'] = closing_date
                plan_df.to_csv('plan.csv', index=False)
                messagebox.showinfo("Success", f"Closing date updated for Plan ID {plan_id}")
            else:
                messagebox.showerror("Error", f"No plan found with ID {plan_id}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def close_plan_frame(parent):
    # initializing
    close_plan_frame = tk.Frame(parent, width=600, height=600, bg='#021631')

    # heading
    tk.Label(close_plan_frame, text="Terminate humanitarian plan", font="calibri 16", bg="#021631", fg="#fff").place(
        x=50, y=50)

    # label
    tk.Label(close_plan_frame, text="Plan ID", font="calibri 12", bg="#021631", fg="#fff").place(x=320,y=230)
    tk.Label(close_plan_frame, text="Closing date (YYYY-MM-DD)", font="calibri 12", bg="#021631", fg="#fff").place(
        x=250, y=330)

    # defining the entries as global variable
    global plan_id_entry
    global end_entry
    plan_df=pd.read_csv('plan.csv')
    active_plans=plan_df[plan_df['active']==1]['PlanID'].tolist()    #filter only active plans
    plan_id_entry = ttk.Combobox(close_plan_frame, values=[str(i) for i in active_plans], width=31)
    end_entry = tk.Entry(close_plan_frame, width=29, bd=2, font="calibri 10")

    plan_id_entry.place(x=239, y=280)
    end_entry.place(x=239, y=380)

    # button
    tk.Button(close_plan_frame,text="Display all plans",bg="#FFFFFF", fg="black", width=15, height=1,
              command=lambda:display_plan(close_plan_frame)).place(x=70, y=170)
    tk.Button(close_plan_frame, text="Back", bg="#FFFFFF", fg="black", width=10, height=1,
              command=lambda: back(close_plan_frame)).place(x=220, y=670)
    tk.Button(close_plan_frame, text="Clear", bg="#FFFFFF", fg="black", width=10, height=1, command=clear).place(x=320,
                                                                                                                  y=670)
    tk.Button(close_plan_frame, text="Submit", bg="#FFFFFF", fg="black", width=10, height=1,
              command=submit_date).place(x=420, y=670)

    close_plan_frame.grid(row=0, column=0, sticky="nsew")
    return close_plan_frame


if __name__ == '__main__':
    close_plan_frame(tk.Tk())  # will only execute in this file, for testing purposes only
    root.mainloop()


