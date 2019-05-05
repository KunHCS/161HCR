from flask import (Flask, send_from_directory, render_template,
                   request, jsonify)
from pathlib import Path
from .config import Config
import numpy as np
import re
import base64
from keras.preprocessing.image import img_to_array
from flask_cors import CORS
from PIL import Image
import io
from .hasy import predict_hasy, predict_mnist

from scipy.misc import imsave, imread, imresize

app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)
CORS(app)


# decoding an image from base64 into raw representation
def convert_image(image_data):
    image_str = re.search(b'base64,(.*)', image_data).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(image_str))
    image = Image.open(io.BytesIO(base64.b64decode(image_str)))
    image = preprocess_image(image, (32, 32))
    return image

# decoding an image from base64 into raw representation for MNIST model
def convert_image2(image_data):
    image_str = re.search(b'base64,(.*)', image_data).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(image_str))
    image = Image.open(io.BytesIO(base64.b64decode(image_str)))
    image = preprocess_image(image, (28, 28))
    return image


def preprocess_image(image, size):
    image = remove_transparency(image).convert('L')
    image = image.resize(size, Image.BICUBIC)
    image = image.point(lambda x: 0 if x < 255 else 255, '1')
    image.save('resize.png')
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency
    print('Image mode: ', im.mode)
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



# Route for HASYv2 model
# user input image
@app.route('/image', methods=['POST', 'GET'])
def image_route():
    mapping = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'x', 'y',
               'z']

    image_data = request.get_data()
    image = convert_image(image_data)
    print(image.shape)
    image = image.astype(np.float32)


    out = predict_hasy(image)
    out = out.item()
    print('OUTPUT', mapping[out])
    return jsonify({'Result': mapping[out], 'Symbol': out}), 200

# Route for MNIST model
@app.route('/image2', methods=['POST', 'GET'])
def image_route2():
    image_data = request.get_data()
    image = convert_image2(image_data)
    print(image.shape)
    image = image.astype(np.float32)
    
    out = predict_mnist(image)
    #out = np.array_str(out)
    print('OUTPUT', out)
    return jsonify({'Result': int(out)}), 200


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
