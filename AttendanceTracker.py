import face_recognition
from FaceRec import FaceReco
import mysql.connector
import time
import datetime
import cv2
from Database import Database
import GUI
from ultralytics import YOLO


class AttendanceTracker:
    def __init__(self, database, face_recog):
        self.database = database
        self.facerecog = face_recog
        self.model = YOLO('yolov8n.pt')

    def download_csv_data(self):
        """
        Function that downloads a csv of all the data in the system
        :return:
        """
        self.database.export_to_csv()

    def update_times(self, entered=None, exited=None):
        try:
            entryTime = entered[-1]
            enteredNames = entered[0:-1]
            # print(enteredNames)
            for name in enteredNames:
                # print(name)
                exist = self.database.select_from_table(name)
                employee_table_name = 'table_employees'
                employee_info = self.database.select_from_table(name, employee_table_name)
                if not exist:
                    self.database.insert_into_table(name, employee_info[0][1], entryTime)
                # print(exist)
                if exist[0][2] == None:
                    self.database.update_times(exist[0][0], entryTime, exist[0][3])
        except:
            pass
        try:
            exitTime = exited[-1]
            exitedNames = exited[0:-1]
            for ename in exitedNames:
                eexist = self.database.select_from_table(ename)
                # print(eexist)
                self.database.update_times(eexist[0][0], eexist[0][2], exitTime)
        except:
            pass

    def add_new_person(self, name, employeeID):
        """
        add a new person to the database
        :return:
        """
        self.facerecog.create_data(name)
        self.facerecog.create_known_faces()
        # self.database.insert_into_table(name, employeeID, None)
        self.database.insert_into_employee_table(name, employeeID)

    def detect_faces_and_count(self):
        self.facerecog.create_known_faces()
        old_names = []
        # Open the default webcam (usually index 0)
        cap = cv2.VideoCapture(0)
        OnFaces = 0

        def is_face(class_id):
            # Define the class index for "face" in the YOLO model's class list
            face_class_index = 0
            return class_id == face_class_index

        while True:
            nFaces = 0
            new_names = []
            ret, frame = cap.read()

            if not ret:
                break

            # Predict using the YOLO model
            results = self.model(frame)

            # Access the detected boxes and class IDs
            boxes = results[0].boxes.xyxy
            classIDs = results[0].boxes.cls

            # Loop through the detected objects and draw bounding boxes around faces
            for box, classID in zip(boxes, classIDs):
                if is_face(classID):
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    nFaces += 1

            cv2.putText(frame, "Number of faces: " + str(nFaces), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2)

            # Display the frame with the detected faces
            cv2.imshow('Detected Faces', frame)

            # Press 'q' to exit the loop and close the window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if not (nFaces == OnFaces): # If the number of faces has changed
                # Perform face recognition on the frame
                data = self.facerecog.recognize_faces(frame)
                for f in data:
                    new_names.append(f[0])
                new_names = set(new_names) # Remove duplicates
                old_names = set(old_names) # Remove duplicates
                entered = list(new_names - old_names) # Find the names that have entered
                if entered:
                    entered.append(time.strftime("%H:%M:%S")) # Add the current time to the list
                    self.update_times(entered, None)
                    print("Entered:")
                    print(entered)
                else:
                    entered = None

                exited = list(old_names - new_names)
                if exited:
                    exited.append(time.strftime("%H:%M:%S"))
                    self.update_times(None, exited)
                    print("Exited:")
                    print(exited)
                else:
                    exited = None

                # Update previous faces with current data
                old_names = new_names

            OnFaces = nFaces

        # Release the capture and close the window
        cap.release()
        cv2.destroyAllWindows()
