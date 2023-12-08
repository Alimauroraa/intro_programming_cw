import tkinter as tk
#import the login page for volunteer and admin
from admin_login_gui import Admin
from create_plan import HumanitarianPlan

root = None
def admin_login_page(root):
    root.withdraw()
    admin_login_frame = Admin("", "", "", home_page, root)
    admin_login_frame.create_login_frame()



def open_volunteer_login(root):
    root.withdraw()
    from GUI_volunteer_login_update import login
    login()

def home_page():
    bg_color = '#021631'

    # Main frame initialization
    root = tk.Tk()
    root.title("The Hope Trust: A Humanitarian Management System")
    root.geometry('400x350+0+0')
    root['bg'] = bg_color

    # Creating frame
    home = tk.Frame(root, width=600, height=600, bg=bg_color)
    home.pack_propagate(False)
    home.pack()

    # Home page components
    # Load the image each time the function is called
    logo_image = tk.PhotoImage(file="images/logo2.gif")
    logo_widget = tk.Label(
        home,
        image=logo_image,
        width=150,
        height=150,
        bg=bg_color
    )
    logo_widget.image = logo_image  # Keep a reference to the image
    logo_widget.pack(expand=False, fill='none', padx=10, pady=20)

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
        command=lambda: open_volunteer_login(root)).pack()     #this will open page volunteer login when clicked
    root.mainloop()

if __name__=='__main__':
    home_page()
    # Create an instance of HumanitarianPlan and call the method
    humanitarian_plan_instance = HumanitarianPlan(None, None, None, None, None, None)
###