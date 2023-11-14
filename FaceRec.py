'''A program that performs real-time face recognition using webcam video stream.'''
import os
import time
import face_recognition
import cv2

'''A class that contains the functions to perform face recognition.'''
class FaceReco():
    def __init__(self, known_faces_path, known_names_path):
        """
        Initialize the FaceRecognizer class.

        Args:
            known_faces_path (str): Path to the directory containing known face images.
            known_names_path (str): Path to the directory containing known names text files.
        """
        self.known_names_path = known_names_path
        self.known_faces_path = known_faces_path
        self.known_face_encodings = []

    def create_known_faces(self):
        """
        Load known face images, encode them, and store the encodings along with their names.
        """
        for filename in os.listdir(self.known_faces_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(self.known_faces_path, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]  # Use the first face encoding
                    name_file = filename.split('.')[0] + '.txt'  # Assuming name files have .txt extension
                    name_path = os.path.join(self.known_names_path, name_file)

                    if os.path.isfile(name_path):
                        with open(name_path, 'r') as f:
                            name = f.read().strip()

                        self.known_face_encodings.append((face_encoding, name))
                    else:
                        print(f"No name file found for '{filename}'.")

    def create_data(self, name):
        """
        Capture video frames from the webcam, save the image, and store the name in a text file.

        Args:
            name (str): The name to associate with the captured image.
        """
        video_capture = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame from the webcam
            ret, frame = video_capture.read()

            # Display the frame
            cv2.imshow('Video', frame)

            # Wait for 'q' key to exit and capture the image
            if cv2.waitKey(1) & 0xFF == ord('q'):
                try:
                    # Save the image
                    image_path = os.path.join(self.known_faces_path, f"{name}.jpg")
                    cv2.imwrite(image_path, frame)

                    # Save the name in a text file
                    name_path = os.path.join(self.known_names_path, f"{name}.txt")
                    with open(name_path, 'w') as f:
                        f.write(name)

                    print("Data saved successfully!")
                except:
                    print("Data not saved.")
                break

        # Release the video capture and close the windows
        video_capture.release()
        cv2.destroyAllWindows()

    def recognize_faces(self, frame):
        """
        Perform face recognition on a given frame.

        Args:
            frame (numpy.ndarray): The frame to perform face recognition on.

        Returns:
            List: A list of recognized faces, each containing the name and bounding box coordinates.
        """
        # Load known face encodings and names
        list_of_faces = []
        known_face_encodings = [item[0] for item in self.known_face_encodings]
        known_names = [item[1] for item in self.known_face_encodings]
        face_locations = face_recognition.face_locations(frame)
        new_face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_location, new_face_encoding in zip(face_locations, new_face_encodings):
            top, right, bottom, left = face_location
            matches = face_recognition.compare_faces(known_face_encodings, new_face_encoding)
            matched_indices = [i for i, match in enumerate(matches) if match]

            if matched_indices:
                first_matched_index = matched_indices[0]
                name = known_names[first_matched_index]
            else:
                name = "unknown"

            list_of_faces.append([name, [left, top, right, bottom]])

        return list_of_faces

    def replace_data(self, name):
        """
        Replace the existing data (image and name) for a given name.

        Args:
            name (str): The name to replace the existing data with.
        """
        image_path = os.path.join(self.known_faces_path, f"{name}.jpg")

        if os.path.isfile(image_path):
            video_capture = cv2.VideoCapture(0)

            while True:
                # Capture frame-by-frame from the webcam
                ret, frame = video_capture.read()

                # Display the frame
                cv2.imshow('Video', frame)

                # Wait for 'q' key to exit and replace the image
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    try:
                        # Replace the image
                        cv2.imwrite(image_path, frame)

                        print("Data replaced successfully!")
                    except:
                        print("Data not replaced.")
                    break

            # Release the video capture and close the windows
            video_capture.release()
            cv2.destroyAllWindows()
        else:
            print(f"No existing data found for '{name}'.")

    def runfacerec(self):
        """
        Perform real-time face recognition using webcam video stream.
        """
        # Open the video capture from the webcam
        #self.create_known_faces()
        video_capture = cv2.VideoCapture(0)

        # Check if the video capture was successfully opened
        if not video_capture.isOpened():
            print("Error opening video capture")
            return

        start_time = time.time()
        frame_count = 0
        old_names = []

        # Iterate over each frame in the video stream
        while True:
            new_names = []

            # Read the current frame
            ret, frame = video_capture.read()

            # If the frame was not read successfully, exit the loop
            if not ret:
                break

            # Perform face recognition on the frame
            data = self.recognize_faces(frame)

            # Determine entered and exited faces
            for f in data:
                new_names.append(f[0])
            new_names = set(new_names)
            old_names = set(old_names)
            entered = list(new_names - old_names)
            if entered:
                entered.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            print("Entered:")
            print(entered)
            exited = list(old_names - new_names)
            if exited:
                exited.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            print("Exited:")
            print(exited)

            # Update previous faces with current data
            old_names = new_names

            # Display the frame with bounding boxes and names
            for face in data:
                name, bounding_box = face
                left, top, right, bottom = bounding_box

                # Draw bounding box
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Draw name label
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Calculate FPS
            frame_count += 1
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time

            # Display FPS on the frame
            cv2.putText(frame, f"FPS: {round(fps, 2)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Display the frame with bounding boxes and names
            cv2.imshow("Frame with Bounding Boxes", frame)

            # Wait for the 'q' key to be pressed to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object and close any open windows
        video_capture.release()
        cv2.destroyAllWindows()
