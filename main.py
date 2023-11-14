from FaceRec import FaceReco
from Database import Database
from AttendanceTracker import AttendanceTracker
from GUI import GUI
import datetime


# Get today's date
today = datetime.date.today()

# Format the date as MMDDYYYY
formatted_date = today.strftime("%m%d%Y")

# Initialize the database
data = Database(formatted_date)
host = input("Enter the host IP address: ")
port = input("Enter the port number: ")
database = input("Enter the database name: ")
user = input("Enter the username: ")
password = input("Enter the password: ")
data.configure_database(host, port, database, user, password)

data.create_table(formatted_date)

# Initialize the face recognition
known_faces_path = 'KnownFaces'
known_names_path = 'KnownNames'
facerecog = FaceReco(known_faces_path, known_names_path)

# Initialize the attendance tracker
attendance = AttendanceTracker(data, facerecog)

# Run the GUI
g = GUI(attendance)
g.run_gui()
