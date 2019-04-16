from flask import (Flask, send_from_directory, render_template,
                   render_template_string, request, jsonify)
from pathlib import Path
from .config import Config
from .machine_learning.mnist.testMnist import test_mnist

app = Flask(__name__, static_folder=Config.STATIC_PATH,
            template_folder=Config.TEMPLATE_PATH)
app.config.from_object(Config)


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
@app.route('/image', methods=['POST'])
def image_route():
    
    imgData = request.get_data()
    print ('test:', imgData)
    allowed_extension = ('.png', '.jpg', '.jpeg')
    file = request.files.get('image', None)
    if not file or not file.filename.lower().endswith(allowed_extension):
        return jsonify({'msg': 'Wrong key, no file or invalid file type. File '
                               'must be an images in .png .jpg .jpeg '
                               'format'}), 400

    # pass to processing instead of saving
    file.save('api_image.png')
    return jsonify({'msg': 'Image Received'}), 200


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
