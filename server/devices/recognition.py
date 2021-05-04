import json
import itertools
import face_recognition as fr
from PIL import Image
import numpy as np


def get_faces(image: Image):
    """get a list of (`face_embedding`, `face_image`) tuples in the provided image"""
    image = np.array(image.convert('RGB'))
    return [(embedding, Image.fromarray(image[top:bottom, left:right])) for embedding, (top, right, bottom, left) in
            zip(fr.face_encodings(image), fr.face_locations(image))]


def find_face(user, image: Image = None, embedding: np.array = None, ):
    """finds similar face to provided image/embedding """
    from .models import Face
    embedding = embedding if embedding is not None else fr.face_encodings(np.array(image.convert('RGB')))[0]
    embeddings, faces = [], []
    for face in Face.objects.filter(user=user) if user is not None else Face.objects.all():
        if not face.embedding:
            continue
        embeddings.append(json.loads(face.embedding))
        faces.append(face)
    matches = fr.compare_faces(np.array(embeddings), embedding)
    if not sum(matches):
        return False
    match = itertools.compress(faces, matches)
    return next(match)
