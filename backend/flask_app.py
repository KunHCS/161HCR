from flask import (Flask, send_from_directory, render_template,
                   request, jsonify)
from pathlib import Path
from .config import Config
# scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
# for matrix math
import matplotlib.pyplot as plt
import numpy as np
# for regular expressions, saves time dealing with string data
import re
import base64
from keras import backend as K
from keras.preprocessing.image import img_to_array
from .machine_learning.mnist.mnist_loader import predict_output
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)
CORS(app)


# decoding an image from base64 into raw representation
def convertImage(imgData1):
    imgstr = re.search(b'base64,(.*)', imgData1).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))
    image = Image.open(io.BytesIO(base64.b64decode(imgstr)))
    image = preprocess_image(image, (28, 28))
    return image


def preprocess_image(image, size):
    image = remove_transparency(image).convert('L')
    image = image.point(lambda x: 0 if x < 128 else 255, '1')
    image = image.resize(size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency
    if im.mode in ('RGBA', 'LA') or (
            im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format

        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


# user input image
@app.route('/image', methods=['POST', 'GET'])
def image_route():
    imgData = request.get_data()

    # print ('test:', imgData)
    image = convertImage(imgData)
    print(image.shape)
    x = imread('output.png', mode='L')
    print(image[0].shape)
    image = image.reshape(1, 28, 28)
    plt.imsave('original.png', image[0])
    # compute a bit-wise inversion so black becomes white and vice versa
    # x = np.invert(x)

    # change size
    x = imresize(x, (28, 28))
    plt.imsave('resized.png', image[0])
    # convert to a 4D tensor to feed into our model
    x = x.reshape(1, 28, 28)

    out = predict_output(image)
    print('OUTPUT', out)
    out = out.item()
    # print(np.argmax(out, axis=1))
    K.clear_session()

    # response = np.array_str(np.argmax(out, axis=0))
    return jsonify({'output': out}), 200

    # print(np.argmax(out,axis=1))
    # convert the response to a string
    # response = np.array_str(np.argmax(out,axis=1))
    # return response
    # print(np.argmax(out,axis=1))
    # convert the response to a string
    # response = np.array_str(np.argmax(out,axis=1))

    # allowed_extension = ('.png', '.jpg', '.jpeg')
    # file = request.files.get('image', None)
    # if not file or not file.filename.lower().endswith(allowed_extension):
    #    return jsonify({'msg': 'Wrong key, no file or invalid file type. File '
    #                           'must be an images in .png .jpg .jpeg '
    #                           'format'}), 400

    # pass to processing instead of saving
    # file.save('api_image.png')
    # return jsonify({'msg': 'Image Received'}), 200


# Catch all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    file_path = './client/build'
    if path and Path(file_path + '/' + path).exists():
        print('sent: ', path)
        return send_from_directory(Config.TEMPLATE_PATH, path)
    print(f'caught: /{path}')
    return render_template('index.html')
