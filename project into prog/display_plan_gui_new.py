import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from close_plan import ClosePlan
def load_plan_ids():
    df = pd.read_csv("plan.csv")
    return sorted(df['PlanID'].dropna().unique())

def display_plan():
    try:
        plan_id = int(combo.get())
        df = pd.read_csv("plan.csv")
        plan_info = df[df['PlanID'] == plan_id]
        if not plan_info.empty:
            show_info(plan_info)
        else:
            display_error("Plan ID not found.")
    except ValueError:
        display_error("Please enter a valid Plan ID.")

def display_volunteers(parent, dataframe):
    camp_id = []
    # Find CampID and get corresponding volunteer data
    if 'camp_id' in dataframe.columns:
        camps = dataframe.iloc[0]['camp_id']
        camp_list = [int(item) for item in camps.split(",")]
        volunteer_csv = pd.read_csv("volunteers_file.csv")
        volunteers_for_plan = volunteer_csv[volunteer_csv['camp_id'].isin(camp_list)]

        # Create a new top-level window
        volunteer_window = tk.Toplevel(parent)
        volunteer_window.title("Volunteers for Plan")

        # Create Treeview widget
        tree = ttk.Treeview(volunteer_window)
        tree["columns"] = list(volunteers_for_plan.columns)
        tree["show"] = "headings"

        # Define headings
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data into the treeview
        for idx, row in volunteers_for_plan.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill='both')

def display_refugees(parent, dataframe):
    camp_id = []
    # Find CampID and get corresponding volunteer data
    if 'camp_id' in dataframe.columns:
        camps = dataframe.iloc[0]['camp_id']
        camp_list = [int(item) for item in camps.split(",")]
        refugees_csv = pd.read_csv("Refugee_DataFrame.csv")
        refugees_for_plan = refugees_csv[refugees_csv['Camp_ID'].isin(camp_list)]

        # Create a new top-level window
        refugees_window = tk.Toplevel(parent)
        refugees_window.title("Refugees for Plan")

        # Create Treeview widget
        tree = ttk.Treeview(refugees_window)
        tree["columns"] = list(refugees_for_plan.columns)
        tree["show"] = "headings"

        # Define headings
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data into the treeview
        for idx, row in refugees_for_plan.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill='both')
def show_info(dataframe):
    top = tk.Toplevel(root)
    top.title("Plan Details")
    top['bg']='#021631'

    frame = tk.Frame(top,bg='#021631')
    frame.pack(padx=20, pady=10, expand=True, fill='both')

    for idx, col in enumerate(dataframe.columns):
        if col == 'active':
            active_value = dataframe.iloc[0][col]
            message = "Plan is currently active" if active_value != 0 else "Plan is inactive"
            messagebox.showinfo("Plan Status", message)
        if col=='closingDate':
            dataframe['closingDate']=pd.to_datetime(dataframe[col], errors='coerce').dt.strftime('%Y-%m-%d')
        label = tk.Label(frame, text=col, bg='#021631',
                         fg="white", font=("Calibri", 10))
        label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(frame, width=100)
        entry.insert(tk.END, str(dataframe.iloc[0][col]))
        entry.grid(row=idx, column=1, padx=20, pady=10, sticky="w")
        entry.config(state=tk.DISABLED)  # Make the entry non-editable

    # Add the 'Display Volunteers for Plan' button at the bottom
    volunteers_button = tk.Button(frame, text="Display Volunteers for Plan",bg="#FFFFFF", fg="black",command=lambda: display_volunteers(top, dataframe))
    volunteers_button.grid(row=len(dataframe.columns) + 1, column=0, pady=10, padx=50)

    refugees_button = tk.Button(frame, text="Display Refugees for Plan",bg="#FFFFFF", fg="black",command=lambda: display_refugees(top, dataframe))
    refugees_button.grid(row=len(dataframe.columns) + 1, column=1, pady=10, padx=20)

error_label= None
def display_error(message):
    global error_label
    if error_label is not None:
        error_label.config(text=message)

def back(root):
    root.grid_forget()

def date_parser(x):
    formats = ['%Y-%m-%d', '%m-%d-%Y', '%m/%d/%Y', '%Y/%m/%d' ]  # Add more formats as needed
    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except ValueError:
            pass
    return pd.NaT

def update_active_flag():
    today_date = datetime.now().date()
    df = pd.read_csv('plan.csv', parse_dates=['startDate', 'closingDate'], date_parser=date_parser)

    # Check if the 'startDate' matches the current date and update 'active' column accordingly
    df.loc[df['closingDate'].dt.date >= today_date, 'active'] = 0

    # Save the updated dataframe back to the CSV file
    df.to_csv('plan.csv', index=False)

    df.close()
def display_all_plan(root):
    df = pd.read_csv('plan.csv', parse_dates=['startDate', 'closingDate'], date_parser=date_parser)

    # Convert the dates to the desired format
    df['startDate'] = df['startDate'].dt.strftime('%Y-%m-%d')
    df['closingDate'] = df['closingDate'].dt.strftime('%Y-%m-%d')

    new_window=tk.Toplevel(root)
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


def display_plan_frame(parent):
    global root
    # Create tkinter window
    root = tk.Frame(parent,width=600, height=600, bg='#021631')
    root.grid_propagate(False)
    #root.title("Display Plan")

    # Create label and entry for Plan ID
    tk.Label(root, text="Select Plan ID",font="calibri 16",bg="#021631", fg="#fff").place(x=240,y=200)

    global combo
    plan_ids = load_plan_ids()
    combo = ttk.Combobox(root, values=plan_ids, state='readonly')
    combo.place(x=230, y=270)
    #entry = tk.Entry(root,width=20, bd=2, font="calibri 10")
    #entry.place(x=230, y=270)

    # Create 'Display Plan' button
    button = tk.Button(root, text="Display Plan", bg="#FFFFFF", command=display_plan)
    button.place(x=270, y=320)

    tk.Button(root, text="Display all plans", bg="#FFFFFF", fg="black", width=15, height=1,
              command=lambda: display_all_plan(root)).place(x=50, y=100)

    back_button=tk.Button(root, text="Back", width=10, bg="#FFFFFF", command=lambda:back(root))
    back_button.place(x=270, y=500)
    # error_label = ttk.Label(root, text="", foreground="red")
    # error_label.pack()

    return root
    # Run the tkinter main loop
    #root.mainloop()

if __name__=='__main__':
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    root.geometry("600x600")
    root['bg'] = '#021631'
    display_plan_frame(root)

    frame=display_plan_frame(root)
    frame.pack()

    root.mainloop()
