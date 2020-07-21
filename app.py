from flask import Flask, request, jsonify

import face_recognition
from PIL import Image
import base64
import numpy as np
import io

app = Flask(__name__)


@app.route("/", methods=['GET'])
def homepage():
    return {'status': "Success"}


@app.route("/", methods=['POST'])
def check():
    image_1 = np.array(Image.open(io.BytesIO(
        base64.b64decode(request.form['data1']))))
    image_1_face_encoding = face_recognition.face_encodings(image_1)[0]

    known_face_encodings = [image_1_face_encoding]
    known_face_names = [request.form['name']]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    test_1 = np.array(Image.open(io.BytesIO(
        base64.b64decode(request.form['data2']))))
    test_1_face_encoding = face_recognition.face_encodings(test_1)[0]
    face_encodings.append(test_1_face_encoding)

    print()
    print("Result".center(100, "*"))
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print(name)
            return {'status': 'Success', 'name': name}, 200

    return {'status': 'Failure'}, 401


if __name__ == "__main__":
    app.run(debug=True)
