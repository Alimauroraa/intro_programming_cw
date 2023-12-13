import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from close_plan import ClosePlan
from PIL import Image, ImageTk


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

        volunteer_window = tk.Toplevel(parent)
        volunteer_window.title("Volunteers for Plan")

        tree = ttk.Treeview(volunteer_window)
        tree["columns"] = list(volunteers_for_plan.columns)
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # Insert data into the treeview
        for idx, row in volunteers_for_plan.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill='both')

def display_map(parent, geographical_area):
    map_window = tk.Toplevel(parent)
    map_window.title("Geographical Map")

    map_image = Image.open("world_map.jpg")  # Replace "world_map.jpg" with the actual image file
    map_photo = ImageTk.PhotoImage(map_image)

    # Create a label to display the map image
    map_label = tk.Label(map_window, image=map_photo)
    map_label.image = map_photo
    map_label.pack()

    # Get the coordinates for the selected geographicalArea
    coordinates = get_country_coordinates(geographical_area)

    # Add a label with a red spot at the specified coordinates
    label = tk.Label(map_window, text="●", font=("Arial", 12), fg="red")
    label.place(x=coordinates[0], y=coordinates[1])

    print(f"Displaying red spot at coordinates: {coordinates}")

def get_country_coordinates(country, image_size=(1425, 625), x_offset=-70,y_offset=10):
    coordinates_lookup = {
        "Afghanistan": (33.9391, 67.7100),
        "Albania": (41.1533, 20.1683),
        "Algeria": (28.0339, 1.6596),
        "Andorra": (42.5063, 1.5218),
        "Angola": (-11.2027, 17.8739),
        "Antigua and Barbuda": (17.0608, -61.7964),
        "Argentina": (-38.4161, -63.6167),
        "Armenia": (40.0691, 45.0382),
        "Australia": (-25.2744, 133.7751),
        "Austria": (47.5162, 14.5501),
        "Azerbaijan": (40.1431, 47.5769),
        "Bahamas": (25.0343, -77.3963),
        "Bahrain": (26.0667, 50.5577),
        "Bangladesh": (23.6850, 90.3563),
        "Barbados": (13.1939, -59.5432),
        "Belarus": (53.7098, 27.9534),
        "Belgium": (50.8503, 4.3517),
        "Belize": (17.1899, -88.4976),
        "Benin": (9.3077, 2.3158),
        "Bhutan": (27.5142, 90.4336),
        "Bolivia": (-16.2902, -63.5887),
        "Bosnia and Herzegovina": (43.9159, 17.6791),
        "Botswana": (-22.3285, 24.6849),
        "Brazil": (-14.2350, -51.9253),
        "Brunei": (4.5353, 114.7277),
        "Bulgaria": (42.7339, 25.4858),
        "Burkina Faso": (12.2383, -1.5616),
        "Burundi": (-3.3731, 29.9189),
        "Cabo Verde": (16.5388, -23.0418),
        "Cambodia": (12.5657, 104.9910),
        "Cameroon": (7.3697, 12.3547),
        "Canada": (56.1304, -106.3468),
        "Central African Republic": (6.6111, 20.9394),
        "Chad": (15.4542, 18.7322),
        "Chile": (-35.6751, -71.5430),
        "China": (35.8617, 104.1954),  # Added China
        "Colombia": (4.5709, -74.2973),
        "Comoros": (-11.6455, 43.3334),
        "Congo (Congo-Brazzaville)": (-0.2280, 15.8277),
        "Costa Rica": (9.7489, -83.7534),
        "Croatia": (45.1000, 15.2000),
        "Cuba": (21.5218, -77.7812),
        "Cyprus": (35.1264, 33.4299),
        "Czechia (Czech Republic)": (49.8175, 15.4720),
        "Denmark": (56.2639, 9.5018),
        "Djibouti": (11.8251, 42.5903),
        "Dominica": (15.4150, -61.3710),
        "Dominican Republic": (18.7357, -70.1627),
        "Ecuador": (-1.8312, -78.1834),
        "El Salvador": (13.7942, -88.8965),
        "Equatorial Guinea": (1.6508, 10.2679),
        "Eritrea": (15.1794, 39.7823),
        "Estonia": (58.5953, 25.0136),
        "Swaziland": (-26.5225, 31.4659),
        "Ethiopia": (9.1450, 40.4897),
        "Fiji": (-17.7134, 178.0650),
        "Finland": (61.9241, 25.7482),
        "Gabon": (-0.8037, 11.6094),
        "Gambia": (13.4432, -15.3101),
        "Georgia": (42.3154, 43.3569),
        "Ghana": (7.9465, -1.0232),
        "Greece": (39.0742, 21.8243),
        "Grenada": (12.1165, -61.6790),
        "Guatemala": (15.7835, -90.2308),
        "Guinea": (9.9456, -9.6966),
        "Guinea-Bissau": (11.8037, -15.1804),
        "Guyana": (4.8604, -58.9302),
        "Haiti": (18.9712, -72.2852),
        "Holy See": (41.9029, 12.4534),
        "Honduras": (15.1991, -86.2419),
        "Hungary": (47.1625, 19.5033),
        "Iceland": (64.9631, -19.0208),
        "India": (20.5937, 78.9629),  # Added India
        "Indonesia": (-0.7893, 113.9213),
        "Iran": (32.4279, 53.6880),
        "Iraq": (33.3152, 44.3661),
        "Ireland": (53.1424, -7.6921),
        "Israel": (31.0461, 34.8516),
        "Italy": (41.8719, 12.5675),
        "Ivory Coast": (7.5399, -5.5471),
        "Jamaica": (18.1096, -77.2975),
        "Japan": (36.2048, 138.2529),  # Added Japan
        "Jordan": (30.5852, 36.2384),
        "Kazakhstan": (48.0196, 66.9237),
        "Kenya": (-1.2921, 36.8219),
        "Kiribati": (-3.3704, -168.7340),
        "Kuwait": (29.3759, 47.9774),
        "Kyrgyzstan": (41.2044, 74.7661),
        "Laos": (19.8563, 102.4955),
        "Latvia": (56.8796, 24.6032),
        "Lebanon": (33.8547, 35.8623),
        "Lesotho": (-29.6099, 28.2336),
        "Liberia": (6.4281, -9.4295),
        "Libya": (26.3351, 17.2283),
        "Liechtenstein": (47.1660, 9.5554),
        "Lithuania": (55.1694, 23.8813),
        "Luxembourg": (49.8153, 6.1296),
        "Madagascar": (-18.7669, 46.8691),
        "Malawi": (-13.2543, 34.3015),
        "Malaysia": (4.2105, 101.9758),
        "Maldives": (3.2028, 73.2207),
        "Mali": (17.5707, -3.9962),
        "Malta": (35.9375, 14.3754),
        "Marshall Islands": (7.1315, 171.1845),
        "Mauritania": (21.0079, -10.9408),
        "Mauritius": (-20.3484, 57.5522),
        "Mexico": (23.6345, -102.5528),
        "Micronesia": (7.4256, 150.5508),
        "Moldova": (47.4116, 28.3699),
        "Monaco": (43.7384, 7.4246),
        "Mongolia": (46.8625, 103.8467),
        "Montenegro": (42.7087, 19.3744),
        "Morocco": (31.7917, -7.0926),
        "Mozambique": (-18.6657, 35.5296),
        "Myanmar (formerly Burma)": (21.9162, 95.9560),
        "Namibia": (-22.9576, 18.4904),
        "Nauru": (-0.5228, 166.9315),
        "Nepal": (28.3949, 84.1240),
        "Netherlands": (52.3676, 4.9041),
        "New Zealand": (-40.9006, 174.8860),
        "Nicaragua": (12.8654, -85.2072),
        "Niger": (17.6078, 8.0817),
        "Nigeria": (9.0820, 8.6753),
        "North Korea": (40.3399, 127.5101),
        "North Macedonia (formerly Macedonia)": (41.6086, 21.7453),
        "Norway": (60.4720, 8.4689),
        "Oman": (21.4735, 55.9754),
        "Pakistan": (30.3753, 69.3451),
        "Palau": (7.5150, 134.5825),
        "Palestine State": (31.3, 34.3),
        "Panama": (8.5379, -80.7821),
        "Papua New Guinea": (-6.314993, 143.95555),
        "Paraguay": (-23.4425, -58.4438),
        "Peru": (-9.1900, -75.0152),
        "Philippines": (12.8797, 121.7740),
        "Poland": (51.9194, 19.1451),
        "Portugal": (39.3999, -8.2245),
        "Qatar": (25.2769, 51.5200),
        "Romania": (45.9432, 24.9668),
        "Russia": (61.5240, 105.3188),
        "Rwanda": (-1.9403, 29.8739),
        "Saint Kitts and Nevis": (17.357822, -62.782998),
        "Saint Lucia": (13.9094, -60.9789),
        "Saint Vincent and the Grenadines": (12.9843, -61.2872),
        "Samoa": (-13.7590, -172.1046),
        "San Marino": (43.9424, 12.4578),
        "Sao Tome and Principe": (0.1864, 6.6131),
        "Saudi Arabia": (23.8859, 45.0792),
        "Senegal": (14.4974, -14.4524),
        "Serbia": (44.0165, 21.0059),
        "Seychelles": (-4.6796, 55.4920),
        "Sierra Leone": (8.4606, -11.7799),
        "Singapore": (1.3521, 103.8198),
        "Slovakia": (48.6690, 19.6990),
        "Slovenia": (46.1512, 14.9955),
        "Solomon Islands": (-9.2010, 160.1562),
        "Somalia": (5.1521, 46.1996),
        "South Africa": (-30.5595, 22.9375),
        "South Korea": (35.9078, 127.7669),
        "South Sudan": (6.8770, 31.3070),
        "Spain": (40.4637, -3.7492),
        "Sri Lanka": (7.8731, 80.7718),
        "Sudan": (12.8628, 30.2176),
        "Suriname": (3.9193, -56.0278),
        "Sweden": (60.1282, 18.6435),
        "Switzerland": (46.8182, 8.2275),
        "Syria": (34.8021, 38.9968),
        "Tajikistan": (38.8610, 71.2761),
        "Tanzania": (-6.369028, 34.8888),
        "Thailand": (15.8700, 100.9925),
    "Timor-Leste": (-8.8742, 125.7275),
    "Togo": (8.6195, 0.8248),
    "Tonga": (-21.1789, -175.1982),
    "Trinidad and Tobago": (10.6918, -61.2225),
    "Tunisia": (33.8869, 9.5375),
    "Turkey": (38.9637, 35.2433),
    "Turkmenistan": (38.9697, 59.5563),
    "Tuvalu": (-7.1095, 177.6493),
    "Uganda": (1.3733, 32.2903),
    "Ukraine": (53.3794, 31.1656),
    "United Arab Emirates": (23.4241, 53.8478),
    "United States": (37.0902, -95.7129),
    "Uruguay": (-32.5228, -55.7658),
    "Uzbekistan": (41.3775, 64.5853),
    "Vanuatu": (-15.3767, 166.9592),
    "Vatican City": (41.9029, 12.4534),
    "Venezuela": (6.4238, -66.5897),
    "Vietnam": (14.0583, 108.2772),
    "Yemen": (15.5524, 48.5164),
    "Zambia": (-13.1339, 27.8493),
    "Zimbabwe": (-19.0154, 29.1549),
    }

    # Convert geographical coordinates to pixel coordinates
    lat, lon = coordinates_lookup.get(country, (0, 0))
    if lat == 0 and lon == 0:
        # Check for an alternative name (e.g., "United States" vs. "USA")
        alt_name = {"United States": "USA"}.get(country)
        lat, lon = coordinates_lookup.get(alt_name, (0, 0))

    if lat == 0 and lon == 0:
        print(f"Unknown coordinates for {country}")
        return (0, 0)  # Return (0, 0) for unknown coordinates

    # Assume the world map spans a certain latitude and longitude range
    lat_range = (90.0, -90.0)  # Latitude range from north to south
    lon_range = (-180.0, 180.0)  # Longitude range from west to east

    # Convert latitude and longitude to pixel coordinates
    pixel_x = int((lon - lon_range[0]) / (lon_range[1] - lon_range[0]) * image_size[0])
    pixel_y = int((lat_range[0] - lat) / (lat_range[0] - lat_range[1]) * image_size[1])

    # Add an offset to the x-coordinate
    pixel_x += x_offset
    pixel_y+= y_offset

    print(f"Calculated pixel coordinates for {country}: ({pixel_x}, {pixel_y})")

    return (pixel_x, pixel_y)
