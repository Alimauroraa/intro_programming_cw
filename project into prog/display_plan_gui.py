# import pandas as pd
# import tkinter as tk
# plan_id = int(input("please enter the plan ID you would like to display: "))
# def DisplayPlan(csv,plan_id):
#     df = pd.read_csv(csv)
#     plan_info = df[df.PlanID == plan_id]
#     print(plan_info)
#
# DisplayPlan("plan.csv",1)
#
import tkinter as tk
from tkinter import ttk
import pandas as pd
def display_plan():
    try:
        plan_id = int(entry.get())
        df = pd.read_csv("plan.csv")
        plan_info = df[df['PlanID'] == plan_id]
        show_table(plan_info)
    except ValueError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Please enter a valid Plan ID.")
        result_text.config(state=tk.DISABLED)

def show_table(dataframe):
    top = tk.Toplevel(root)
    top.title("Plan Details")

    tree = ttk.Treeview(top)
    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")

    tree.configure(yscrollcommand=scrollbar.set)

    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    for column in dataframe.columns:
        tree.heading(column, text=column)

    for index, row in dataframe.iterrows():
        tree.insert("", tk.END, values=list(row))

def display_plan_frame(parent):
    # Create tkinter window
    root = tk.Frame(parent,width=600, height=600, bg='#021631')
    root.pack_propagate(False)
    #root.title("Display Plan")

    # Create label and entry for Plan ID
    tk.Label(root, text="Enter Plan ID",font="calibri 16",bg="#021631", fg="#fff").place(x=240,y=200)

    global entry
    entry = tk.Entry(root,width=20, bd=2, font="calibri 10")
    entry.place(x=230, y=270)

    # Create 'Display Plan' button
    button = tk.Button(root, text="Display Plan", bg="#FFFFFF", command=display_plan)
    button.place(x=270, y=320)

    # Create text widget to display the result
    # global result_text
    # result_text = tk.Text(root, height=10, width=50)
    # result_text.pack()
    # result_text.config(state=tk.DISABLED)

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