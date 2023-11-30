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

def validate_date(plan_id,closing_date):
    # validate end date
    if len(closing_date) == 0:
        messagebox.showerror("Error", "Required. Please enter a closing date")
        return False
    else:
        try:
            matching_row=plan_df.loc[plan_df['PlanID']== int(plan_id)]
            if len(matching_row) > 0:
                start = pd.to_datetime(matching_row['startDate']).dt.date.iloc[0]
                end= dt.strptime(closing_date,'%Y-%m-%d').date()
            if end >= dt.now().date() and end > start:
                return True
            else:
                messagebox.showerror("Error", "Closing date should be later than current and start date")
                return False
        except ValueError as e:
            messagebox.showerror("Error", "Required. Please enter a start date in YYYY-MM-DD format")
            return False
    return True

def submit_date():
    #retrieve entry
    plan_id= plan_id_entry.get()
    closing_date = end_entry.get()
    if validate_date(plan_id,closing_date):
        plan_df.loc[plan_df['PlanID']==int(plan_id), 'closingDate']=closing_date
        plan_df.to_csv('plan.csv', index=False)
        messagebox.showinfo("Success", f"Closing date updated for Plan ID {plan_id}")

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

    plan_id_entry = ttk.Combobox(close_plan_frame, values=[i for i in map(str, plan_df['PlanID'].tolist())], width=31)
    end_entry = tk.Entry(close_plan_frame, width=29, bd=2, font="calibri 10")

    plan_id_entry.place(x=239, y=260)
    end_entry.place(x=239, y=360)

    # button
    tk.Button(close_plan_frame, text="Back", bg="#FFFFFF", fg="black", width=10, height=1,
              command=lambda: back(close_plan_frame)).place(x=200, y=600)
    tk.Button(close_plan_frame, text="Clear", bg="#FFFFFF", fg="black", width=10, height=1, command=clear).place(x=300,
                                                                                                                  y=600)
    tk.Button(close_plan_frame, text="Submit", bg="#FFFFFF", fg="black", width=10, height=1,
              command=submit_date).place(x=400, y=600)

    close_plan_frame.grid(row=0, column=0, sticky="nsew")
    return close_plan_frame


if __name__ == '__main__':
    close_plan_frame(tk.Tk())  # will only execute in this file, for testing purposes only
    root.mainloop()


