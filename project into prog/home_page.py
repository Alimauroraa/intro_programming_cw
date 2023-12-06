import tkinter as tk
#import the login page for volunteer and admin
from admin_login_gui import Admin
from create_plan import HumanitarianPlan

def admin_login_page(root):
    root.withdraw()
    admin_login_frame=Admin("","","")
    admin_login_frame.create_login_frame()

def open_volunteer_login():
    from GUI_volunteer_login_update import login
    login()

def home_page():
    bg_color = '#021631'

    #main frame initialisation
    root = tk.Tk()
    root.title("The Hope Trust: A Humanitarian Management System")  # --Can change this later, only for demo
    #root.eval("tk::PlaceWindow . center")  # --Placing the window on the centre of the screen

    #screen_width=root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()

    #x= (screen_width-600)//2
    #y=(screen_height-750)//2
    #root.geometry("600x600")
    #root.geometry(f"700x700+{x}+{y}")
    root.geometry('400x350+0+0')
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
        width=150,
        height=150,
        bg=bg_color
    )
    logo_widget.image = logo_image
    logo_widget.pack(expand=False, fill='none', padx=10,pady=20)

    tk.Label(
        home,
        text="Welcome change makers! Ready to make an impact?",
        bg=bg_color,
        fg="white",
        font=("Calibri", 12, 'bold')
    ).pack()

    # button components
    tk.Button(
        home,
        text="Admin",
        font=("Calibri", 11),
        width=10,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda: admin_login_page(root)).pack(padx=20,pady=15)  #this will open admin login page when clicked

    tk.Button(
        home,
        text="Volunteer",
        font=("Calibri", 11),
        width=10,
        height=0,
        bg="#FFFFFF",
        fg="black",
        cursor="hand2",
        activebackground="#B8B8B8",
        activeforeground="black",
        command=lambda: open_volunteer_login()).pack()     #this will open page volunteer login when clicked

    root.mainloop()

if __name__=='__main__':
    home_page()
    # Create an instance of HumanitarianPlan and call the method
    humanitarian_plan_instance = HumanitarianPlan(None, None, None, None, None, None)
