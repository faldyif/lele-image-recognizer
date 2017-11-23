# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename

import os
from lib.scripts import pre_encode, find_face

face_encodings = pre_encode()

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploaded/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # The image file seems valid! Detect faces and return the result.
            face_find = find_face(file, face_encodings)

            return render_template('output.html', face_find=face_find, filename=filename)

    filename = ''
    # If no valid image file was uploaded, show the file upload form:
    return render_template('home.html', filename=filename)


# buat load halaman webkem dan declare fungsi webcam untuk dapat dipanggil pada file html
@app.route('/webkem')
def webkem():
    os.system('python3.6 facerec_from_webcam_faster.py')
    # If no valid image file was uploaded, show the file upload form:
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
