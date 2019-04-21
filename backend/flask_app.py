from flask import (Flask, send_from_directory, render_template,
                   render_template_string, request, jsonify)
from pathlib import Path
from .config import Config
#scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
#for matrix math
import numpy as np
#for regular expressions, saves time dealing with string data
import re
import base64
from keras import backend as K


from .machine_learning.mnist.testMnist import test_mnist
from .machine_learning.mnist.mnist_loader import predict_output


app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)


#decoding an image from base64 into raw representation
def convertImage(imgData1):
    imgstr = re.search(b'base64,(.*)',imgData1).group(1)
    with open('output.png','wb') as output:
        output.write(base64.b64decode(imgstr))



# Test mnist predict
@app.route('/test')
def test_ml():
    result = test_mnist()
    print(result)
    template_str = '''
    <h1>Result</h1>
    <p>Value: {{value}}</p>
    <img src={{img}} alt={{value}} height="42" width="42">
    '''
    return render_template_string(template_str, value=str(result))


# user input image
@app.route('/image', methods=['POST', 'GET'])
def image_route():
    
    imgData = request.get_data()
    
    #print ('test:', imgData)
    convertImage(imgData)

    x = imread('output.png',mode='L')

    #compute a bit-wise inversion so black becomes white and vice versa
    x = np.invert(x)

    #change size
    x = imresize(x,(28,28))

    #convert to a 4D tensor to feed into our model
    x = x.reshape(1,28,28,1)

    out = predict_output(x)
    print('test2', out)
    print(np.argmax(out,axis=1))
    K.clear_session()

    response = np.array_str(np.argmax(out,axis=0))
    return response 

    #print(np.argmax(out,axis=1))
     #convert the response to a string
    #response = np.array_str(np.argmax(out,axis=1))
    #return response 
    #print(np.argmax(out,axis=1))
        #convert the response to a string
    #response = np.array_str(np.argmax(out,axis=1))


    
    #allowed_extension = ('.png', '.jpg', '.jpeg')
    #file = request.files.get('image', None)
    #if not file or not file.filename.lower().endswith(allowed_extension):
    #    return jsonify({'msg': 'Wrong key, no file or invalid file type. File '
    #                           'must be an images in .png .jpg .jpeg '
    #                           'format'}), 400

    # pass to processing instead of saving
    #file.save('api_image.png')
    #return jsonify({'msg': 'Image Received'}), 200


# Catch all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    file_path = './client/build'
    if path and Path(file_path+'/'+path).exists():
        print('sent: ', path)
        return send_from_directory(Config.TEMPLATE_PATH, path)
    print(f'caught: /{path}')
    return render_template('index.html')
