import numpy as np
import face_recognition
import picamera
from os import walk
from cv2 import imwrite, rectangle, putText, FONT_HERSHEY_SIMPLEX


class SmartCamera:
    def __init__(self):
        self.camera = picamera.PiCamera()  # camera initialization
        self.camera.resolution = (320, 240)
        self.output = np.empty((240, 320, 3), dtype=np.uint8)

        _, _, filenames = next(walk('people'))  # loading registered faces

        self.saved_pics, self.saved_names = zip(
            *[(face_recognition.face_encodings(face_recognition.load_image_file('people/' + file))[0], file[:-4]) for
              file in filenames if file.endswith('.jpg')])

    def capture(self, enter, time):
        self.camera.capture(self.output, format='rgb')

        face_locations = face_recognition.face_locations(self.output)
        face_encodings = face_recognition.face_encodings(self.output, face_locations)

        name = "Unknown Person"
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.saved_pics, face_encoding)
            name = "Unknown Person"

            for match, nm in zip(matches, self.saved_names):
                if match:
                    name = nm

            rectangle(self.output, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            putText(self.output, name, (left, y), FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        print(f"I see someone named {name}" + (' enter.' if enter else ' exit.'))

        # save picture
        imwrite("snaps/" + name + "_" + time + '.jpg', self.output[:, :, ::-1])

    def close(self):
        self.camera.close()