def display_refugees(parent, dataframe):
    camp_id = []
    # Find CampID and get corresponding volunteer data
    if 'camp_id' in dataframe.columns:
        camps = dataframe.iloc[0]['camp_id']
        camp_list = [int(item) for item in camps.split(",")]
        refugees_csv = pd.read_csv("Refugee_DataFrame.csv")
        refugees_for_plan = refugees_csv[refugees_csv['Camp_ID'].isin(camp_list)]

        refugees_window = tk.Toplevel(parent)
        refugees_window.title("Refugees for Plan")

        tree = ttk.Treeview(refugees_window)
        tree["columns"] = list(refugees_for_plan.columns)
        tree["show"] = "headings"

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

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

    map_button = tk.Button(frame, text="Display Geographical Map", bg="#FFFFFF",
                           fg="black", command=lambda: display_map(top, dataframe.iloc[0]['geographicalArea']))
    map_button.grid(row=len(dataframe.columns) + 1, column=2, pady=10, padx=50)
error_label= None
def display_error(message):
    global error_label
    if error_label is not None:
        error_label.config(text=message)

def back(root):
    root.grid_forget()

def date_parser(x):
    formats = ['%Y-%m-%d', '%m-%d-%Y', '%m/%d/%Y', '%Y/%m/%d' ]
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

    df['startDate'] = df['startDate'].dt.strftime('%Y-%m-%d')
    df['closingDate'] = df['closingDate'].dt.strftime('%Y-%m-%d')

    new_window = tk.Toplevel(root)
    new_window.title('Plans Table')

    # Create treeview to display table
    tree = ttk.Treeview(new_window, show='headings')
    tree['columns'] = list(df.columns)

    # Display columns
    for col in df.columns:
        tree.column(col, anchor='center')
        tree.heading(col, text=col, anchor='center')

    for i, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

    # Set specific width for planid, adminid, and active columns
    tree.column('PlanID', width=40)  # Set the width you desire
    tree.column('adminID', width=30)  # Set the width you desire
    tree.column('camp_id', width=50)
    tree.column('active', width=30)    # Set the width you desire
    tree.column('planName', width=200)
    tree.column('startDate', width=90)
    tree.column('closingDate', width=90)
    tree.column('geographicalArea', width=160)
    tree.column('planDesc', width=300)
    tree.column('NumberOfCamps', width=100)


    # Adding scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    new_window.geometry("1600x400")
    tree.pack(expand=True, fill='both')


