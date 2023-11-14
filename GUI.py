import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from PIL import ImageTk, Image
import DataVisualization


class GUI:
    def __init__(self, attendance_tracker):
        """
        The initialization function
        :param attendance_tracker: the attendance tracking system
        """
        # GUI initialization
        self.top = tk.Tk()
        self.time_label = None
        self.front = None

        # Image initialization
        self.background_label = None
        self.background_image = None
        self.overlay_photo = None
        self.image = Image.open("Images/background.png")
        self.logo = Image.open("Images/kpitlogo.png")
        # Display the images
        self.display_images()

        # Variable Initialization
        self.name_entry = None
        self.entry1 = None
        self.entry2 = None
        self.attendance = attendance_tracker
        self.visualization = DataVisualization.DataVis(self.attendance.database)

    def display_images(self):
        """
        Displays the background and logo images
        :return:
        """
        # Load the background image
        self.background_image = ImageTk.PhotoImage(self.image)
        # Create the background label and place it
        self.background_label = tk.Label(self.top, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.top.bind("<Configure>", self.resize_image)

        #Load the logo image
        resized_image = self.logo.resize((200, 100))
        self.overlay_photo = ImageTk.PhotoImage(resized_image)
        overlay_label = tk.Label(self.top, image=self.overlay_photo)
        overlay_label.place(x=0, y=0)
        self.top.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        """
        Resizes an image to fit the screen
        :param event: the event being resized
        :return:
        """
        new_width = event.width
        new_height = event.height
        resized_image = self.image.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.configure(image=self.background_image)

    def update_time(self):
        """
        Updates the time on the main GUI screen
        :return:
        """
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.top.after(1000, self.update_time)

    def display_message_submit_entry(self):
        """
        Submits the new entry into the database and facial recognition system
        :return:
        """
        first_name = self.entry1.get()
        employee_id = self.entry2.get()

        self.attendance.add_new_person(first_name, employee_id)
        # Clear the text entry boxes
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)

        self.front.destroy()
        messagebox.showinfo("Popup", "Entry Submitted!")

    def display_message_start(self):
        """
        Starts the facial recognition code
        :return:
        """
        self.attendance.detect_faces_and_count()

    def name_entry_gui(self):
        """
        Pops up a new GUI window to enter a new entry (face)
        :return:
        """
        self.front = tk.Toplevel(self.top)

        self.front.title("Data Entry")

        # Set the starting window size
        window_width = 400  # Desired width
        window_height = 200  # Desired height
        self.front.geometry(f"{window_width}x{window_height}")

        #Background
        background_image = ImageTk.PhotoImage(self.image)
        background_label = tk.Label(self.front, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.front.bind("<Configure>", self.resize_image)

        #Logo
        resized_img = self.logo.resize((200, 100))
        overlay_photo = ImageTk.PhotoImage(resized_img)
        overlay_lbl = tk.Label(self.front, image=overlay_photo)
        overlay_lbl.place(x=0, y=0)
        self.front.bind("<Configure>", self.resize_image)

        #name text entry
        first_name = tk.Label(self.front, text = "Name")
        first_name.pack()
        self.entry1 = tk.Entry(self.front, bd = 5)
        self.entry1.pack(anchor = "center")

        #KPIT ID text entry
        e_id = tk.Label(self.front, text = "KPIT ID")
        e_id.pack()
        self.entry2= tk.Entry(self.front, bd = 5)
        self.entry2.pack(anchor = "center")

        #Button to submit
        B3 = tk.Button(self.front, text ="Submit entry", command = self.display_message_submit_entry, cursor = "hand2")
        B3.pack(anchor = "center")

        self.front.mainloop()

    def display_message_end(self):
        """
        Ends the facial recognition code
        :return:
        """
        messagebox.showinfo("Popup", "Facial Recognition Ended")

    def display_hours(self):
        # Get the entered information
        name = self.name_entry.get()
        initial_date = self.entry1.get()
        end_date = self.entry2.get()

        # Data visualization code
        self.visualization.display_total_hours(name, initial_date, end_date)

        # Clear the text entry boxes
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)

    def weekly_hours_worked(self):
        """
        Pops up a new GUI window to enter a new entry (face)
        :return:
        """
        self.front = tk.Toplevel(self.top)

        self.front.title("Data Entry")

        # Set the starting window size
        window_width = 400  # Desired width
        window_height = 200  # Desired height
        self.front.geometry(f"{window_width}x{window_height}")

        # Background
        background_image = ImageTk.PhotoImage(self.image)
        background_label = tk.Label(self.front, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.front.bind("<Configure>", self.resize_image)

        # Logo
        resized_img = self.logo.resize((200, 100))
        overlay_photo = ImageTk.PhotoImage(resized_img)
        overlay_lbl = tk.Label(self.front, image=overlay_photo)
        overlay_lbl.place(x=0, y=0)
        self.front.bind("<Configure>", self.resize_image)

        # Name text entry
        e_id = tk.Label(self.front, text = "Name")
        e_id.pack()
        self.name_entry = tk.Entry(self.front, bd = 5)
        self.name_entry.pack(anchor = "center")

        # first date text entry
        first_name = tk.Label(self.front, text = "Initial Date")
        first_name.pack()
        self.entry1 = tk.Entry(self.front, bd = 5)
        self.entry1.pack(anchor = "center")

        # second date text entry
        e_id = tk.Label(self.front, text = "End Date")
        e_id.pack()
        self.entry2 = tk.Entry(self.front, bd = 5)
        self.entry2.pack(anchor = "center")

        #Button to submit
        B1 = tk.Button(self.front, text ="Display Hours", command = self.display_hours, cursor = "hand2")
        B1.pack(anchor = "center")

        #Button to close GUI
        B3 = tk.Button(self.front, text ="Done", command = self.front.destroy, cursor = "hand2")
        B3.pack(anchor = "center")

        self.front.mainloop()

    def download_csv(self):
        self.attendance.download_csv_data()

        messagebox.showinfo("Popup", "CSV Downloaded")


    def run_gui(self):
        """
        Runs the GUI interface
        :return:
        """
        self.top.title("Face Attendance System")

        # Set the starting window size
        window_width = 800  # Desired width
        window_height = 360  # Desired height
        self.top.geometry(f"{window_width}x{window_height}")

        #Display current time
        time = tk.Label(self.top, text="Current time:")
        time.pack()
        self.time_label = tk.Label(self.top, font=("Helvetica", 24))
        self.time_label.pack(anchor="center")
        self.update_time()

        #Button to make new entry
        B1 = tk.Button(self.top, text="Make new entry", command = self.name_entry_gui, cursor = "hand2")
        B1.pack(anchor="center")

        #Button to start facial recognition
        B3 = tk.Button(self.top, text="Start", command = self.display_message_start, cursor = "hand2")
        B3.pack(anchor="center")

        # Button to view a specific persons data
        B4 = tk.Button(self.top, text="View Weekly Hours Worked", command = self.weekly_hours_worked, cursor = "hand2")
        B4.pack(anchor="center")

        # Button to view a specific persons data
        B5 = tk.Button(self.top, text="Download CSV", command = self.download_csv, cursor = "hand2")
        B5.pack(anchor="center")

        B6 = tk.Button(self.top, text="End", command = self.display_message_end, cursor = "hand2")
        B6.pack(anchor="center")
        self.top.mainloop()

