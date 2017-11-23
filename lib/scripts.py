import os
from pprint import pprint

import numpy
from PIL import Image
import face_recognition
from random import randint


def pre_encode():
    dir_photos = 'photos/'  # Direktori menuju file tempat menyimpan foto
    dict_encodings = {}

    # Looping isi file di dalam directory
    for file in os.listdir(dir_photos):
        image = face_recognition.load_image_file(dir_photos + file)
        face_encoding = face_recognition.face_encodings(image)[0]

        # file_name = [x for x in map(str.strip, file.split('.')) if x][1]
        file_name = file
        dict_encodings[file_name] = face_encoding

    return dict_encodings


def match_image(input_face_encoding, face_encodings):
    results = face_recognition.face_distance(list(face_encodings.values()), input_face_encoding)
    distances = []

    i = 0
    for face in face_encodings:
        string_parsed = [x for x in map(str.strip, face.split('.')) if x]
        name = string_parsed[1]
        gender = string_parsed[0]
        tmp = {'name': name, 'gender': gender, 'value': results[i]}
        distances.append(tmp)

        i += 1

    newlist = sorted(distances, key=lambda k: k['value'])

    return newlist


def find_face(file_stream, face_encodings):
    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    img = face_recognition.load_image_file(file_stream)
    face_locations = face_recognition.face_locations(img)
    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    result = []

    i = 0
    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                    right))
        offset = 100
        # You can access the actual face itself like this:
        # face_image = img[top:bottom, left:right]
        face_image = img[top - offset:bottom + offset, left - offset:right + offset]

        pil_image = Image.fromarray(face_image)
        filename = 'uploaded/faces/' + str(i) + '.jpg'
        pil_image.save('static/' + filename, 'JPEG')

        mapping = {'top': top - offset, 'bottom': bottom + offset, 'left': left - offset, 'right': right + offset}

        input_face_encoding = face_recognition.face_encodings(face_image)[0]
        dict_res = {'mapping': mapping, 'filename': filename, 'rand': randint(0, 999999999),
                    'result': match_image(input_face_encoding, face_encodings)}
        result.append(dict_res)

        i += 1

    return result