def display_plan_frame(parent):
    global root
    root = tk.Frame(parent,width=600, height=600, bg='#021631')
    root.grid_propagate(False)

    # Create label and entry for Plan ID
    tk.Label(root, text="Select Plan ID",font="calibri 16",bg="#021631", fg="#fff").place(x=240,y=200)

    global combo
    plan_ids = load_plan_ids()
    combo = ttk.Combobox(root, values=plan_ids, state='readonly')
    combo.place(x=230, y=270)

    # Create 'Display Plan' button
    button = tk.Button(root, text="Display Plan", bg="#FFFFFF", command=display_plan)
    button.place(x=270, y=320)

    tk.Button(root, text="Display all plans", bg="#FFFFFF", fg="black", width=15, height=1,
              command=lambda: display_all_plan(root)).place(x=50, y=100)

    back_button=tk.Button(root, text="Back", width=10, bg="#FFFFFF", command=lambda:back(root))
    back_button.place(x=270, y=500)

    return root

if __name__=='__main__':
    root = tk.Tk()
    root.title("Admin home page")
    root.eval("tk::PlaceWindow . center")
    root.geometry("600x600")
    root['bg'] = '#021631'
    display_plan_frame(root)

    frame=display_plan_frame(root)
    frame.pack()

    root.mainloop()
