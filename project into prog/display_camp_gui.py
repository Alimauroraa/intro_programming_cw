import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

def display_camp():
    try:
        camp_id = int(camp_entry.get())
        df = pd.read_csv("camps.csv")

        if 'CampID' in df.columns and not df.empty:
            df['CampID'] = df['CampID'].astype(int)

            if camp_id in df['CampID'].values:
                camp_info = df[df['CampID'] == camp_id]
                show_camp_table(camp_info)
            else:
                messagebox.showerror("Error", "Camp ID not found")
        else:
            messagebox.showerror("Error", "No camps available")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid camp ID, numerical characters only")

def show_camp_table(dataframe):
    top = tk.Toplevel(root)
    top.title("Camp Details")

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

def back(root):
    root.grid_forget()

def display_camp_frame(parent):
    global root, camp_entry
    root = tk.Frame(parent, width=600, height=600, bg='#021631')
    root.grid_propagate(False)

    tk.Label(root, text="Enter Camp ID", font="calibri 16", bg="#021631", fg="#fff").place(x=240, y=200)

    camp_entry = tk.Entry(root, width=20, bd=2, font="calibri 10")
    camp_entry.place(x=230, y=270)

    button = tk.Button(root, text="Display Camp", bg="#FFFFFF", command=display_camp)
    button.place(x=270, y=320)

    back_button = tk.Button(root, text="Back", width=10, bg="#FFFFFF", command=lambda: back(root))
    back_button.place(x=270, y=500)

    return root

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")
    root.geometry("600x600")
    root['bg'] = '#021631'
    display_camp_frame(root)

    frame = display_camp_frame(root)
    frame.pack()

    root.mainloop()
