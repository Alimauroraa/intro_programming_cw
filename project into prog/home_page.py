import tkinter as tk
#import the login page for volunteer and admin
from admin_login_gui import Admin
from create_plan import HumanitarianPlan

def admin_login_page():
    admin_login_frame=Admin("","","")
    admin_login_frame.create_login_frame()

def home_page():
    bg_color = '#021631'

    #main frame initialisation
    root = tk.Tk()
    root.title("The Hope Trust: A Humanitarian Management System")  # --Can change this later, only for demo
    root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen
    root.geometry("600x600")
    root['bg'] = '#021631'

    # creating frame
    home = tk.Frame(root, width=600, height=600, bg=bg_color)
    # admin = tk.Frame(root, bg=bg_color)
    # volunteer = tk.Frame(root, bg=bg_color)
    # for frame in (home, admin, volunteer):
    #home.grid(row=0, column=0, sticky="nsew")

    home.pack_propagate(False)
    home.pack()

    # home page components
    logo_image = tk.PhotoImage(file="images/logo2.gif")
    logo_widget = tk.Label(
        home,
        image=logo_image,
        width=250,
        height=250,
        bg=bg_color
    )
    logo_widget.image = logo_image
    logo_widget.pack(expand=False, fill='none', padx=10,pady=50)

    tk.Label(
        home,
        text="Welcome change makers! Ready to make an impact?",
        bg=bg_color,
        fg="white",
        font=("Calibri", 16)
    ).pack()

    # button components
    tk.Button(
        home,
        text="Admin",
        font=("Calibri", 12),
        width=15,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=admin_login_page).pack(padx=20,pady=30)  #this will open admin login page when clicked

    tk.Button(
        home,
        text="Volunteer",
        font=("Calibri", 12),
        width=15,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda: open_frame(volunteer)).pack()     #this will open page volunteer login when clicked

    root.mainloop()

if __name__=='__main__':
    home_page()
    # Create an instance of HumanitarianPlan and call the method
    humanitarian_plan_instance = HumanitarianPlan(None, None, None, None, None, None, None)
    humanitarian_plan_instance.generate_missing_camps_from_plans()