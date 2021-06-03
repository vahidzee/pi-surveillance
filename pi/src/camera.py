import numpy as np
import face_recognition
import picamera
from PIL import Image
from io import BytesIO


class SmartCamera:
    def __init__(self, encodings, ids):
        self.camera = picamera.PiCamera()  # camera initialization
        self.camera.resolution = (320, 240)
        self.output = np.empty((240, 320, 3), dtype=np.uint8)

        # loading registered faces
        self.saved_pics = encodings
        self.saved_ids = ids

    def capture(self):
        self.camera.capture(self.output, format='rgb')

        face_locations = face_recognition.face_locations(self.output)
        face_encodings = face_recognition.face_encodings(self.output, face_locations)
        print(len(face_locations))
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.saved_pics, face_encoding)
            face_found = False
            for match, saved_id in zip(matches, self.saved_ids):
                if match:
                    face_found = True
                    yield {'known': True, 'face_id': saved_id}
            if not face_found:
                byte_io = BytesIO()
                Image.fromarray(self.output[top:bottom+1, left:right+1, ::1]).save(byte_io, 'png')
                byte_io.seek(0)
                yield {'known': False, 'pic': byte_io, 'embedding': face_encoding.tolist()}

    def add_face(self, enc, face_id):
        self.saved_pics.append(enc)
        self.saved_ids.append(face_id)

    def set_faces(self, encodings, ids):
        self.saved_pics = encodings
        self.saved_ids = ids

    def close(self):
        self.camera.close()
