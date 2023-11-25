import tkinter as tk
from tkinter import ttk
import create_plan_frame
import display_plan_gui
import close_plan_frame

bg_color = '#021631'

# def switch_frame(frame):
#     frame.tkraise()

def plan_creator_frame(root):
    # # initializing
    # root = tk.Tk()
    # root.title("Admin home page")
    # root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    # root.geometry("600x600")
    # root['bg'] = '#021631'
    #
    # home_frame = tk.Frame(root, width=800, height=600, bg=bg_color)
    # home_frame.grid(row=0, column=0, sticky="nsew")
    create_plan_frame.plan_creator_frame(root)
    #switch_frame(create_plan_frame.plan_creator_frame(tk.Tk()))


def plan_summary_frame(root):
    display_plan_gui.display_plan_frame(root).grid(row=0, column=0)

def terminate_plan(root):
    close_plan_frame.close_plan_frame(root).grid(row=0, column=0)

def edit_volunteer_frame():
    pass

def allocate_resources_frame():
    pass

def admin_home(root):
    # initializing
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 550) // 2
    y = (screen_height - 600) // 2
    # root.geometry("600x600")
    root.geometry(f"600x600+{x}+{y}")
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
    ).pack(padx=100, pady=150)

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
        command=lambda:plan_creator_frame(root)).place(x=236,y=250)  # this will open admin login page when clicked

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
        command=lambda:terminate_plan(root)).place(x=236, y=300)  # this will open admin login page when clicked

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
        command=lambda:plan_summary_frame(root)).place(x=236,y=350)  # this will open admin login page when clicked

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
        command=edit_volunteer_frame).place(x=236,y=450)  # this will open admin login page when clicked

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
        command=allocate_resources_frame).pack(pady=70) # this will open admin login page when clicked

    root.mainloop()

if __name__=='__main__':
    # initializing
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    root.geometry("600x600")
    root['bg'] = '#021631'

    # frames
    home_frame = tk.Frame(root, width=800, height=600, bg=bg_color)
    home_frame.grid(row=0, column=0, sticky="nsew")
    # create_plan=tk.Frame(home_frame)

    admin_home(root)

    root.mainloop()

