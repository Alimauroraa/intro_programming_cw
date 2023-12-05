import tkinter as tk
from tkinter import ttk
import create_plan_frame
import display_plan_gui_new

import close_plan_frame

from manage_camps_frame import ManageCampsFrame
import EditVolunteerAccount
import allocatesrourcesnew
import livefeed


bg_color = '#021631'

# def switch_frame(frame):
#     frame.tkraise()

def plan_creator_frame(root):
    create_plan_frame.plan_creator_frame(root)
def allocate_volunteer():
    pass

def plan_summary_frame(root):
    display_plan_gui_new.display_plan_frame(root).grid(row=0, column=0)

def terminate_plan(root):
    close_plan_frame.close_plan_frame(root).grid(row=0, column=0)

def edit_volunteer_frame(root):
    EditVolunteerAccount.edit_volunteer_frame(root).grid(row=0, column=0)

def open_manage_camps(root):
    # Clear existing widgets in root
    for widget in root.winfo_children():
        widget.destroy()

    # Create an instance of ManageCampsFrame
    manage_camps_frame = ManageCampsFrame(root)
    manage_camps_frame.setup_ui()

    # Add a 'Go Back' button
    go_back_button = tk.Button(root, text="Back", width=10, command=lambda: admin_home(root))
    go_back_button.place(x=370,y=600)

def allocate_resources_frame(root):
    allocatesrourcesnew.create_gui(root).grid(row=0, column=0)

def live_feed_frame(root):
    livefeed.livefeed_frame(root).grid(row=0, column=0)

def admin_home(root):
    # initializing
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 600) // 2
    y = (screen_height - 850) // 2
    # root.geometry("600x600")
    root.geometry(f"700x800+{x}+{y}")
    root['bg'] = '#021631'

    # frames
    home_frame = tk.Frame(root, width=800, height=600, bg=bg_color)
    home_frame.grid(row=0, column=0, sticky="nsew")
    tk.Label(
        home_frame,
        text="Welcome admin! What do you want to do for today?",
        bg=bg_color,
        fg="white",
        font=("Calibri", 14)
    ).pack(padx=150, pady=150)

    # button components
    tk.Button(
        home_frame,
        text="Create plan",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:plan_creator_frame(root)).place(x=286,y=250)  # this will open admin login page when clicked

    tk.Button(
        home_frame,
        text="Terminate plan",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:terminate_plan(root)).place(x=286, y=300)  # this will open admin login page when clicked

    tk.Button(
        home_frame,
        text="View plan summary",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:plan_summary_frame(root)).place(x=286,y=350)  # this will open admin login page when clicked

    tk.Button(
        home_frame,
        text="Edit volunteer",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:edit_volunteer_frame(root)).place(x=286,y=400)  # this will open admin login page when clicked

    tk.Button(
        home_frame,
        text="Allocate volunteer",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=allocate_volunteer).place(x=286, y=550)

    tk.Button(
        home_frame,
        text="Allocate resources",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:allocate_resources_frame(root)).pack(padx=50,pady=170) # this will open admin login page when clicked

    tk.Button(
        home_frame,
        text="See live feed",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda:live_feed_frame(root)).place(x=286, y=600)


    manage_camps_button = tk.Button(
        home_frame,
        text="Manage Camps",
        font=("Calibri", 12),
        width=16,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda: open_manage_camps(root)  # This button will call the open_manage_camps function
    )
    manage_camps_button.place(x=286, y=450)  # Adjust the position as needed

    root.deiconify()

if __name__=='__main__':
    # initializing
    root = tk.Tk()
    root.title("Admin")
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    root.geometry("700x800")
    root['bg'] = '#021631'

    # frames
    home_frame = tk.Frame(root, width=800, height=600, bg=bg_color)
    home_frame.grid(row=0, column=0, sticky="nsew")
    # create_plan=tk.Frame(home_frame)

    admin_home(root)

    root.mainloop()

